import json
from requests import Session
import lib
from os import mkdir, path
import sys


def get_json(session: Session, url: str) -> dict:
    r = session.get(url)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        exit(f"get_json: {r.status_code}")


def convert_date(date: str):
    return date
    # return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
    ##split_str = date.replace("/", ":").replace(" ", ":").replace(".", ":").split(":")
    ### order is day month year hour minute am/pm
    ##if(len(split_str) == 6):
    ##    if(split_str[5].lower() == "pm"):
    ##        split_str[3] = str(int(split_str[3])+12)
    ##
    ##order = [2, 1, 0, 3, 4]
    ##ret = ""
    ##for index in order:
    ##    ret += split_str[index]
    ##return ret


def get_dump(start: int, ammount: int, username: str, mailbox: str, s: Session) -> dict:
    return get_json(
        s,
        f"https://fvbschulen.eu/iserv/mail/api/v2/account/{username}/message?mailbox[]={mailbox}&limit={ammount}&offset={start}&sort=date&order=desc",
    )


def get_email(url: str, s: Session) -> str:
    r = s.get(url)
    if r.status_code == 200:
        return r.text
    else:
        return str(r.status_code)


if __name__ == "__main__":
    # verbose logging when running with -v
    pprint = print if "-s" not in sys.argv else lambda *b: None
    vprint = pprint if len(sys.argv) >= 2 and "-v" in sys.argv else lambda *a: None
    ignore_previous_downloads = "-i" in sys.argv

    if path.exists("downloaded.json"):
        with open("downloaded.json", "r") as f:
            downloaded = json.loads(f.read())
    else:
        downloaded = []

    s = lib.gen_session()
    state: dict = lib.gen_state()

    mailboxID = state["inboxID"] if "--sent" not in sys.argv else state["outboxID"]
    save_directory = (
        state["inbox_directory"]
        if "--sent" not in sys.argv
        else state["outbox_directory"]
    )

    emails_per_get = state["get_ammount"]
    start = 0
    dump = get_dump(start, emails_per_get, state["username"], mailboxID, s)

    while state["total"] < dump["total"]:
        try:
            emails = dump["items"]
            for mail in emails:
                if mail["id"]["uid"] in downloaded and not ignore_previous_downloads:
                    pprint("Skipping " + mail["subject"])
                    state["total"] += 1
                    continue  # skips any email that has been downloaded
                try:
                    filename = (
                        convert_date(mail["date"])
                        + str(mail["id"]["uid"])
                        + f":{mail['from'][0]['display']}-{mail['subject']}".replace(
                            "/", "_"
                        )
                        .replace("\n", "")
                        .replace("\r", "")
                    )
                    pprint("\nDownloading: " + mail["subject"])
                    contents = get_email(
                        f'https://fvbschulen.eu/iserv/mail/api/v2/account/{state["username"]}/mailbox/{mailboxID}/message/{mail["id"]["uid"]}',
                        s,
                    )
                    vprint("Got email response")
                    if len(contents) > 3:
                        # vprint("Filename: " + filename)
                        contents = json.loads(contents)
                        attachments = contents["attachments"]
                        if len(attachments) > 0:
                            pprint(
                                "Found "
                                + str(len(attachments))
                                + " attachments, downloading..."
                            )
                            lib.ensure_path(
                                path.join(save_directory, filename, "attachments")
                            )
                        for attachment in attachments:
                            attachment_name = attachment["data"]["filename"]
                            vprint("Getting attachment data...")
                            with s.get(
                                f'https://fvbschulen.eu/iserv/fs/file/mail/{attachment["data"]["messageId"]["accountId"]}/{attachment["data"]["messageId"]["mailboxId"]}/{attachment["data"]["headerMessageId"]}/{attachment["data"]["partId"]}/{attachment["data"]["filename"]}',
                                stream=True,
                            ) as r:
                                vprint("Downloading attachment data stream...")
                                r.raise_for_status()
                                with open(
                                    path.join(
                                        save_directory,
                                        filename,
                                        "attachments",
                                        attachment_name,
                                    ),
                                    "wb",
                                ) as f:
                                    for chunk in r.iter_content(chunk_size=4096):
                                        f.write(chunk)
                            pprint("   Downloaded " + attachment_name)
                        try:
                            text = contents["content"]["plain"][0]["content"]
                            lib.write_file(
                                path.join(save_directory, filename, filename + ".txt"),
                                text,
                            )
                        except:
                            vprint("Mail {mail['subject']} has no text")
                        state["total"] += 1
                        if not ignore_previous_downloads:
                            downloaded.append(mail["id"]["uid"])
                        pprint(f"Saved {mail['subject']}")
                    else:
                        pprint(f"Error getting {mail['subject']}")
                except Exception as e:
                    pprint(e)

            start += emails_per_get
            dump = get_dump(start, emails_per_get, state["username"], mailboxID, s)
            lib.write_file("downloaded.json", json.dumps(downloaded))
        except KeyboardInterrupt:
            pprint("Exiting...")
            lib.write_file("downloaded.json", json.dumps(downloaded))
            break

    lib.write_file("downloaded.json", json.dumps(downloaded))
    exit(0)
