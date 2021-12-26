import config
from instapy import smart_run


def parse_followers(session, target_accounts):
    with smart_run(session):

        for account in target_accounts:
            f = open(config.PARSE_FOLDER + account + '_followers.txt', 'w')
            target_followers = session.grab_followers(username=account,
                                                      amount="full",
                                                      live_match=False,
                                                      store_locally=False)
            for el in target_followers:
                f.write(el + "\n")

            f.close()


if __name__ == "__main__":

    import os
    from instapy import InstaPy
    from dotenv import load_dotenv

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    session = InstaPy(username=os.getenv("INSTA_USERNAME"),
                      password=os.getenv("INSTA_PASSWORD"),
                      headless_browser=config.HEADLESS_BROWSER_BOOL,
                      bypass_security_challenge_using='sms',
                      want_check_browser=True)

    target_accounts = [config.account]
    parse_followers(session, target_accounts)
