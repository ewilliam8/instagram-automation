import os
import time
import json
import random
import config
import requests

from bs4 import BeautifulSoup
from instapy import InstaPy
from instapy import smart_run
from instapy import set_workspace
from dotenv import load_dotenv


class Actions:

    def __init__(self):
        self.here = os.path.abspath(os.path.dirname(__file__))
        self.dotenv_path = os.path.join(
            os.path.dirname(__file__), '..', '.env')
        if os.path.exists(self.dotenv_path):
            load_dotenv(self.dotenv_path)
        path_to_manager = os.path.join(
            self.here + "\\" +
            "manager" + "\\" +
            str(os.getenv("INSTA_USERNAME")) + "\\")
        self.filtered_file = os.path.join(
            path_to_manager +
            str(config.FILTER_FOLDER) +
            str(config.account) + "_filtered.txt")
        self.interacted_file = os.path.join(
            path_to_manager +
            str(config.INTERACTED_FILE))

        set_workspace(path=path_to_manager)
        proxy = {
            "username": str(os.getenv("PROXY_LOGIN")),
            "password": str(os.getenv("PROXY_PASSWORD")),
            "address": str(os.getenv("PROXY_IP")),
            "port": str(os.getenv("PROXY_PORT"))
        }

        if bool(proxy):
            self.session = InstaPy(
                username=str(os.getenv("INSTA_USERNAME")),
                password=str(os.getenv("INSTA_PASSWORD")),
                headless_browser=False,
                bypass_security_challenge_using='sms',
                disable_image_load=True,
                want_check_browser=True,
                proxy_username=proxy["username"],
                proxy_password=proxy["password"],
                proxy_address=proxy["address"],
                proxy_port=proxy["port"])
            input("\nВведите Логин и Пароль для прокси," +
                  "введите любую клавишу и нажмите Enter")
        else:
            self.session = InstaPy(
                username=str(os.getenv("INSTA_USERNAME")),
                password=str(os.getenv("INSTA_PASSWORD")),
                headless_browser=config.HEADLESS_BROWSER_BOOL,
                bypass_security_challenge_using='sms',
                want_check_browser=True)
        self.session.set_dont_include(config.exclude_accaunts)
        self.session.set_relationship_bounds(
            enabled=True,
            max_followers=8500,
            max_following=4490,
            min_followers=40,
            min_following=40,
            min_posts=1,
            max_posts=2000)
        self.session.set_quota_supervisor(
            enabled=True,
            sleep_after=["likes",
                         "comments_d",
                         "follows",
                         "unfollows",
                         "server_calls_h"],
            sleepyhead=True,
            stochastic_flow=True,
            notify_me=True,
            peak_likes_hourly=57,
            peak_likes_daily=585,
            peak_comments_hourly=21,
            peak_comments_daily=182,
            peak_follows_hourly=48,
            peak_follows_daily=238,
            peak_unfollows_hourly=35,
            peak_unfollows_daily=402,
            peak_server_calls_hourly=None,
            peak_server_calls_daily=4700)
        self.session.set_action_delays(
            enabled=True,
            like=8,
            comment=5,
            follow=4.17,
            unfollow=28,
            story=10)
        self.session.set_skip_users(
            skip_private=False,
            private_percentage=100,
            skip_no_profile_pic=True,
            no_profile_pic_percentage=100,
            skip_business=True,
            skip_non_business=False,
            business_percentage=100,
            skip_business_categories=[],
            dont_skip_business_categories=config.person_categories,
            skip_bio_keyword=config.skip_bio_keyword,
            mandatory_bio_keywords=[])
        self.session.set_mandatory_language(
            enabled=True,
            character_set=['CYRILLIC'])

    def interact_by_feed(self, amount_interact=50):
        with smart_run(self.session, threaded=True):
            self.session.set_do_story(
                enabled=True,
                percentage=95,
                simulate=True)
            self.session.like_by_feed(
                amount=amount_interact,
                randomize=True,
                unfollow=True,
                interact=True)

    def follow(self, amount=35):
        with smart_run(self.session, threaded=True):
            target_followers = []

            f = open(self.filtered_file).readlines()
            for _ in range(0, amount):
                user = f.pop(0).replace('\n', '')
                target_followers.append(user)

            with open(self.filtered_file, 'w', encoding='UTF-8') as F:
                F.writelines(f)

            with open(self.interacted_file, 'a', encoding='UTF-8') as f:
                for el in target_followers:
                    f.write(el + "\n")

            self.session.set_simulation(enabled=True, percentage=66)
            self.session.set_do_story(enabled=True, percentage=100,
                                      simulate=True)
            self.session.set_do_like(True, percentage=55)
            self.session.follow_by_list(followlist=target_followers, times=1,
                                        sleep_delay=600, interact=True)

    def unfollow(self, amount_unf=60):
        with smart_run(self.session, threaded=True):
            self.session.unfollow_users(
                amount=amount_unf,
                allFollowing=True,
                style="FIFO",
                unfollow_after=3*60*60,
                sleep_delay=450)

    def full_parse_followers(self):
        with smart_run(self.session, threaded=True):
            target_accounts = [config.account]
            for account in target_accounts:
                followers_file = self.here + "\\" + \
                    "manager" + "\\" + \
                    os.getenv("INSTA_USERNAME") + "\\" + \
                    config.PARSE_FOLDER.replace("/", "\\") + \
                    config.account + "_followers.txt"

                f = open(followers_file, 'w', encoding='UTF-8')
                target_followers = self.session.grab_followers(
                    username=account,
                    amount="full",
                    live_match=False,
                    store_locally=False)

                for el in target_followers:
                    f.write(el + "\n")

                f.close()


