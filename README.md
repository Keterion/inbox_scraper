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

Running it with `-v` (`python inbox.py -v`) will enable verbose so a lot more yapping, up to you if you want that.

(Also, you might have to edit `inbox.py`. On line 35 or so, in the get_dump function, the url contains the string "SU5CT1g". It might be that that is not the mailbox ID you have.
### Getting your mailbox ID
There are two ways I know of.

The first one is to hover over any attachment and look at the link. After your email and before a bunch of random characters there should be something resembling the SU5CT1g I found. Just take that and replace the text in `inbox.py`.

Alternatively, open the inspector, click on the network tab, then on an email. One of the GET requests will have a normal number under the File column, that's the email.
Click on that request, and somewhere you should see the GET request that was made. And there, in between /mailbox/ and /message/ should be the ID you're looking for.

## Configuration
Little to nothing here, you can check out `lib.py` and see if you want to change any of the default state things.

The two relevant things are *save_dir*, so the directory the mails are saved under, and *get_ammount*.

The higher *get_ammount* is, the worse it would be if the program were to fail because you'd loose stuff. Yeah.
