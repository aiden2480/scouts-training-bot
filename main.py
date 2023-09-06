import os

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from helpers import (create_webdriver, determine_object_type, get_creds,
                     get_cwd, is_object_required)


# Process module from a link
def process_module(module_link: str) -> None:
    """
        Accepts a module link and navigates to that webpage,
        locates mandatory training, and marks it as completed.
    """

    browser.get(module_link)
    container = browser.find_element(By.CLASS_NAME, "module-page-container")
    module_name = container.find_element(By.TAG_NAME, "h1").text
    print(f"\n[MODULE] Traversing module {module_name!r}")

    # Determine which objects are have already been completed
    all_objects = browser.find_element(By.CLASS_NAME, "learning-object-list")
    uncompleted = all_objects.find_element(By.XPATH, "*[1]")
    h5 = uncompleted.find_elements(By.TAG_NAME, "h5")
    already_completed = []

    for header in h5:
        try:
            header.find_element(By.TAG_NAME, "img")
            already_completed.append(header.text.strip())
        except NoSuchElementException:
            continue

    # Find required objects and remove already completed ones
    objects = browser.find_elements(By.CLASS_NAME, "learning_object")
    required_maybe_completed = filter(is_object_required, objects)
    uncompleted = []

    for object in required_maybe_completed:
        title = object.find_element(By.CLASS_NAME, "title-text").text.strip()
        
        if title not in already_completed:
            uncompleted.append(object)
        else:
            print(f"[MODULE] Skipping completed object {title!r}")

    # For video and document objects, we can simply send a request to the API
    # to mark the object as complete, but for emodules, we need to access the
    # page to process further information
    emodules = []
    for object in uncompleted:
        if determine_object_type(object) == "video":
            name = object.find_element(By.CLASS_NAME, "title-text").text
            print(f"[MODULE] Marking video {name!r} complete")

            mark_video_complete(object)

        if determine_object_type(object) == "emodule":
            parent = object.find_element(By.CLASS_NAME, "emodule-object")
            href = parent.find_element(By.TAG_NAME, "a")
            name = object.find_element(By.CLASS_NAME, "title-text").text
            print(f"[MODULE] Enqueuing emodule {name!r}")

            link = "https://training.scouts.com.au" + href.get_attribute("data-url")
            emodules.append((name, link)) # Queue for processing

        if determine_object_type(object) == "document":
            name = object.find_element(By.CLASS_NAME, "title-text").text
            print(f"[MODULE] Marking document {name!r} complete")

            mark_document_complete(object)
    
    # Now all emodule links need to be opened and processed
    for name, link in emodules:
        print(f"[MODULE] Marking emodule {name!r} as complete")
        browser.get(link)

        with open(os.path.join(get_cwd(), "js/emod.js")) as fp:
            browser.execute_script(fp.read())
    
    # Check if post module test exists
    try:
        pte = browser.find_element(By.XPATH, "//img[@title='post-test exam']")
    except NoSuchElementException:
        print("[MODULE] No post-module exam required")
        return
    
    try:
        pte.find_element(By.XPATH, "../../../../*[1]/img")
    except NoSuchElementException:
        print("[MODULE] Opening post-module exam")
        pte.click()

        # Wait until the exam has loaded
        cond = EC.presence_of_element_located((By.CLASS_NAME, "public-exam-block"))
        WebDriverWait(browser, 10, 0.1).until(cond)

        complete_postmod_quiz(browser.current_url)
    else:
        print("[MODULE] Skipping completed post-module exam")

def mark_video_complete(obj: WebElement) -> None:
    video = obj.find_element(By.CLASS_NAME, "video-object")
    objid = video.get_attribute("data-object-id")
    
    with open(os.path.join(get_cwd(), "js/video.js")) as fp:
        browser.execute_script(fp.read(), objid)

def mark_document_complete(obj: WebElement) -> None:
    document = obj.find_element(By.CLASS_NAME, "document-object")
    objid = document.get_attribute("data-object-id")

    with open(os.path.join(get_cwd(), "js/document.js")) as fp:
        browser.execute_script(fp.read(), objid)

def complete_postmod_quiz(quiz_link: str, possible_answers = None) -> None:
    browser.get(quiz_link)

    if not possible_answers:
        possible_answers = {}

    # Extract possible questions and answers
    container_elem = browser.find_element(By.CLASS_NAME, "public-exam-block")
    questions_elems = container_elem.find_elements(By.CLASS_NAME, "question-column")

    for question in questions_elems:
        id = question.find_element(By.ID, "questions_").get_attribute("value")
        answers_elems = question.find_elements(By.CLASS_NAME, "exam_answer")

        if id in possible_answers:
            continue

        possible_answers[id] = []
        for answer in answers_elems:
            possible_answers[id].append(answer.get_attribute("value"))

    with open(os.path.join(get_cwd(), "js/postmodquiz.js")) as fp:
        completed_url = browser.execute_script(fp.read(), possible_answers)
    
    browser.get(completed_url)
    with open(os.path.join(get_cwd(), "js/extractpostmod.js")) as fp:
        completed, possible_answers = browser.execute_script(fp.read(), possible_answers)

    if not completed:
        correct = len([i for i in possible_answers.values() if len(i) == 1])
        total = len(possible_answers)

        print(f"[EXAM] {correct}/{total} exam questions correct")
        complete_postmod_quiz(quiz_link, possible_answers)
    else:
        print("[EXAM] Exam pass mark achieved")

creds = get_creds()
browser = create_webdriver()
browser.get("https://training.scouts.com.au")

if creds:
    browser.find_element(By.ID, "branch").send_keys(creds["branch"])
    browser.find_element(By.ID, "number").send_keys(creds["username"])
    browser.find_element(By.ID, "password").send_keys(creds["password"])
    browser.find_element(By.ID, "login-submit").click() # TODO incorrect login details check
else:
    print("Please login to the portal webpage")
    url_equals_homepage = EC.url_to_be("https://training.scouts.com.au/curriculums/index")
    WebDriverWait(browser, float("inf"), 0.1).until(url_equals_homepage)

# Determine which modules need to be completed
my_training = browser.find_element(By.CLASS_NAME, "curriculum-summary-container")
my_training.find_element(By.XPATH, "./*").click() # It's all on the same page, so we can just click the first element
uncompleted_modules = []

for module in browser.find_elements(By.CLASS_NAME, "learning-module"):
    name = module.find_element(By.CLASS_NAME, "module-name").text
    link = module.find_element(By.XPATH, "..").get_attribute("href")
    image = module.find_element(By.TAG_NAME, "img")
    src = image.get_attribute("src")

    if "coming-soon" in src: # Module is unavailable
        print("[INDEX] Skipping unavailable", name)
        continue
    
    if "checked-green" in src: # Module is already completed
        print("[INDEX] Skipping completed  ", name)
        continue
    
    print("[INDEX] Uncompleted module  ", name)
    uncompleted_modules.append((name, link))

for name, link in uncompleted_modules:
    final_module_quiz_required = process_module(link)

# Go back to main page
browser.get("https://training.scouts.com.au")
my_training = browser.find_element(By.CLASS_NAME, "curriculum-summary-container")
my_training.find_element(By.XPATH, "./*").click()
