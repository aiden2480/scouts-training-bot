# :robot: Scouts Training Bot
A script written in Python with Selenium to log in to the scouts training website and automatically complete all training modules, watch all videos, open all required documents, and take all tests.

<div align="center">
    <img src="https://img.shields.io/github/last-commit/aiden2480/scouts-training-bot?color=yellow" alt="Last commit" />
    <img src="https://img.shields.io/github/license/aiden2480/scouts-training-bot" alt="Licence" />
    <img src="https://img.shields.io/github/languages/code-size/aiden2480/scouts-training-bot" alt="Code size" />
</div>

## :key: Setup
Ensure you have Google Chrome installed before running. Run the following commands to install requirements and run the script. If you don't have Python installed, you can [download the latest release for windows](https://github.com/aiden2480/scouts-training-bot/releases/latest) instead.

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
