import os
from config import *
from instapy import InstaPy
from instapy import smart_run
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

session = InstaPy(username=os.getenv("INSTA_USERNAME"),
                  password=os.getenv("INSTA_PASSWORD"),
                  headless_browser=False,
                  bypass_security_challenge_using='sms')

target_accounts = [account]

if not os.path.isdir(PARSE_FOLDER):
    os.mkdir(PARSE_FOLDER)

with smart_run(session):

    for account in target_accounts:
        f = open(PARSE_FOLDER + account + '_followers.txt', 'w')
        target_followers = session.grab_followers(username=account,
                                                  amount="full",
                                                  live_match=False,
                                                  store_locally=False)
        for el in target_followers:
            f.write(el + "\n")

        f.close()
