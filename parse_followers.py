from config  import insta_username,\
                    insta_password
from instapy import InstaPy
from instapy import smart_run
import os

session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=False,
                  bypass_security_challenge_using='sms')

PARSE_FOLDER  = "PARSE/"
target_accounts = ["skycode_school"]

if not os.path.isdir(PARSE_FOLDER):
    os.mkdir(PARSE_FOLDER)

with smart_run(session):

    for account in target_accounts:
    
        f = open(PARSE_FOLDER + account + '_followers.txt', 'w')
        target_followers = session.grab_followers(username=account, amount="full", live_match=False, store_locally=False)
        for el in target_followers:
            f.write(el + "\n")

        f.close()


        


    



