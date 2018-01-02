# file_grabber
[![License](http://img.shields.io/:license-mit-blue.svg)](https://github.com/l50/mass-wpscan/blob/master/LICENSE)

Download all available files on a target web application for one or many
user accounts. So far this has been tested exclusively on an old
instance of [DragonFly](https://dragonflycms.org/). Can be useful to
find files that don't have proper permissions set (unauth users are able
to access privileged files).

### Install the Requests library using pip:
```
pip install –r requirements.txt
```
-or-
```
pip install requests
```

### Change user_pass.txt.example to user_pass.txt in the auth directory,
and specify usernames and passwords for the site in the following
format:

```
username/password
username2/password2
```

### Change config.py.example to config.py and specify the configuration
parameters:
- site: The target site
- download_uri: The URI path for downloading files on the target site
- login_page: The login page on the target site (POST based auth)
- creds_file: Holds the credentials to access the site
- downloads_folder: The name of the folder that should be created to
  store the downloaded files
- n: The number of permutations of a file the script should grab
  (accounts for duplicate naming schemes)

### Run the code:
```
python file_grabber.py
```

## License
MIT
