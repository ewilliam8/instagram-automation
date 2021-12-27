from instapy import InstaPy
from instapy import smart_run


def unfollow(session):
    with smart_run(session):

        session.set_quota_supervisor(enabled=True,
                                     sleep_after=["likes", "comments_d",
                                                  "follows", "unfollows",
                                                  "server_calls_h"],
                                     sleepyhead=True,
                                     stochastic_flow=True,
                                     notify_me=True,
                                     peak_unfollows_hourly=35,
                                     peak_unfollows_daily=402,
                                     peak_server_calls_hourly=None,
                                     peak_server_calls_daily=4700)
        session.unfollow_users(amount=60,
                               instapy_followed_enabled=True,
                               instapy_followed_param="nonfollowers",
                               style="FIFO",
                               unfollow_after=90*60*60,
                               sleep_delay=501)
        session.end(threaded_session=True)

# instapy_followed_enabled - отписываемся от пользователей, на которых
#   были подписаны с помощью бота Instapy

# session.unfollow_users(amount=60, instapy_followed_enabled=True,
# instapy_followed_param="all", style="FIFO",
# unfollow_after=90*60*60, sleep_delay=501)

# session.unfollow_users(amount=60, instapy_followed_enabled=True,
# instapy_followed_param="nonfollowers", style="FIFO",
# unfollow_after=90*60*60, sleep_delay=501)


if __name__ == "__main__":

    import os
    import config
    from dotenv import load_dotenv

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    session = InstaPy(username=os.getenv("INSTA_USERNAME"),
                      password=os.getenv("INSTA_PASSWORD"),
                      headless_browser=config.HEADLESS_BROWSER_BOOL,
                      bypass_security_challenge_using='sms',
                      want_check_browser=True)

    unfollow(session)
