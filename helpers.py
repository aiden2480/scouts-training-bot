import os
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Literal, Optional

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


@dataclass
class Module:
    name: str
    link: str


class Branch(Enum):
    NAT = "National"
    ACT = "Australian Capital Territory"
    NSW = "New South Wales"
    NT = "Northern Territory"
    QLD = "Queensland"
    SA = "South Australia"
    TAS = "Tasmania"
    VIC = "Victoria"
    WA = "Western Australia"
    INT = "International"


def get_cwd() -> str:
    if getattr(sys, "frozen", None) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS

    return os.getcwd()


def is_object_required(obj: WebElement) -> bool:
    """Determines whether an object is marked as mandatory training"""

    try:
        obj.find_element(By.CLASS_NAME, "required-icon")
    except NoSuchElementException:
        return False

    return True


def determine_object_type(obj: WebElement) -> Literal["video", "document", "emodule"]:
    """Determines whether a specified object is a video, document, or emodule"""

    types = ["video", "document", "emodule"]

    for objtype in types:
        try:
            obj.find_element(By.CLASS_NAME, f"{objtype}-object")
        except NoSuchElementException:
            continue
        else:
            return objtype

    raise ValueError("Object type not found")


def create_webdriver() -> Chrome:
    """Creates a webdriver with the given chromedriver version"""

    options = Options()

    options.add_argument("--mute-audio")
    options.add_argument("--log-level=3")
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    return Chrome(options=options)


def get_creds(env_file: str = ".env") -> Optional[dict]:
    is_valid = lambda i: i.count("=") == 1 and not i.startswith("#")

    if not os.path.isfile(env_file):
        return None

    with open(env_file) as fp:
        lines = [i for i in fp.readlines() if is_valid(i)]

    env = {}
    missing = []

    for line in lines:
        key, value = line.split("=")
        env[key.strip().lower()] = value.strip()

    if "branch" not in env:
        missing.append("branch")
    if "username" not in env:
        missing.append("username")
    if "password" not in env:
        missing.append("password")

    if len(missing):
        print("Not all required values passed: missing", ", ".join(missing))
        return None

    if not env["username"].isnumeric():
        print("Username is invalid")
        return None

    if env["branch"].upper() not in Branch.__members__:
        print("Branch must be one of", ", ".join(Branch.__members__))
        return None

    # Expand branch code and return
    env["branch"] = Branch[env["branch"].upper()].value

    return env
