import os
import sys
import json
from os import path
from src.config import *
from io import open as io_open
from setuptools import setup
from dotenv import load_dotenv
here = path.abspath(path.dirname(__file__))

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
path_to_storage = os.path.join(here + "\\src\\manager")
path_to_storage_username = os.path.join(
    path_to_storage + "\\" +
    os.getenv("INSTA_USERNAME"))
interacted_file_path = path_to_storage_username + "\\" + INTERACTED_FILE
parse_folder__path = path_to_storage_username + "\\" + PARSE_FOLDER
filter_folder_path = path_to_storage_username + "\\" + FILTER_FOLDER
manager_file_path = path_to_storage_username + "\\" + MANAGER_FILE


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

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

if not os.path.exists(path_to_storage):
    os.mkdir(path_to_storage)

if not os.path.exists(path_to_storage_username):
    os.mkdir(path_to_storage_username)

if not os.path.exists(interacted_file_path):
    open(interacted_file_path, "w", encoding='UTF-8').close()

if not os.path.isdir(parse_folder__path):
    os.mkdir(parse_folder__path)

if not os.path.isdir(filter_folder_path):
    os.mkdir(filter_folder_path)

if not os.path.exists(manager_file_path):
    with open(manager_file_path, "w", encoding='UTF-8') as file_manager:
        data = {
            os.getenv("INSTA_USERNAME"):
            {
                "INSTA_USERNAME": "",
                "INSTA_PASSWORD": "",
                "donor_accounts": [],
                "statistic": []
                # "messaged": [],
                # "buyed": []
            }
        }
        json.dump(data, file_manager, indent=4)

with open("requirements.txt") as f:
    dependencies = f.read().splitlines()

# setup(
#     name="instapy extended",
#     version="1.0",
#     install_requires=dependencies
# )

documentation = readall("README.md")
print(documentation)