class NoLoginActions:

    def __init__(self):
        self.here = os.path.abspath(os.path.dirname(__file__))
        self.manager_file = os.path.join(
            self.here + "\\" +
            "manager" + "\\" +
            str(os.getenv("INSTA_USERNAME")) + "\\" +
            str(config.MANAGER_FILE))
        self.parse_file = os.path.join(
            self.here, "\\",
            "manager", "\\",
            str(os.getenv("INSTA_USERNAME")), "\\",
            str(config.PARSE_FOLDER),
            str(config.account), "_followers.txt")
        self.filtered_file = os.path.join(
            self.here, "\\",
            "manager", "\\",
            str(os.getenv("INSTA_USERNAME")), "\\",
            str(config.FILTER_FOLDER),
            str(config.account), "_filtered.txt")
        self.interacted_file = os.path.join(
            self.here, "\\",
            "manager", "\\",
            str(os.getenv("INSTA_USERNAME")), "\\",
            "interacted.txt")

        # proxy = {"https": "https://LOGIN:PASSWORD@IP:PORT"}
        self.proxy = None

    def __manager_add(self, key, value):
        with open(self.manager_file, "r", encoding='UTF-8') as file_manager:
            data = json.load(file_manager)

        data[os.getenv("INSTA_USERNAME")][key].append(value)

        with open(self.manager_file, "w", encoding='UTF-8') \
                as file_manager_w:
            json.dump(data, file_manager_w)

    def __check_user(self, username,
                     skip_words=[],
                     non_skip_business_categories=[],
                     skip_private=True
                     ):

        min_followers = 50
        max_followers = 10000
        min_following = 50
        max_following = 10000
        min_posts = 1
        max_posts = 2000

        self.__manager_add("already_filtered", username)

        def find_nth(haystack, needle, n):
            start = haystack.find(needle)
            while start >= 0 and n > 1:
                start = haystack.find(needle, start+len(needle))
                n -= 1
            return start

        print(f"\n--> Checking {username}")

        # check by username
        for skip_word in config.skip_name_keywords:
            if username.find(skip_word) != -1:
                print(f"× The user has a name with: {skip_word}")
                return None

        # check with already interacted users
        interacted_users = open(self.interacted_file,
                                'r', encoding='UTF-8').readlines()
        for index, elem in enumerate(interacted_users, start=0):
            interacted_users[index] = elem[:-1]

        if username in interacted_users:
            print(f"× The user has been already interacted")
            return None

        # --- SERVER CALL ---
        url = f'https://www.instagram.com/{username}/'
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/96.0.4664.110 Safari/537.36'}
        if self.proxy is not None:
            r = requests.get(url, headers=headers, proxies=self.proxy)
        else:
            r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.text, 'lxml')
        follows_name_posts = str(soup.find_all("meta")[13])

        bio_and_desc = str(soup.find_all("script"))
        bio_and_desc = bio_and_desc.encode("utf-16", "surrogatepass") \
                                   .decode("utf-16", "surrogatepass")
        biography_extra = bio_and_desc[
            bio_and_desc.find('biography'):
            bio_and_desc.find('blocked_by_viewer')][12:-3]
        biography_extra_decoded = biography_extra \
            .encode("utf-16", "surrogatepass") \
            .decode("utf-16", "surrogatepass")
        bio_and_desc = bio_and_desc[
            find_nth(bio_and_desc, "<script", 5):
            find_nth(bio_and_desc, "</script", 5)]

        followers = follows_name_posts.split(" ")[1][9:]
        if followers[-1] == 'm':
            followers = 1000000
        elif followers[-1] == 'k':
            followers = 100000
        else:
            followers = int(str(followers).replace(',', ''))

        following = follows_name_posts.split(" ")[3]
        if following[-1] == 'm':
            following = 1000000
        elif following[-1] == 'k':
            following = 100000
        else:
            following = int(str(following).replace(',', ''))

        posts = follows_name_posts.split(" ")[5]
        posts = int(str(posts).replace(',', ''))
        name = str(follows_name_posts.split(" ")[14:-2])[1:-1]
        name_decoded = name \
            .replace("'", '').replace(',', '') \
            .encode("utf-16", "surrogatepass") \
            .decode("utf-16", "surrogatepass")
        biography = bio_and_desc[
            bio_and_desc.find("biography") + 12:
            bio_and_desc.find("blocked_by_viewer") - 3]
        biography_decoded = biography \
            .encode("utf-16", "surrogatepass") \
            .decode("utf-16", "surrogatepass")

        # Ограничения по подписчикам, подпискам и кол-во постов
        if followers < min_followers or followers > max_followers:
            print(
              f"× The user has unacceptable amount of followers: {followers}")
            return None

        if following < min_following or following > max_following:
            print(
              f"× The user has unacceptable amount of following: {following}")
            return None

        if posts < min_posts or posts > max_posts:
            print(f"The user has unacceptable amount of posts: {posts}")
            return None

        # Бизнес аккаунт
        is_business = bio_and_desc[
            bio_and_desc.find("is_business_account"):
            bio_and_desc.find("is_professional_account")][21:-2]
        if is_business == 'true':
            business_category = str.encode(
                bio_and_desc[
                    bio_and_desc.find("business_category_name"):
                    bio_and_desc.find("overall_category_name")][25:-3]) \
                    .decode('unicode_escape')

            if business_category not in non_skip_business_categories:
                print(f"× It's a business account: {business_category}")
                return None

        # Приватный аккаунт?
        is_private = bio_and_desc[
            bio_and_desc.find("is_private"):
            bio_and_desc.find("is_verified")][12:-2]
        if is_private == 'true' and skip_private:
            print("× User skipped by private account")
            return None

        # Слова в имени и био
        for word in skip_words:
            word_to_print = word
            word = str(word.encode("unicode_escape"))\
                .replace('\\\\', '\\')[2:-1]

            if name.find(word) != -1 and \
                    name_decoded.find(word) != -1:
                print(f"× User skipped by keyword in Name: {word_to_print}")
                return None

            if biography.find(word) != -1 and \
                    biography_decoded.find(word) != -1:
                print(f"× User skipped by keyword in Bio: {word_to_print}")
                return None

            if biography_extra.find(word) != -1 and \
                    biography_extra_decoded.find(word) != -1:
                print(f"× User skipped by keyword in Bio: {word_to_print}")
                return None

        print("+ Added to a list")
        return username

    def filter(self, amount=9):
        for gi in range(0, amount):

            accounts_to_check = []
            exception_occurred = 0
            with open(self.parse_file, 'r', encoding='UTF-8') as f:
                userslist = f.readlines()
                for _ in range(0, 10):
                    user = userslist.pop(0).replace('\n', '')
                    accounts_to_check.append(user)
                with open(self.parse_file, 'w', encoding='UTF-8') as F:
                    F.writelines(userslist)

            filtered_accounts = []
            for username in accounts_to_check:

                local_check_user = None
                try:
                    local_check_user = self.__check_user(
                        username,
                        config.skip_bio_keyword,
                        config.person_categories,
                        False)
                except Exception as ex:
                    exception_occurred += 1
                    print("An exception occurred")
                    print(ex)

                    if exception_occurred >= 5:
                        print("\n\nSome problems with Instagram!\n")
                        print("Close the program\n")
                        exit()

                if local_check_user is not None:
                    filtered_accounts.append(local_check_user)
                    print(filtered_accounts)

                time.sleep(random.randint(1, 5))

            with open(self.filtered_file, 'a', encoding='UTF-8') as f:

                for el in filtered_accounts:
                    f.write(el + "\n")

            print(f"\n~~ Users checked [{(gi + 1) * 10}/{amount * 10}]")
            if (gi + 1) != amount:
                print("~~ Sleeping between 1 and 5 minutes")
                time.sleep(random.randint(60, 300))


if __name__ == "__main__":

    actions = Actions()

    actions.follow(35)
    actions.unfollow(35)

    del actions
