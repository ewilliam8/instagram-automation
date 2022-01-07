from logging import StrFormatStyle
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
statistics_file_path = path_to_storage_username + config.STATISTICS_FILE


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

if not os.path.exists(statistics_file_path):
    open(statistics_file_path, "w", encoding='UTF-8').close()

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
            "INSTA_USERNAME": os.getenv("INSTA_USERNAME"),
            "INSTA_PASSWORD": os.getenv("INSTA_PASSWORD"),
            "donor_accounts": donor_accounts,
            "actual_interacted": []
            # "messaged": [],
            # "buyed": []
        }
        json.dump(data, file_manager, indent=4)

with open("requirements.txt") as f:
    dependencies = f.read().splitlines()

documentation = readall("README.md")
print(documentation)
