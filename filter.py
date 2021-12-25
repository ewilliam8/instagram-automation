import sys
import time
import random
import requests
from config import *
from bs4 import BeautifulSoup


def check_user(username, skip_words=[],
               non_skip_business_categories=[],
               skip_private=True
               ):

    min_followers = 50
    max_followers = 10000
    min_following = 50
    max_following = 10000
    min_posts = 1
    max_posts = 2000

    def find_nth(haystack, needle, n):
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start+len(needle))
            n -= 1
        return start

    print(f"\n--> Checking {username}")

    # check by username
    for skip_word in skip_name_keywords:
        if username.find(skip_word) != -1:
            print(f"× The user has a name with: {skip_word}")
            return None

    # check with already interacted users
    interacted_users = open(INTERACTED_FILE,
                            'r', encoding='UTF-8').readlines()
    for index, elem in enumerate(interacted_users, start=0):
        interacted_users[index] = elem[:-1]

    if username in interacted_users:
        print(f"× The user has been already interacted")
        return None

    # --- SERVER CALL ---
    url = f'https://www.instagram.com/{username}/'
    headers = {'user-agent': 'Chrome/62.0.3202.84'}
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    follows_name_posts = str(soup.find_all("meta")[13])

    bio_and_desc = str(soup.find_all("script"))
    bio_and_desc = bio_and_desc.encode("utf-16", "surrogatepass") \
                               .decode("utf-16", "surrogatepass")
    bio_and_desc_extra = bio_and_desc[
        bio_and_desc.find('biography'):
        bio_and_desc.find('blocked_by_viewer')][12:-3]
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
    name = str(follows_name_posts.split(" ")[14:-2])[1:-1]\
        .replace("'", '').replace(',', '') \
        .encode("utf-16", "surrogatepass") \
        .decode("utf-16", "surrogatepass")
    biography = bio_and_desc[
        bio_and_desc.find("biography") + 12:
        bio_and_desc.find("blocked_by_viewer") - 3] \
        .encode("utf-16", "surrogatepass") \
        .decode("utf-16", "surrogatepass")
    biography_extra = bio_and_desc_extra

    # Ограничения по подписчикам, подпискам и кол-во постов
    if followers < min_followers or followers > max_followers:
        print(f"× The user has unacceptable amount of followers: {followers}")
        return None

    if following < min_following or following > max_following:
        print(f"× The user has unacceptable amount of following: {following}")
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
        word = str(word.encode("unicode_escape")).replace('\\\\', '\\')[2:-1]

        if name.find(word) != -1:
            print(f"× User skipped by keyword in Name: {word_to_print}")
            return None

        if biography.find(word) != -1:
            print(f"× User skipped by keyword in Bio: {word_to_print}")
            return None

        if biography_extra.find(word) != -1:
            print(f"× User skipped by keyword in Bio: {word_to_print}")
            return None

    print("✓ Added to a list")
    return username


def filter_base(to_filter=9):
    for gi in range(0, to_filter):

        accounts_to_check = []
        exception_occurred = 0
        with open(PARSE_FOLDER + account + '_followers.txt',
                  'r', encoding='UTF-8') as f:
            userslist = f.readlines()
            for _ in range(0, 10):
                user = userslist.pop(0).replace('\n', '')
                accounts_to_check.append(user)
            with open(PARSE_FOLDER + account + '_followers.txt',
                      'w', encoding='UTF-8') as F:
                F.writelines(userslist)

        filtered_accounts = []
        for username in accounts_to_check:

            local_check_user = None
            try:
                local_check_user = check_user(username,
                                              skip_bio_keyword,
                                              person_categories,
                                              False)
            except Exception as ex:
                exception_occurred += 1
                print("An exception occurred")

                if exception_occurred >= 5:
                    print("\n\nSome problems with Instagram!\n")
                    print("Close the program\n")
                    sys.exit(1)
                    break

            if local_check_user is not None:
                filtered_accounts.append(local_check_user)
                print(filtered_accounts)

            time.sleep(random.randint(1, 5))

        with open(FILTER_FOLDER + account + '_filtered.txt',
                  'a', encoding='UTF-8') as f:

            for el in filtered_accounts:
                f.write(el + "\n")

        print(f"\n~~ Users checked [{(gi + 1) * 10}/{to_filter * 10}]")
        print("~~ Sleeping between 1 and 5 minutes")
        time.sleep(random.randint(60, 300))


if __name__ == "__main__":
    filter_base()
