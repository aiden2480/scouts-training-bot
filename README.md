# :robot: Scouts Training Bot
A script written in Python with Selenium to log in to the scouts training website and automatically complete all training modules, watch all videos, open all required documents, and take all tests.

<div align="center">
    <img src="https://img.shields.io/github/last-commit/aiden2480/scouts-training-bot?color=yellow" alt="Last commit" />
    <img src="https://img.shields.io/github/license/aiden2480/scouts-training-bot" alt="Licence" />
    <img src="https://img.shields.io/github/languages/code-size/aiden2480/scouts-training-bot" alt="Code size" />
</div>

## :running: Run via executable
Ensure you have Google Chrome installed before running. Then, download the [Scouts Training Bot latest release](https://github.com/aiden2480/scouts-training-bot/releases/latest) and run it. Once the login screen for the training portal appears, enter your credentials and sign in.

<img src=".github/screenshots/login.png" alt="Login" />

The program will run the training curriculum that is currently selected. To change this, login and scroll to the bottom of the index page, then click `Set as My Training` under the desired curriculum.

<div align="center">
    <img src=".github/screenshots/setasmytraining.png" alt="Set as My Training" />
    <img src=".github/screenshots/mytraining.png" alt="My Training" />
</div>

## :snake: Run via Python
```
$ pip install -r requirements.txt
$ python main.py
```

You can also optionally add a `.env` file in the root directory, or next to the executable to provide credentials to login with, rather than having to manually sign into the browser. 

| Property   | Description                                |
|------------|--------------------------------------------|
| `branch`   | The two or three letter code of the branch |
| `username` | Your username for Scouts Training          |
| `password` | Your password for Scouts Training          |

## :outbox_tray: Screenshots
<img src=".github/screenshots/youth.png" alt="Youth already completed training" />
<img src=".github/screenshots/group1.png" alt="Completing group leader training 1" />
<img src=".github/screenshots/group2.png" alt="Completing group leader training 2" />
