import datetime

if __name__ == "src.index":
    import src.actions as actions
    import src.config as config

if __name__ == "__main__":
    import actions
    import config


def menu():
    print(f"INSTAGRAM AUTOMATION v{config.PROGRAM_VERSION}\n")

    count_usernames = config.get_all_usernames()
    if count_usernames != 1:
        account_number = input("Choose an account: ")
        config.set_account_variables(int(account_number))
    else:
        config.set_account_variables(1)
    # choose account -> [info - paid days] start, settings, back

    time_now = datetime.datetime.now()
    time_stop = datetime.datetime(2022, 1, 27)
    today_date = time_now.strftime("%d.%m.%Y")

    if time_now < time_stop:
        delta_str = str(time_stop - time_now).replace("day,", "день,") \
                                             .replace("days,", "дней,")
        delta_str = delta_str[:delta_str.find(".")]

        print("\nСегодня: " + today_date, end='')
        print(". У Вас осталось оплаченного времени: " + delta_str)
    else:
        print("У вас не осталось оплаченного времени")
        input("Закройте программу")
        exit()


def main():

    menu()

    time_now = datetime.datetime.now()
    day_of_month = time_now.strftime("%d")
    inst_actions = actions.Actions()
    # nologin_actions = actions.NoLoginActions()

    def day_type_one():
        print("Follow")
        inst_actions.follow_user_followers()

    def day_type_two():
        print("Filtering a base")
        # nologin_actions.filter()
        inst_actions.follow_user_followers()

    def day_type_three():
        print("Unfollowing")
        inst_actions.unfollow()

    def day_type_four():
        print("Liking feed")
        inst_actions.interact_by_feed()

    if day_of_month == "01" or \
       day_of_month == "20" or \
       day_of_month == "29":
        day_type_one()

    if day_of_month == "02" or \
       day_of_month == "06" or \
       day_of_month == "09" or \
       day_of_month == "11" or \
       day_of_month == "15" or \
       day_of_month == "17" or \
       day_of_month == "23" or \
       day_of_month == "25":
        day_type_two()
        day_type_three()

    if day_of_month == "03" or \
       day_of_month == "04" or \
       day_of_month == "05" or \
       day_of_month == "08" or \
       day_of_month == "10" or \
       day_of_month == "12" or \
       day_of_month == "14" or \
       day_of_month == "16" or \
       day_of_month == "18" or \
       day_of_month == "19" or \
       day_of_month == "22" or \
       day_of_month == "24" or \
       day_of_month == "26" or \
       day_of_month == "28" or \
       day_of_month == "30" or \
       day_of_month == "31":
        day_type_one()

    if day_of_month == "07" or \
       day_of_month == "13" or \
       day_of_month == "21" or \
       day_of_month == "27":
        day_type_two()
        day_type_four()

    del inst_actions
    # del nologin_actions


if __name__ == "__main__":

    main()
