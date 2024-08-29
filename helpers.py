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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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


def get_index_page(browser: Chrome):
    browser.get("https://training.scouts.com.au")


def login_if_creds_provided(browser: Chrome):
    creds = get_creds()

    if not creds:
        print("Please login to the portal webpage")
        return None

    browser.find_element(By.ID, "branch").send_keys(creds["branch"])
    browser.find_element(By.ID, "number").send_keys(creds["username"])
    browser.find_element(By.ID, "password").send_keys(creds["password"])
    browser.find_element(By.ID, "login-submit").click()


def wait_for_curriculumns_index_page(browser: Chrome):
    wait = WebDriverWait(browser, float("inf"), 0.1)
    url_equals_homepage = EC.url_to_be("https://training.scouts.com.au/curriculums/index")
    
    wait.until(url_equals_homepage)


def navigate_to_modules_index_page(browser: Chrome):
    # All the modules are on the same page, so we can just click the first one
    my_training = browser.find_element(By.CLASS_NAME, "curriculum-summary-container")
    my_training.find_element(By.XPATH, "./*").click()


def get_uncompleted_modules(browser: Chrome) -> list[Module]:
    modules = []

    for module_elem in browser.find_elements(By.CLASS_NAME, "learning-module"):
        name = module_elem.find_element(By.CLASS_NAME, "module-name").text
        link = module_elem.find_element(By.XPATH, "..").get_attribute("href")
        image = module_elem.find_element(By.TAG_NAME, "img")
        src = image.get_attribute("src")

        assert src is not None, f"Image does not have src tag for {name}"
        assert link is not None, f"Link was none for {name}"

        if "coming-soon" in src: # Module is unavailable
            print("[INDEX] Skipping unavailable", name)
            continue
        
        if "checked-green" in src: # Module is already completed
            print("[INDEX] Skipping completed  ", name)
            continue
        
        print("[INDEX] Uncompleted module  ", name)
        modules.append(Module(name, link))
    
    print("[INDEX] The following modules will now be processed:")
    print(" -", "\n - ".join(map(lambda m: f"{m.name} @ {m.link}", modules)))

    return modules
