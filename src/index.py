import datetime
import tkinter as tk
from tkinter import ttk
from tkinter.constants import DISABLED
from tkinter import Tk, Canvas, Frame, BOTH, LAST

if __name__ == "src.index":
    import src.actions as actions
    import src.config as config

if __name__ == "__main__":
    import actions
    import config


def gui_menu():

    def working_day(event):
        if 'disabled' in comboBox.state():
            print("Can to work")

    win = tk.Tk()
    icon = tk.PhotoImage(file=config.ICON_PATH)
    BACKGROUND_COLOR = "#E8EFF1"
    FONT_COLOR = "#202324"

    win.config(bg=BACKGROUND_COLOR)
    win.iconphoto(False, icon)
    win.title(f"INSTAGRAM AUTOMATION v{config.PROGRAM_VERSION}")
    win.geometry("320x400+200+100")
    win.resizable(False, False)

    usernames = config.get_all_usernames()
    if len(usernames) == 0:
        label_1 = tk.Label(win, text=f"Аккаунт не установлен",
                           bg=BACKGROUND_COLOR,
                           fg=FONT_COLOR,
                           pady=5,
                           padx=3)
        label_1.grid(column=0, row=0)
    elif len(usernames) == 1:
        label_1 = tk.Label(win, text=f"Аккаунт: {usernames[0]}",
                           bg=BACKGROUND_COLOR,
                           fg=FONT_COLOR,
                           pady=5,
                           padx=3)
        label_1.grid(column=0, row=0)
        config.set_account_variables(1)
    else:
        label_1 = tk.Label(win, text="Выберете аккаунт",
                           bg=BACKGROUND_COLOR,
                           fg=FONT_COLOR,
                           pady=5,
                           padx=3)
        label_1.grid(column=0, row=0)
        comboBox = ttk.Combobox(win, values=usernames)
        comboBox.current(0)
        comboBox.grid(column=0, row=1, ipady=2)

        apply_btn = tk.Button(text="Применить",
                              command=lambda: comboBox.config(state=DISABLED))
        apply_btn.grid(column=1, row=1, padx=5)

    c = Canvas(win, width=250, height=20, bg=BACKGROUND_COLOR, highlightthickness=0, relief='ridge')
    c.grid(column=0, row=2, columnspan=2)
    c.create_line(10, 10, 250, 10, dash=(4,2))
    
    work_btn = tk.Button(text="Рабочий день")
    work_btn.grid(column=0, row=3, padx=5, sticky="w")
    work_btn.bind('<Button-1>', working_day)

    win.mainloop()


def menu():
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

    # main()
    gui_menu()
