## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This repo contains a Selenium bot for booking driving lessons at Bukit Batok Driving Center (BBDC) in Singapore. This bot works with the upgraded version of BBDC website launched in Dec 2022.

You can use this bot to check for available lesson slots and receive alerts on Telegram when new slots become available. In this way you wouldn't have to check the BBDC website manually to fight for newly opened slots or those cancelled by other people in the last minute.
This bot also allows a certain level of customization by modifying settings in the config file.

## Technologies
Project is created with:
* Python version: 3.10
* Selenium version: 4.7.2
* ChromeDriver version: 110.0.5481.30
	
## Setup
### Setting up local files
1. To run this project, download and unzip the released file.
2. Run `$ pip install -r requirements.txt` to install required packages.
3. Download a version of Chromedriver from https://chromedriver.chromium.org/downloads that suits your OS and chrome version.
4. Copy the full path to your downloaded Chromedriver file, and add it to `config.yaml` under `chromedriver`.
5. Add the username and password of your BBDC account to `config.yaml` under `bbdc`.

### Setting up Telegram bot
1. Search for BotFather and start a conversation with it.
2. Send /newbot to BotFather and follow the instructions to create a new Telegram bot.
3. Note down the Telegram bot's access token and add it to `config.yaml` under `telegram`.
4. Start a group chat and include your newly created into it.
5. Click on the chat group and check your web url. It should be in the format of "https://web.telegram.org/k/#-xxxxxxxxx" where each x is a number. Copy the part after '#' (not including the '#') to `config.yaml` under `telegram`.

### Running the bot
1. In command line, navigate to your project root and run
```
python main.py
```
2. Customization, such as search frequency, desired months etc., can be done by modifying settings in `config.yaml`. 
