import helpers
import processes

# Setup
creds = helpers.get_creds()
browser = helpers.create_webdriver()

# Pre-processing steps
helpers.get_index_page(browser)
helpers.login_if_creds_provided(browser)
helpers.wait_for_curriculumns_index_page(browser)
helpers.navigate_to_modules_index_page(browser)

# Sequentially process each module
uncompleted_modules = helpers.get_uncompleted_modules(browser)

for module in uncompleted_modules:
    processes.process_module(browser, module)

# Go back to main page, we're done
helpers.get_index_page(browser)
