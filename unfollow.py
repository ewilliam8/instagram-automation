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
                  headless_browser=os.getenv("HEADLESS_BROWSER"),
                  bypass_security_challenge_using='sms',
                  want_check_browser=True)


with smart_run(session):

    session.set_quota_supervisor(enabled=True,
                                 sleep_after=["likes", "comments_d", "follows",
                                              "unfollows", "server_calls_h"],
                                 sleepyhead=True,
                                 stochastic_flow=True,
                                 notify_me=True,
                                 peak_unfollows_hourly=35,
                                 peak_unfollows_daily=402,
                                 peak_server_calls_hourly=None,
                                 peak_server_calls_daily=4700)
    # instapy_followed_enabled отписываемся от пользователей,
    # на которых были подписаны с помощью бота Instapy
    # session.unfollow_users(amount=60,
    #                        instapy_followed_enabled=True,
    #                        instapy_followed_param="all",
    #                        style="FIFO",
    #                        unfollow_after=90*60*60,
    #                        sleep_delay=501)
    session.unfollow_users(amount=60,
                           instapy_followed_enabled=True,
                           instapy_followed_param="nonfollowers",
                           style="FIFO",
                           unfollow_after=90*60*60,
                           sleep_delay=501)

    # nonFollowers отписываемся от пользователей, которые не подписались на вас
    # session.unfollow_users(amount=126,
    #                        nonFollowers=True,
    #                        style="RANDOM",
    #                        unfollow_after=42*60*60,
    #                        sleep_delay=655)

    # allFollowing отписываемся от всех пользователей
    # session.unfollow_users(amount=40,
    #                        allFollowing=True,
    #                        style="LIFO",
    #                        unfollow_after=3*60*60,
    #                        sleep_delay=450)

    # FIFO (первым пришел – первым вышел), бот будет отписываться от
    # пользователей в точном порядке их загрузки (это значение по умолчанию);
    # LIFO (последним пришел-первым вышел), бот отписывается от пользователей
    # в порядке, обратном их загрузки; RANDOM, бот отписываться от
    # пользователей в произвольном порядке;
