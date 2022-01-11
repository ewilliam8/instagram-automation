import os
import sys
import json
import src.config as config
from os import path
from io import open as io_open
from dotenv import load_dotenv

here = path.abspath(path.dirname(__file__))

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
path_to_storage = os.path.join(here + "\\src\\manager")
path_to_storage_username = os.path.join(
    path_to_storage + "\\" +
    str(os.getenv("INSTA_USERNAME")) + "\\")
interacted_file_path = path_to_storage_username + config.INTERACTED_FILE
parse_folder__path = path_to_storage_username + config.PARSE_FOLDER
filter_folder_path = path_to_storage_username + config.FILTER_FOLDER
manager_file_path = path_to_storage_username + config.MANAGER_FILE
accounts_file_path = os.path.join(here + "\\src\\" + config.ACCOUNTS_FILE)


def readall(*args):
    with io_open(path.join(here, *args), encoding="utf-8") as fp:
        return fp.read()


if not sys.version_info.major and sys.version_info.minor:
    print("Python 3.9.7 or higher is required.")
    print("You are using Python {}.{}.{}".format(
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro))
    exit()

# - - - FOLDERS - - -
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

if not os.path.exists(path_to_storage):
    os.mkdir(path_to_storage)

if not os.path.exists(path_to_storage_username):
    os.mkdir(path_to_storage_username)

if not os.path.isdir(parse_folder__path):
    os.mkdir(parse_folder__path)

if not os.path.isdir(filter_folder_path):
    os.mkdir(filter_folder_path)

# - - - FILES - - -
if not os.path.exists(interacted_file_path):
    open(interacted_file_path, "w", encoding='UTF-8').close()

if not os.path.exists(manager_file_path):
    with open(manager_file_path, "w", encoding='UTF-8') as file_manager:

        donor_accounts = []
        for account in config.target_accaunts:
            donor_accounts.append({
                "username": account,
                "count_followers": None,
                "date": None
            })

        data = {
            "PROGRAM_VERSION": config.PROGRAM_VERSION,
            "donor_accounts": donor_accounts,
            "actual_interacted": []
            # "messaged": [],
            # "buyed": []
        }
        json.dump(data, file_manager, indent=4)

with open("requirements.txt") as f:
    dependencies = f.read().splitlines()

# - - - SET ACCOUNT(S) - - -
if not os.path.exists(accounts_file_path):
    with open(accounts_file_path, "w", encoding='UTF-8') as accounts_file:
        print("INSTAGRAM AUTOMATION - SETUP\n")
        DATA = []

        count_accounts = "None"
        while not count_accounts.isdigit():
            count_accounts = input("How many accounts do you want to input?: ")
        count_accounts = int(count_accounts)
        print()

        for user in range(0, count_accounts):
            print(f"|>  Input of data for User {user + 1} is open")

            # LOGIN, PASSWORD, KEY
            INSTA_USERNAME = input("INSTAGRAM USERNAME:\t")
            INSTA_PASSWORD = input("INSTAGRAM PASSWORD:\t")
            KEY = input("INSTAGRAM AUTOMATION KEY:\t")
            print()

            # PROXY
            is_proxy = input("Do you use proxy [Y/n]: ")
            if is_proxy == 'Y' or \
               is_proxy == 'y':
                PROXY_IP = input("PROXY IP:\t")
                PROXY_PORT = input("PROXY PORT:\t")
                PROXY_LOGIN = input("PROXY LOGIN:\t")
                PROXY_PASSWORD = input("PROXY PASSWORD:\t")
            else:
                PROXY_IP = None
                PROXY_PORT = None
                PROXY_LOGIN = None
                PROXY_PASSWORD = None
            print()

            # TARGET ACCOUNTS
            TARGET_ACCOUNTS = []
            count_target_accounts = "None"
            while not count_target_accounts.isdigit():
                count_target_accounts = input(
                    "How many target accounts do you want to input?: ")
            count_target_accounts = int(count_target_accounts)

            for ta in range(0, count_target_accounts):
                print("Input target account " +
                      f"[{ta+1}/{count_target_accounts}]: ", end="")
                TARGET_ACCOUNTS.append(input())

            DATA.append({
                "INSTA_USERNAME": INSTA_USERNAME,
                "INSTA_PASSWORD": INSTA_PASSWORD,
                "KEY": KEY,
                "PROXY_IP": PROXY_IP,
                "PROXY_PORT": PROXY_PORT,
                "PROXY_LOGIN": PROXY_LOGIN,
                "PROXY_PASSWORD": PROXY_PASSWORD,
                "TARGET_ACCOUNTS": TARGET_ACCOUNTS
            })

            print(f"|>  Input of data for User {user + 1} is closed\n\n")

        json.dump(DATA, accounts_file, indent=4)


documentation = readall("README.md")
print(documentation)
