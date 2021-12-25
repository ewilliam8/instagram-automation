# import os
# from config import *
import datetime
import filter
import follow
import feed


# TODO
# Autostart the program
# UI
# Код для работы на 28 дней
# Проверить прокси


def day_type_one():
    print("Подписка")
    follow.follow()


def day_type_two():
    print("Фильтрация")
    filter.filter_base()


def day_type_three():
    print("Полный отдых")


def day_type_four():
    print("Лайкинг новостей и просмотр сториз")
    feed.feed_interact()


if __name__ == "__main__":
    time_now = datetime.datetime.now()
    # time_now = datetime.datetime(2019, 8, 9)
    day_of_month = time_now.strftime("%d")
    print(day_of_month)

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
