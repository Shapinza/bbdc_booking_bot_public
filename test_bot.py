from bot import *
from config import load_config

config = load_config("config.yaml")
bot_token = config["telegram"]["token"]
chat_id = config["telegram"]["chat_id"]
send_message("test", bot_token, chat_id)
