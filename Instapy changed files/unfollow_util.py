import time

def get_actual_user_followers(
    browser,
    user_name,
    logger,
):
    """
    For the given username, follow who they follows.

    :param browser: webdriver instance
    :param user_name: given username of account to follow
    :param logger: the logger instance
    :return: list of actual user's following
    """

    usernames_index = 1
    usernames = []
    user_name = user_name.strip().lower()

    def find_names(index):
        for _ in range(0, 12):
            usernames.append(browser.find_element_by_xpath(
                f"/html/body/div[1]/section/main/div/ul/div/li[{index}]/div/div[1]/div[2]/div[1]/a").get_attribute("textContent"))
            index += 1

    user_link = "https://www.instagram.com/{}/".format(user_name)
    web_address_navigator(browser, user_link)

    if not is_page_available(browser, logger):
        return [], []

    try:
        # followers button
        browser.find_element_by_xpath("/html/body/div[1]/section/main/div/ul/li[2]").click()
        time.sleep(random.randint(2, 5))

    except NoSuchElementException as nsee:
        print("NoSuchElementException")
        print(nsee)
        return [], []

    find_names(usernames_index)
    usernames_index += 12
    find_names(usernames_index)
    usernames_index += 12

    for _ in range(0, 5):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(3, 6))

        find_names(usernames_index)
        usernames_index += 12

    # remove duplicates
    index = 1
    while index < len(usernames):
        if usernames[index] in usernames[ : index]:
            usernames.pop(index)
        else:
            index += 1

    return usernames