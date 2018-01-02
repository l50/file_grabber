import config
import requests
import re
import os

__auth__ = 'jayson.e.grace@gmail.com'


class FileGrab(object):
    """ Used to grab all files that a user can access on a website.
    These values are pulled from the config.py file.
    """

    def __init__(self):
        self.site_creds = []

    def read_credentials(self):
        """ Read credentials out of a text file and adds them to the site_creds instance variable.
        Credentials must be in the following format to be parsed properly:
        username/password
        """
        with open(config.creds_file, 'r') as f:
            for line in f:
                line = line.strip().split('/')
                self.site_creds.append((line[0], line[1]))
        return

    def connect_to_site(self, account):
        """ Connect to the website specified in the login_page instance variable.
        
        :type account: tuple
        :param account: username and password to use for authentication
       
       :return session that comes from successfully authenticating to the site
        """
        payload = {
            'username': account[0],
            'password': account[1]
        }
        with requests.Session() as s:
            s.post(config.login_page, data=payload)
        return s

    def download_helper(self, response, account, fname, i):
        """ Helper method to assist download_files with saving the file to disk.

        :type response: Request object
        :param response: current Request object

        :type account: string
        :param account: account name

        :type fname: string
        :param fname: name of file to be downloaded

        :type i: string
        :param i: iterator for the current file
        """
        fname = fname.strip('"').split('.')
        if len(fname) > 1:
            filepath = 'downloads/' + account + '/' + fname[0] + str(i) + '.' + fname[1]
        else:
            filepath = 'downloads/' + account + '/' + fname[0] + str(i)
        with open(filepath, 'wb') as f:
            for block in response.iter_content(1024):
                f.write(block)

    def download_files(self, session, account):
        """ Iterates through n (specified in config) different file URLs for type doc and type bug.
        This parameter can be adjusted based on manual examination of the web application.
        Several pages may have files with the same name, so the script adds an iterator value onto the file name to
        prevent overwriting. The files are downloaded into <specified downloads folder>/<account name>.

        :type session: Session object
        :param session: current Session object

        :type account: string
        :param account: account name
        """
        for i in range(1, config.n):
            response = session.get(config.site + config.download_uri + str(i) + '&type=doc')
            d = response.headers['content-disposition']
            fname = re.findall("filename=(.+)", d)[0]
            self.download_helper(response, account, fname, i)
            response = session.get(config.site + config.download_uri + str(i) + '&type=bug')
            d = response.headers['content-disposition']
            fname = re.findall("filename=(.+)", d)[0]
            self.download_helper(response, account, fname, i)
            print "Downloaded files for iterator value " + str(i)

    def grab_files(self):
        for account in self.site_creds:
            print account
            session = self.connect_to_site(account)
            if not os.path.exists(config.downloads_folder + account[0]):
                os.makedirs(config.downloads_folder + account[0])
            self.download_files(session, account[0])


def main():
    """ Main entry point """
    fg = FileGrab()
    fg.read_credentials()
    fg.grab_files()


if __name__ == '__main__':
    main()
