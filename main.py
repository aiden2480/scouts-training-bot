import helpers
import processes
import rich

# Setup
console = rich.get_console()

with console.status("Loading webdriver"):
    creds = helpers.get_creds()
    browser = helpers.create_webdriver()

with console.status("Waiting for successful login"):
    helpers.get_index_page(browser)
    helpers.login_if_creds_provided(browser)
    helpers.wait_for_curriculumns_index_page(browser)

with console.status("Navigating to modules index page"):
    helpers.navigate_to_modules_index_page(browser)

# Sequentially process each module
uncompleted_modules = helpers.get_uncompleted_modules(browser)

for module in uncompleted_modules:
    processes.process_module(browser, module)

# Go back to main page, we're done
helpers.get_index_page(browser)

console.print()
console.rule("[orange1]Finished[/]")
console.print(" - If some post-module quizes have been missed, try running the program again.")
console.print(" - To run the program on a different curriculum, click the corresponding [cyan]Set as My Training[/] button on the index page")
console.print(" - [green]Have a nice day :D[/]")
console.input("\n[grey46]Press enter to exit...[/]")
