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
                  headless_browser=bool(os.getenv("HEADLESS_BROWSER")),
                  bypass_security_challenge_using='sms',
                  want_check_browser=True)


def feed_interact():

    with smart_run(session):
        session.set_do_story(enabled=True, percentage=95, simulate=True)
        session.like_by_feed(amount=100, randomize=True, unfollow=True,
                             interact=True)
        session.end(threaded_session=True)


if __name__ == "__main__":
    feed_interact()
