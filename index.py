import discord
import os
import logging
import sqlite3
import signal
import sys
import atexit

from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from dbHandler import DbHandler

load_dotenv()
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
db = DbHandler()

def shutdown_handler(signum, frame):
    print('shuting down, closing db...')
    db.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler) #ctrl-c
signal.signal(signal.SIGTERM, shutdown_handler) #docker stop

@atexit.register
def cleanup():
    try:
        db.close()
    except Exception:
        pass

class Client(commands.Bot):
    async def on_ready(self):
        print(f"We have logged in as {self.user}")

        try:
            guild=discord.Object(id=os.getenv('SERVER_ID'))
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

    async def close(self):
        print('bot shutting down, Goodbye')
        db.close()
        await super().close()

    async def on_message(self, message):
        if message.author == client.user:
            return
        
        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')


intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents, command_prefix="!")
# client = discord.Client(intents=intents)
GUILD_ID=discord.Object(id=os.getenv('SERVER_ID'))


#slash commands

#easy pong test
@client.tree.command(name="ping", description="Responds with pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

#practice with passing in variables
@client.tree.command(name='printer', description='print word x times')
async def printer(interaction: discord.Interaction, word: str, x: int):
    await interaction.response.send_message(word+ " " + str(x))


#minecraft coords
@client.tree.command(name='add', description='Add a coordinate location with tag.')
async def add(interaction: discord.Interaction, label:str, x:int, y:int, z:int):
    print(f'adding {label, x, y, z, interaction.user.name}')
    name = interaction.user.name
    res = db.add(label, x, y, z, name)
    await interaction.response.send_message(res)
    # if res==1:
    #     print(f"user: {interaction.user.name},  **{label}** added at coordinates x: {x}, y: {y}, z: {z}")
    #     await interaction.response.send_message(f"Perfect {interaction.user.name} added **{label}** at coordinates x: {x}, y: {y}, z: {z}")
    # else:
    #     await interaction.response.send_message(f"there was an issue adding this coordinate to the database!")
    
@client.tree.command(name="ls", description='lists out all saved coordinates')
async def ls(interaction: discord.Interaction):
    res = db.list()
    if res==0:
        await interaction.response.send_message('There was an issue getting the coordinates from the database!')
    await interaction.response.send_message(res)

#rm rows
@client.tree.command(name="rm", description="remove coordinates IF you created them")
async def rm(interaction: discord.Interaction, label:str):
    print(f'removing {label}')
    res=db.remove(label, interaction.user.name)
    await interaction.response.send_message(res)

@client.tree.command(name="find", description="lists all coordinates matching [label]")
async def find(interaction: discord.Interaction, label:str):
    print(f'finding {label}')
    res= db.find(label)
    await interaction.response.send_message(res)    

@client.tree.command(name="man", description="minecraft coord bot manual")
async def man(interaction: discord.Interaction):
    await interaction.response.send_message(
        """
        ***Minecraft Coordinate Saver Manual***\n
        This bot contains 4 commands [add, rm, ls, man]\n
        **add:** adds a new coordinate to the database\n
        use: '\\add [label] [x] [y] [z]'  :  responds 1 on successful add\n
        **rm:** removes coordinate from database _if_ you created it\n
        use: '\\rm [label]  :  responds 'removed [label] created by [creator] on successful removal\n
        **ls:** lists all active coordinates\n
        **find:** finds all entries with the matching label\n
        use: \\find[label]  :  responds with all entries matching label. If no entries exists, responds 'no matching entries'
        """
    )



client.run(os.getenv('TOKEN'), log_handler=handler, log_level=logging.DEBUG)