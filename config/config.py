import os
import yaml
import discord
from dotenv import load_dotenv

# Chargements des varaibles d'environnement dans via le fichier .env
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

PREFIX = "."  # prefix des commandes discord

def get_prefix(bot, msg):
    """Renvoie le prefix en fonction sur server"""
    if type(msg.channel) is discord.TextChannel: # channel textuel de server
        id_server = str(msg.guild.id)
        with open("data/yaml/bot.yml") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        if id_server not in data["servers"]:
            with open("data/yaml/bot.yml") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
            with open("data/yaml/bot.yml", "w") as f:
                # Création du serveur à partir du model 'default'
                data["servers"][id_server] = data["servers"]["default"]
                yaml.dump(data, f)
        prefix = data["servers"][id_server]["prefix"]
    else: # message privée (groupé ou non)
        prefix = PREFIX
    return prefix

my_id = 283649186446966784 # Call_me_Valou
# marc_id = 478552571510915072 # Marc Partensky
# masters_id = [my_id]

path_todo_list = "data/md/TODO.md"
path_todo_json = "data/json/TODO.json"
