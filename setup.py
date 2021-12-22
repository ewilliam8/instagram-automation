import os
from os import path
from config import *
from io import open as io_open
from setuptools import setup
here = path.abspath(path.dirname(__file__))


def readall(*args):
    with io_open(path.join(here, *args), encoding="utf-8") as fp:
        return fp.read()


# проверка на папки FILTER и PARSE
if not os.path.isdir(PARSE_FOLDER):
    os.mkdir(PARSE_FOLDER)
if not os.path.isdir(FILTER_FOLDER):
    os.mkdir(FILTER_FOLDER)

open("interacted.txt", "w", encoding='UTF-8').close()

with open("requirements.txt") as f:
    dependencies = f.read().splitlines()

# setup(
#     name="instapy extended",
#     version="1.0",
#     install_requires=dependencies
# )

documentation = readall("README.md")
print(documentation)
