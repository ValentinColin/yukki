import os
import yaml
from dotenv import load_dotenv

# Chargements des varaibles d'environnement dans via le fichier .env
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

PREFIX = "."  # prefix des commandes discord

def get_prefix(bot, msg):
    """Renvoie le prefix en fonction sur server"""
    with open("data/yaml/bot.yml") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    if "prefix" in data["servers"][str(msg.guild.id)]:
        prefix = data["servers"][str(msg.guild.id)]["prefix"]
    else:
        prefix = PREFIX
    return prefix

my_id = 283649186446966784  # Call_me_Valou
masters_id = [my_id]

path_todo_list = "data/md/TODO.md"
path_todo_json = "data/json/TODO.json"
