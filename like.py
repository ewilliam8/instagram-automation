from random import randint
from config  import *
from instapy import InstaPy
from instapy import smart_run
# from instapy import *     # 5526 стр.: len(links)

FILTER_FOLDER = "FILTER/"
PARSE_FOLDER  = "PARSE/"
account = "skycode_school"

session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=False,
                  bypass_security_challenge_using='sms')


target_accaunts = ["skycode_school"]
exclude_accaunts = []

# слияние списков
def merge(lst, res=[]):
    for el in lst:
        merge(el) if isinstance(el, list) else res.append(el)
    return res



with smart_run(session):

    target_followers = []
    file = FILTER_FOLDER + account + "_filtered.txt"
    f=open(file).readlines()
    for i in range(0, 25):
        user = f.pop(0).replace('\n', '')
        target_followers.append(user)
    
    with open(file,'w') as F:
        F.writelines(f)

    # взаимодействие: лайкинг и просмотр сториз
    session.set_dont_include(exclude_accaunts)
    session.set_mandatory_language(enabled=True, character_set=['LATIN', 'CYRILLIC'])
    session.set_simulation(enabled=True, percentage=66)
    session.set_skip_users(skip_private=True,
                        private_percentage=100,
                        skip_no_profile_pic=True,
                        no_profile_pic_percentage=100,
                        skip_business=True,
                        skip_non_business=False,
                        business_percentage=100,
                        skip_business_categories=[],
                        dont_skip_business_categories=person_categories,
                        skip_bio_keyword=skip_bio_keyword,
                        mandatory_bio_keywords=[])   # обязательные слова

    session.set_relationship_bounds(enabled=True,
                        # potency_ratio=1.34,
                        # delimit_by_numbers=True,
                        max_followers=8500,
                        max_following=4490,
                        min_followers=40,
                        min_following=40,
                        min_posts=1,
                        max_posts=2000)

    session.set_action_delays(enabled=True,
                        like=8,
                        comment=5,
                        follow=4.17,
                        unfollow=28,
                        story=10)

    session.set_quota_supervisor(enabled=True, 
                        sleep_after=["likes", "comments_d", "follows", "unfollows", "server_calls_h"], 
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

    session.set_do_story(enabled = True, percentage = 100, simulate = True)
    session.set_do_like(True, percentage=95)
    session.interact_by_users(target_followers, amount=1, randomize=True, media='Photo')









