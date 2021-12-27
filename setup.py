import os
import sys
import json
from os import path
from config import *
from io import open as io_open
from setuptools import setup
from dotenv import load_dotenv
here = path.abspath(path.dirname(__file__))

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
interacted_file_path = os.path.join(os.path.dirname(__file__), INTERACTED_FILE)


def readall(*args):
    with io_open(path.join(here, *args), encoding="utf-8") as fp:
        return fp.read()


# доделать сравнение версий с минимальной версией 3.10
if not sys.version_info.major and sys.version_info.minor:

    print("Python 3.9.7 or higher is required.")
    print("You are using Python {}.{}.{}".format(sys.version_info.major,
                                                 sys.version_info.minor,
                                                 sys.version_info.micro))
    sys.exit(1)

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

if not os.path.exists(interacted_file_path):
    open(INTERACTED_FILE, "w", encoding='UTF-8').close()
if not os.path.isdir(PARSE_FOLDER):
    os.mkdir(PARSE_FOLDER)
if not os.path.isdir(FILTER_FOLDER):
    os.mkdir(FILTER_FOLDER)


with open(MANAGER_FILE, "w", encoding='UTF-8') as file_manager:
    data = {
        os.getenv("INSTA_USERNAME"): {
            "donor_accounts": [],
            "interacted_users": []

        }
    }
    json.dump(data, file_manager)

with open("requirements.txt") as f:
    dependencies = f.read().splitlines()

# setup(
#     name="instapy extended",
#     version="1.0",
#     install_requires=dependencies
# )

documentation = readall("README.md")
print(documentation)
