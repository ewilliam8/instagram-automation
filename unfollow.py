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


with smart_run(session):

    # instapy_followed_enabled отписываемся от пользователей,
    # на которых были подписаны с помощью бота Instapy
    session.unfollow_users(amount=60,
                           instapy_followed_enabled=True,
                           instapy_followed_param="all",
                           style="FIFO",
                           unfollow_after=90*60*60,
                           sleep_delay=501)
    session.unfollow_users(amount=60,
                           instapy_followed_enabled=True,
                           instapy_followed_param="nonfollowers",
                           style="FIFO",
                           unfollow_after=90*60*60,
                           sleep_delay=501)

    # nonFollowers отписываемся от пользователей, которые не подписались на вас
    session.unfollow_users(amount=126,
                           nonFollowers=True,
                           style="RANDOM",
                           unfollow_after=42*60*60,
                           sleep_delay=655)

    # allFollowing отписываемся от всех пользователей
    session.unfollow_users(amount=40,
                           allFollowing=True,
                           style="LIFO",
                           unfollow_after=3*60*60,
                           sleep_delay=450)

    # FIFO (первым пришел – первым вышел), бот будет отписываться от
    # пользователей в точном порядке их загрузки (это значение по умолчанию);
    # LIFO (последним пришел-первым вышел), бот отписывается от пользователей
    # в порядке, обратном их загрузки; RANDOM, бот отписываться от
    # пользователей в произвольном порядке;
