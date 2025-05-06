# Iserv Scraper
## Setup
### Dependencies:
python >= 3.12
requests = *

### Files
username.txt - iserv username (i.e. "john.doe")
password.txt - iserv password (i.e. "passw0rd")

The files should be in the same folder as this README file.

## Execution
Run `python iserv_scraper/inbox.py`. The command needs to be executed from the folder this README is in.

Alternatively, move the `inbox.py` *and* `lib.py` files to the same folder as username.txt and password.txt (or the .txt files to the .py files)

Running it with `-v` (`python iserv_scraper/inbox.py -v`) will enable verbose more so a lot more yapping you probably don't want
