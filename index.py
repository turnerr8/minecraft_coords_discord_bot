import discord
import os
import logging
import sqlite3


from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from dbHandler import DbHandler

load_dotenv()
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
db = DbHandler()

class Client(commands.Bot):
    async def on_ready(self):
        print(f"We have logged in as {self.user}")

        try:
            guild=discord.Object(id=os.getenv('SERVER_ID'))
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

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
@client.tree.command(name="ping", description="Responds with pong!", guild=GUILD_ID)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

#practice with passing in variables
@client.tree.command(name='printer', description='print word x times', guild=GUILD_ID)
async def printer(interaction: discord.Interaction, word: str, x: int):
    await interaction.response.send_message(word+ " " + str(x))


#minecraft coords
@client.tree.command(name='add', description='Add a coordinate location with tag.', guild=GUILD_ID)
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
    
@client.tree.command(name="ls", description='lists out all saved coordinates', guild=GUILD_ID)
async def ls(interaction: discord.Interaction):
    res = db.list()
    if res==0:
        await interaction.response.send_message('There was an issue getting the coordinates from the database!')
    await interaction.response.send_message(res)

#rm rows
@client.tree.command(name="rm", description="remove coordinates IF you created them", guild=GUILD_ID)
async def rm(interaction: discord.Interaction, label:str):
    print(f'removing {label}')
    res=db.remove(label, interaction.user.name)
    await interaction.response.send_message(res)



client.run(os.getenv('TOKEN'), log_handler=handler, log_level=logging.DEBUG)