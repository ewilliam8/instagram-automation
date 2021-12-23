import os
import json
from os import path
from config import *
from io import open as io_open
from setuptools import setup
from dotenv import load_dotenv
here = path.abspath(path.dirname(__file__))

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def readall(*args):
    with io_open(path.join(here, *args), encoding="utf-8") as fp:
        return fp.read()


# проверка на папки FILTER и PARSE
if not os.path.isdir(PARSE_FOLDER):
    os.mkdir(PARSE_FOLDER)
if not os.path.isdir(FILTER_FOLDER):
    os.mkdir(FILTER_FOLDER)

open(INTERACTED_FILE, "w", encoding='UTF-8').close()
with open(MANAGER_FILE, "w", encoding='UTF-8') as file_manager:
    data = {
        os.getenv("INSTA_USERNAME"): {
            "donor_accounts": [],
            
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
