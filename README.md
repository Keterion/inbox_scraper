# Iserv Scraper
## Setup
### Dependencies:
[python](https://www.python.org/downloads/) >= 3.12

[requests](https://pypi.org/project/requests/) = *

### Files
You need to write information into these two files:

username(.txt) - iserv username (i.e. "john.doe")

password(.txt) - iserv password (i.e. "passw0rd")

The files should be in the same folder as this README file.

## Execution
Run `python inbox.py`. The command needs to be executed from the folder this README is in.

### Flags
|**Flag**   |                 **Action**                    |
|-----------|-----------------------------------------------|
| `-v`      | **Verbose**, more yapping                     |
| `-s`      | **Silent**, no output                         |
| `-i`      | **Ignore** list of already downloaded emails  |
| `--sent`  | Uses the mailbox ID for the sent emails       |

### Mailbox ID
(Also, you might have to edit `lib.py`. In there you have the inboxID and outboxID. You need to change those.
#### Getting your mailbox ID
There are two ways I know of.

The first one is to hover over any attachment and look at the link. After your email and before a bunch of random characters there should be something resembling the SU5CT1g I found. Just take that and replace the text in `inbox.py`.

Alternatively, open the inspector, click on the network tab, then on an email. One of the GET requests will have a normal number under the File column, that's the email.
Click on that request, and somewhere you should see the GET request that was made. And there, in between /mailbox/ and /message/ should be the ID you're looking for.

## Configuration
Little to nothing here, you can check out `lib.py` and see if you want to change any of the default state things.

The two relevant things are *inbox_directory* and *outbox_directory*, which is the directory the mails are saved under, and *get_ammount*.

The higher *get_ammount* is, the worse it would be if the program were to fail because you'd loose stuff. Yeah.
