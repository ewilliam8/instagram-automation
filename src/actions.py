if __name__ == "src.actions":
    import src.config as config
else:
    import config

import os
import time
import json
import random
import datetime
import requests

from bs4 import BeautifulSoup
from instapy import InstaPy
from instapy import smart_run
from instapy import set_workspace


class NoLoginActions:

    def __init__(self):
        self.here = os.path.abspath(os.path.dirname(__file__))
        self.manager_file = os.path.join(
            self.here + "\\" +
            "manager" + "\\" +
            config.insta_username + "\\" +
            config.MANAGER_FILE)
        self.interacted_file = os.path.join(
            self.here + "\\" +
            "manager" + "\\" +
            config.insta_username + "\\" +
            "interacted.txt")
        self.filtered_file = os.path.join(
            self.here + "\\" +
            "manager" + "\\" +
            config.insta_username + "\\" +
            str(config.FILTER_FOLDER) +
            username + "_filtered.txt")
        self.parse_file = os.path.join(
            self.here + "\\" +
            "manager" + "\\" +
            config.insta_username + "\\" +
            str(config.PARSE_FOLDER) +
            username + "_followers.txt")

        # proxy = {"https": "https://LOGIN:PASSWORD@IP:PORT"}
        self.proxy = None

    def __print_info(self, to_print):
        time_now = datetime.datetime.now()
        today_date = time_now.strftime("%Y-%m-%d %H:%M:%S")
        username = config.insta_username
        print(f"INFO [{today_date}] [{username}]  {to_print}")

    def check_user(self, username,
                   skip_words=[],
                   non_skip_business_categories=[],
                   skip_private=True
                   ):

        min_followers = 50
        max_followers = 10000
        min_following = 50
        max_following = 10000
        min_posts = 0
        max_posts = 2000

        def find_nth(haystack, needle, n):
            start = haystack.find(needle)
            while start >= 0 and n > 1:
                start = haystack.find(needle, start+len(needle))
                n -= 1
            return start

        print()
        self.__print_info(f"|> Checking {username}")

        # check by username
        for skip_word in config.skip_name_keywords:
            if username.find(skip_word) != -1:
                self.__print_info(f"× The user has a name with: {skip_word}")
                return None

        # check with already interacted users
        interacted_users = open(self.interacted_file,
                                'r', encoding='UTF-8').readlines()
        for index, elem in enumerate(interacted_users, start=0):
            interacted_users[index] = elem[:-1]

        if username in interacted_users:
            self.__print_info(f"× The user has been already interacted")
            return None

        # --- SERVER CALL ---
        url = f'https://www.instagram.com/{username}/'
        headers = headers = config.request_headers
        try:
            if self.proxy is not None:
                r = requests.get(url, headers=headers, proxies=self.proxy)
            else:
                r = requests.get(url, headers=headers)

            soup = BeautifulSoup(r.text, 'lxml')
            follows_name_posts = str(soup.find_all("meta")[13])
        
        except Exception as ex:
            print(ex)
            return None

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

        # Limits on subscribers, subscriptions and number of posts
        if followers < min_followers or followers > max_followers:
            self.__print_info(
              f"× The user has unacceptable amount of followers: {followers}")
            return None

        if following < min_following or following > max_following:
            self.__print_info(
              f"× The user has unacceptable amount of following: {following}")
            return None

        if posts < min_posts or posts > max_posts:
            self.__print_info(
                f"The user has unacceptable amount of posts: {posts}")
            return None

        # Business account
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
                self.__print_info(
                    f"× It's a business account: {business_category}")
                return None

        # Private account?
        is_private = bio_and_desc[
            bio_and_desc.find("is_private"):
            bio_and_desc.find("is_verified")][12:-2]
        if is_private == 'true' and skip_private:
            self.__print_info("× User skipped by private account")
            return None

        # Words in name and bio
        for word in skip_words:
            word_to_print = word
            word = str(word.encode("unicode_escape"))\
                .replace('\\\\', '\\')[2:-1]

            if name.find(word) != -1 and \
                    name_decoded.find(word) != -1:
                self.__print_info(
                    f"× User skipped by keyword in Name: {word_to_print}")
                return None

            if biography.find(word) != -1 and \
                    biography_decoded.find(word) != -1:
                self.__print_info(
                    f"× User skipped by keyword in Bio: {word_to_print}")
                return None

            if biography_extra.find(word) != -1 and \
                    biography_extra_decoded.find(word) != -1:
                self.__print_info(
                    f"× User skipped by keyword in Bio: {word_to_print}")
                return None

        self.__print_info("+ Added to a list")
        return username

    def filter(self, username, amount=9):
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
                    local_check_user = self.check_user(
                        username,
                        config.skip_bio_keyword,
                        config.person_categories,
                        False)
                except Exception as ex:
                    exception_occurred += 1
                    self.__print_info("An exception occurred")
                    self.__print_info(ex)

                    if exception_occurred >= 5:
                        self.__print_info(
                            "\n\nSome problems with Instagram!\n")
                        self.__print_info("Close the program\n")
                        exit()

                if local_check_user is not None:
                    filtered_accounts.append(local_check_user)
                    self.__print_info(filtered_accounts)

                time.sleep(random.randint(1, 5))

            with open(self.filtered_file, 'a', encoding='UTF-8') as f:

                for el in filtered_accounts:
                    f.write(el + "\n")

            print()
            self.__print_info(
                f"~~ Users checked [{(gi + 1) * 10}/{amount * 10}]")
            if (gi + 1) != amount:
                self.__print_info("~~ Sleeping between 1 and 5 minutes")
                time.sleep(random.randint(60, 300))


