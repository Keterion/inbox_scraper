import requests
from os import path, makedirs


def write_file(file: str, data: str):
    with open(file, "w") as f:
        f.write(data)
        f.flush()


def read_file_line(file):
    with open(file, "r") as f:
        return f.readline().replace("\n", "")


def gen_payload():
    return {
        "_username": read_file_line("username.txt"),
        "_password": read_file_line("password.txt"),
    }


def gen_session() -> requests.Session:
    s = requests.Session()
    url = "https://fvbschulen.eu/iserv/auth/login"
    # s.get(url)
    res = s.post(url, data=gen_payload())
    return s


def gen_state() -> dict:
    return {
        "get_ammount": 10,
        "total": 0,
        "inbox_directory": "inbox",
        "outbox_directory": "sent",
        "inboxID": "SU5CT1g",
        "outboxID": "SU5CT1gvU2VudA",
        "username": read_file_line("username.txt") + "@fvbschulen.eu",
    }


def ensure_path(p: str):
    if not (path.exists(p)):
        makedirs(p)
