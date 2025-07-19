<div align="center">

# MEROSHARE BOT

[![Playwright](https://img.shields.io/pypi/v/playwright.svg)](https://pypi.python.org/pypi/playwright)
[![License Badge](https://img.shields.io/github/license/tprototype/meroshare-bot?color=2b9348)](https://github.com/tprototype/meroshare-bot/blob/master/README.md)
[![Releases](https://img.shields.io/badge/version-0.0.1-blue)](https://github.com/tprototype/meroshare-bot/releases)
<img src="https://komarev.com/ghpvc/?username=Sagar-Timalsena&label=Repo%20views&color=brightgreen&style=flat&repo=MeroShare-Bot" alt="Repo views" />
</div>


**This is meroshare bot, which will auto apply IPO of different company which are open.**

## Get Started

To get started, you need to download this project or can clone this repo on your machine.
And you can simply run the main.py file. But before that you need to setup the environment.

### 1. Install the dependencies

```
pip install --upgrade pip

pip install -r requirments.txt
# or
python3 -m pip install -r requirements.txt
```

### 🌐 2. Run following code in the terminal

```
pip install playwright
playwright install chromium

```

### 📝 3. Edit demats.json file to setup your information in the serial order as given

```
[
  {
    "name": "Ram Bahadur",
    "dp_id": "130123",
    "username": "ram123",
    "password": "ram@123",
    "preferred_bank": "NMB BANK LTD.",
    "kitta": "10",
    "crn": "CRN12345678",
    "txn_pin": "1111"
  },
  {
    "name": "Sita Kumari",
    "dp_id": "130456",
    "username": "sita456",
    "password": "sita@456",
    "preferred_bank": "NIC ASIA BANK LTD.",
    "kitta": "20",
    "crn": "CRN87654321",
    "txn_pin": "2222"
  }
  ]


```

### 4. Now just run main.py file to run the script

```
python main.py
# or
python3 main.py
```

### 🌟 Support the Project
If you find this project helpful, consider giving it a ⭐ on GitHub to show your support!