class Actions:

    def __init__(self):

        if config.insta_username is None:
            print("The user has not been chosen")
            exit()

        self.here = os.path.abspath(os.path.dirname(__file__))
        self.path_to_manager_folder = os.path.join(
            self.here + "\\" +
            "manager" + "\\" +
            config.insta_username + "\\")
        self.interacted_file = os.path.join(
            self.path_to_manager_folder +
            str(config.INTERACTED_FILE))
        self.path_to_manager_file = os.path.join(
            self.path_to_manager_folder + config.MANAGER_FILE)

        set_workspace(path=self.path_to_manager_folder)

        if config.proxy_ip is not None:
            self.session = InstaPy(
                username=config.insta_username,
                password=config.insta_password,
                proxy_port=config.proxy_port,
                proxy_address=config.proxy_ip,
                proxy_username=config.proxy_login,
                proxy_password=config.proxy_password,
                headless_browser=False,
                bypass_security_challenge_using='sms',
                disable_image_load=True,
                want_check_browser=True)
            print("\nВведите Логин и Пароль для прокси," +
                  "введите любую клавишу и нажмите Enter")
            input(f"LOGIN: {config.proxy_login}\n" +
                  f"PASSWORD: {config.proxy_password}\n")
        else:
            self.session = InstaPy(
                username=config.insta_username,
                password=config.insta_password,
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

    def _manager_get_data(self):
        with open(self.path_to_manager_file, "r", encoding='UTF-8') as file:
            data = json.load(file)
        return data

    def _manager_set_data(self, new_data):
        with open(self.path_to_manager_file,
                  "w", encoding='UTF-8') as file_manager:
            json.dump(new_data, file_manager, indent=4)
    
    def _get_interacted_users(self):
        interacted_users = open(self.interacted_file,
            'r', encoding='UTF-8').readlines()
        for index, elem in enumerate(interacted_users, start=0):
            interacted_users[index] = elem[:-1]

        return interacted_users

    def _add_interacted_users(self, new_data):
        with open(self.interacted_file, 'a', encoding='UTF-8') as f:
            for el in new_data:
                f.write(el + "\n")

    def interact_by_feed(self, amount_interact: int = 40):
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

        return self

    def follow(self, username, amount: int = 35):
        target_followers = []
        filtered_file = os.path.join(
            self.path_to_manager_folder + "\\" +
            str(config.FILTER_FOLDER) + "\\" +
            username + "_filtered.txt")

        with smart_run(self.session, threaded=True):

            f = open(filtered_file).readlines()
            for _ in range(0, amount):
                user = f.pop(0).replace('\n', '')
                target_followers.append(user)

            with open(filtered_file, 'w', encoding='UTF-8') as F:
                F.writelines(f)

            with open(self.interacted_file, 'a', encoding='UTF-8') as f:
                for el in target_followers:
                    f.write(el + "\n")

            self.session.set_simulation(enabled=True, percentage=66)
            self.session.set_do_story(enabled=True, percentage=100,
                                      simulate=True)
            self.session.set_do_like(True, percentage=55)
            self.session.follow_by_list(target_followers, times=1,
                                        sleep_delay=600, interact=True)

        return self

    def follow_user_followers(self):
        with smart_run(self.session, threaded=True):
            self.session.set_user_interact(
                amount=1,
                randomize=True,
                percentage=45,
                media='Photo')
            self.session.follow_user_followers(
                config.target_accounts,
                amount=35,
                interact=True,
                randomize=False)

        return self

    def unfollow(self, amount_unf: int = 60):
        with smart_run(self.session, threaded=True):
            self.session.unfollow_users(
                amount=amount_unf,
                allFollowing=True,
                style="LIFO",
                unfollow_after=3*60*60,
                sleep_delay=450)

        return self

    def choose_accounts(self):

        def check_account_followers(username):
            url = f'https://www.instagram.com/{username}/'
            headers = config.request_headers

            if config.proxy_ip is not None:
                proxy = {"https": f"https://{config.proxy_login}:" +
                         "{config.proxy_password}@{config.proxy_ip}:" +
                         "{config.proxy_port}"}
                r = requests.get(url, headers=headers, proxies=proxy)
            else:
                r = requests.get(url, headers=headers)

            soup = BeautifulSoup(r.text, 'lxml')
            follows_name_posts = str(soup.find_all("meta")[13])
            followers = follows_name_posts.split(" ")[1][9:]

            return followers

        accounts_to_parse = []

        
        data = self._manager_get_data()
        data_m = data

        time_now = datetime.datetime.now()
        today_date = time_now.strftime("%Y-%m-%d")

        for index, user in enumerate(data_m["donor_accounts"], start=0):
            username = user["username"]
            user_followers = check_account_followers(username)
            user_followers = user_followers.replace(",", "")

            if user_followers.find('k') == -1 and \
               user_followers.find('m') == -1:
                user_followers = int(user_followers)

            data_user_followers = \
                data["donor_accounts"][index]["count_followers"]

            if isinstance(data_user_followers, int) and \
               isinstance(user_followers, int):

                if user_followers > data_user_followers:
                    data_m["donor_accounts"][index]["count_followers"] = \
                        user_followers
                    data_m["donor_accounts"][index]["date"] = today_date
                    accounts_to_parse.append(username)

            if isinstance(data_user_followers, str) and \
                    isinstance(user_followers, int):
                continue

            elif isinstance(data_user_followers, int) and \
                    isinstance(user_followers, str):
                data_m["donor_accounts"][index]["count_followers"] = \
                        user_followers
                data_m["donor_accounts"][index]["date"] = today_date
                accounts_to_parse.append(username)

            else:
                if data_user_followers != user_followers:
                    data_m["donor_accounts"][index]["count_followers"] = \
                        user_followers
                    data_m["donor_accounts"][index]["date"] = today_date
                    accounts_to_parse.append(username)

            self.session.logger.info(
                f'"{username}" has \t{user_followers} followers')
            time.sleep(random.randint(5, 15))

        self._manager_set_data(data_m)

        return set(accounts_to_parse)

    # delete
    def old_follow_actual_users(self):
        parsed_followers = []
        target_accaunts = self.choose_accounts()
        self.session.logger.info("Now parsing these accounts: " +
                                 str(target_accaunts)[1:-1])

        with smart_run(self.session, threaded=True):
            for user in target_accaunts:
                self.session.logger.info(f"Now parsing username: {user}")
                parsed = self.session.grab_followers(
                    username=user,
                    amount="full",
                    live_match=False,
                    store_locally=True)

                # сохранить данные в PARSE/ user_followers.txt
                followers_file_path = os.path.join(
                    self.path_to_manager_folder + config.PARSE_FOLDER +
                    "\\" + user + "_followers.txt")

                if not os.path.exists(followers_file_path):
                    with open(followers_file_path,
                              'w', encoding='UTF-8') as f:
                        for el in parsed:
                            f.write(el + "\n")
                else:
                    # сравниваем списки
                    followers_list = open(followers_file_path).readlines()
                    difference = list(set(parsed) - set(followers_list))

                    # сравним и добавим разницу в массив
                    parsed_followers.append(difference)

                    # добавить в manager в actual_interacted
                    data = self._manager_get_data()

                    data["actual_interacted"] = \
                        sum(data["actual_interacted"].append(difference), [])

                    self._manager_set_data(data)

                    # обновить файл с подписками
                    with open(followers_file_path,
                              'w', encoding='UTF-8') as f:
                        for el in parsed:
                            f.write(el + "\n")

            parsed_followers = sum(parsed_followers, [])

            nl_actions = NoLoginActions()
            filtered_followers = []

            for user in parsed_followers:
                ret = nl_actions.check_user(
                    user,
                    config.skip_bio_keyword,
                    config.person_categories,
                    False)

                if ret is not None:
                    filtered_followers.append(ret)

                time.sleep(random.randint(3, 10))

            self.session.logger.info(len(filtered_followers))
            self.session.logger.info(filtered_followers)

            # follow ()

        return self

    def grab_user_followers(self, user):
        with smart_run(self.session, threaded=True):
            self.session.logger.info(f"Now parsing username: {user}")
            parsed = self.session.grab_followers(
                username=user,
                amount="full",
                live_match=False,
                store_locally=True)

            # сохранить данные в PARSE/ user_followers.txt
            followers_file_path = os.path.join(
                self.path_to_manager_folder + config.PARSE_FOLDER +
                "\\" + user + "_followers.txt")

            with open(followers_file_path, 'w', encoding='UTF-8') as f:
                for el in parsed:
                    f.write(el + "\n")

        return self

    def follow_actual_users(self):
        with smart_run(self.session, threaded=True):
            usernames = config.target_accounts
            usernames = random.shuffle(usernames)

            for i in range(0, len(usernames)):
                self.session.logger.info(
                    f"Now parsing actual followers from: {usernames[i]}, [{i + 1}/{len(usernames)}]"
                )
                actual_followers = self.session.get_actual_followers(usernames[i])
                if not actual_followers:
                    continue

                # filter

                filtered_followers = actual_followers
                # nl_actions = NoLoginActions()
                # filtered_followers = []

                # for index,user in enumerate(actual_followers, start=1) :
                #     ret = nl_actions.check_user(
                #             user,
                #             config.skip_bio_keyword,
                #             config.person_categories,
                #             False)

                #     if ret is not None:
                #         filtered_followers.append(ret)
                    
                #     self.session.logger.info(
                #         f"[{index}/{len(actual_followers)}]"
                #     )

                #     time.sleep(random.randint(4, 10))

                # del nl_actions
                # self.session.logger.info(
                #     f"Length of filtered actual followers: {len(filtered_followers)}, [{i + 1}/{len(usernames)}]"
                # )

                # follow
                self.session.logger.info(
                    f"Start follow actual followers of {usernames[i]}"
                )
                self.session.set_simulation(enabled=True, percentage=66)
                self.session.set_do_story(enabled=True, percentage=100,
                                          simulate=True)
                self.session.set_do_like(True, percentage=55)
                self.session.follow_by_list(filtered_followers, times=1,
                                            sleep_delay=600, interact=True)

                self.session.logger.info(
                    f"~~ Now sleeping for a while, [{i + 1}/{len(usernames)}]"
                )
                time.sleep(random.randint(300, 600))

if __name__ == "__main__":

    print(f"INSTAGRAM AUTOMATION v{config.PROGRAM_VERSION}\n")

    usernames = config.get_all_usernames()
    if len(usernames) != 1:
        for index, username in enumerate(usernames, start=1):
            print(f"{index} ", end='')
            print(username)
        account_number = input("Choose an account: ")
        config.set_account_variables(int(account_number))
    else:
        config.set_account_variables(1)

    print("\n1) follow 35")
    print("2) unfollow 65")
    print("3) follow actual users")
    print("4) interact by feed")
    print("5) follow user followers")
    print("6) grab user followers")
    print("7) filter user followers")
    print("8) follow actual users")
    action_numb = int(input("Choose an action: "))

    if action_numb == 1:
        filtered_list_username = input("Input username of filtered base: ")
        actions = Actions()
        actions.follow(filtered_list_username, 35)

    if action_numb == 2:
        actions = Actions()
        actions.unfollow(65)

    if action_numb == 3:
        actions = Actions()
        actions.follow_actual_users()

    if action_numb == 4:
        actions = Actions()
        actions.interact_by_feed()

    if action_numb == 5:
        actions = Actions()
        actions.follow_user_followers()

    if action_numb == 6:
        actions = Actions()
        username = input("\nUsername to grab ALL followers: ")
        actions.grab_user_followers(username)

    if action_numb == 7:
        nl_actions = NoLoginActions()
        username = input("\nUsername to grab ALL followers: ")
        number = int(input("Number to filter subscribers: "))
        nl_actions.filter(username, number)

    if action_numb == 8:
        actions = Actions()
        actions.follow_actual_users()

    del actions
