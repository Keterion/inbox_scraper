# Iserv Scraper
## Setup
### Dependencies:
[python](https://www.python.org/downloads/) >= 3.12

[requests](https://pypi.org/project/requests/) = *

### Files
username.txt - iserv username (i.e. "john.doe")

password.txt - iserv password (i.e. "passw0rd")

The files should be in the same folder as this README file.

## Execution
Run `python inbox.py`. The command needs to be executed from the folder this README is in.

Running it with `-v` (`python iserv_scraper/inbox.py -v`) will enable verbose more so a lot more yapping you probably don't want

## Configuration
Little to nothing here, you can check out `lib.py` and see if you want to change any of the default state things.

The two relevant things are *save_dir*, so the directory the mails are saved under, and get_ammount.

The higher get_ammount is, the worse it would be if the program were to fail because you'd loose stuff. Yeah.
