import os
from typing import Any

from rich import get_console
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import helpers


# Constants
EXAM_BLOCK_LOCATOR = (By.CLASS_NAME, "exam-container")
console = get_console()


def process_module(browser: Chrome, module: helpers.Module):
    """
        Accepts a module link and navigates to that webpage,
        locates mandatory training, and marks it as completed.
    """

    console.print()
    console.rule(f"Traversing module [green]{module.name}[/]", )
    browser.get(module.link)

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
    required_maybe_completed = filter(helpers.is_object_required, objects)
    uncompleted = []

    for object in required_maybe_completed:
        title = object.find_element(By.CLASS_NAME, "title-text").text.strip()
        
        if title not in already_completed:
            uncompleted.append(object)
        else:
            console.print(f"Skipping completed object [grey46]{title}[/]")

    # For video and document objects, we can simply send a request to the API
    # to mark the object as complete, but for emodules, we need to access the
    # page to process further information
    emodules = []
    for object in uncompleted:
        if helpers.determine_object_type(object) == "video":
            name = object.find_element(By.CLASS_NAME, "title-text").text
            console.print(f"Marking video [blue]{name}[/] complete")

            mark_video_complete(browser, object)

        if helpers.determine_object_type(object) == "emodule":
            parent = object.find_element(By.CLASS_NAME, "emodule-object")
            href = parent.find_element(By.TAG_NAME, "a")
            name = object.find_element(By.CLASS_NAME, "title-text").text
            console.print(f"Enqueuing emodule [blue]{name}[/]")

            link = "https://training.scouts.com.au" + href.get_attribute("data-url")
            emodules.append((name, link)) # Queue for processing

        if helpers.determine_object_type(object) == "document":
            name = object.find_element(By.CLASS_NAME, "title-text").text
            console.print(f"Marking document [blue]{name}[/] complete")

            mark_document_complete(browser, object)
    
    # Now all emodule links need to be opened and processed
    for name, link in emodules:
        console.print(f"Marking emodule [blue]{name}[/] as complete")
        mark_emodule_complete(browser, link)
    
    # Check if post module test exists
    try:
        pte = browser.find_element(By.XPATH, "//img[@title='post-test exam']")
    except NoSuchElementException:
        console.print("[grey46]No post-module exam required[/]")
        return
    
    try:
        pte.find_element(By.XPATH, "../../../../*[1]/img")
    except NoSuchElementException:
        console.print("Opening [orange1]post-module exam[/]")
        pte.click()

        # Wait until the exam has loaded
        cond = EC.presence_of_element_located(EXAM_BLOCK_LOCATOR)
        WebDriverWait(browser, 10, 0.1).until(cond)

        complete_postmod_quiz(browser, browser.current_url)
    else:
        console.print("[grey46]Skipping completed post-module exam[/]")

def mark_video_complete(browser: Chrome, obj: WebElement):
    video = obj.find_element(By.CLASS_NAME, "video-object")
    objid = video.get_attribute("data-object-id")
    
    execute_js(browser, "js/video.js", objid)

def mark_document_complete(browser: Chrome, obj: WebElement):
    document = obj.find_element(By.CLASS_NAME, "document-object")
    objid = document.get_attribute("data-object-id")

    execute_js(browser, "js/document.js", objid)

def mark_emodule_complete(browser: Chrome, link: str):
    browser.get(link)

    execute_js(browser, "js/emod.js")

def execute_js(browser: Chrome, src: str, *args) -> Any:
    with open(os.path.join(helpers.get_cwd(), src)) as fp:
        return browser.execute_script(fp.read(), *args)

def complete_postmod_quiz(browser: Chrome, quiz_link: str, possible_answers = None):
    browser.get(quiz_link)

    if not possible_answers:
        possible_answers = {}

    # Extract possible questions and answers
    container_elem = browser.find_element(*EXAM_BLOCK_LOCATOR)
    questions_elems = container_elem.find_elements(By.CLASS_NAME, "question-column")

    for question in questions_elems:
        id = question.find_element(By.ID, "questions_").get_attribute("value")
        answers_elems = question.find_elements(By.CLASS_NAME, "exam_answer")

        if id in possible_answers:
            continue

        possible_answers[id] = []
        for answer in answers_elems:
            possible_answers[id].append(answer.get_attribute("value"))

    completed_url = execute_js(browser, "js/postmodquiz.js", possible_answers)
    
    browser.get(completed_url)
    completed, possible_answers = execute_js(browser, "js/extractpostmod.js", possible_answers)

    if not completed:
        correct = len([i for i in possible_answers.values() if len(i) == 1])
        total = len(possible_answers)

        console.print(f"[red]{correct}/{total}[/] exam questions correct")
        complete_postmod_quiz(browser, quiz_link, possible_answers)
    else:
        console.print("[green]Exam pass mark achieved[/]")
