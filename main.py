# import os
# from config import *
import datetime
import unfollow
import config
import filter
import follow
import feed
import sys


# TODO
# Autostart the program
# UI
# Код для работы на 28 дней +-
# Проверить прокси


def day_type_one():
    print("Подписка")
    follow.follow()


def day_type_two():
    print("Фильтрация")
    filter.filter_base()


def day_type_three():
    print("Отписка")
    unfollow.unfollow()


def day_type_four():
    print("Лайкинг новостей и просмотр сториз")
    feed.feed_interact()


if __name__ == "__main__":

    time_now = datetime.datetime.now()
    day_of_month = time_now.strftime("%d")
    time_stop = datetime.datetime(2022, 1, 26)
    today_date = time_now.strftime("%d/%m/%Y").replace("/", ".")

    if time_now < time_stop:
        delta_str = str(time_stop - time_now).replace("day,", "день,") \
                                             .replace("days,", "дней,")
        delta_str = delta_str[:delta_str.find(".")]
        print("Автоматизация Инстаграм")
        print("Версия: " + config.PROGRAM_VERSION)
        print("Сегодня: " + time_now, end='')
        print(". У Вас осталось оплаченного времени: " + delta_str)
    else:
        print("У вас не осталось оплаченных дней")
        input("Закройте программу")
        sys.exit(1)

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
