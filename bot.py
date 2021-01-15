import discord
import asyncio
import os
import random
import sqlite3
from discord.ext import commands, tasks


client = commands.Bot(command_prefix = ',')
client.remove_command('help')

conn = sqlite3.connect('members.db')
c = conn.cursor()

rolesList = ['Dodo Red','Dodo Orange','Dodo Yellow','Dodo Green','Dodo Teal','Dodo Copyright','Dodo Bluev2','Dodo Blue','Dodo Purplev2','Dodo Purple','Dodo Pinkv2','Dodo Pink']

@client.command()
async def load(ctx,extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx,extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    print("Bot is Ready")
    c.execute("""DROP TABLE dodos""")
    print("Let's see...")
    conn.commit()
    # c.execute("""
    #     CREATE TABLE IF NOT EXISTS dodos(
    #         id real,
    #         money real,
    #         Red real,
    #         Orange real,
    #         Yellow real,
    #         Green real,
    #         Teal real,
    #         Copyright real,
    #         Bluev2 real,
    #         Blue real,
    #         Purplev2 real,
    #         Purple real,
    #         Pinkv2 real,
    #         Pink real
    #     ) 
    #     """)
    # conn.commit()
    # for guild in client.guilds:
    #         for member in guild.members:
    #             try:
    #                 c.execute(f"""SELECT id 
    #                         FROM dodos 
    #                         WHERE id ='{member.id}'
    #                     """)
    #             except: 
    #                 c.execute(f"""INSERT INTO dodos 
    #                     VALUES ('{member.id}',0,0,0,0,0,0,0,0,0,0,0,0,0)
    #                 """)
    #                 conn.commit()
    
    # for member in guild.members:
    #     for r in rolesList:
    #         role = discord.utils.get(guild.roles, name=r)
    #         if (role in member.roles):
    #             role = str(role)
    #             role = role.split()[1]
    #             c.execute(f"""Update dodos
    #             SET {role} = {role} + 1
    #             WHERE id = {member.id}
    #             """)
    #             conn.commit()
    #         else:
    #             pass
    


@client.command(pass_context=True)
async def help(ctx):
    embed=discord.Embed(title="Help Command", description="List of all commands", color=0x59cbf0)
    embed.add_field(name=",waves", value="Wave at a user", inline=False)
    embed.add_field(name=",wavesRole @role", value="Waves at a role", inline=False)
    embed.add_field(name=",hug @user", value="Give @user a hug", inline=False)
    embed.add_field(name=",hugsRole @role", value="Grouphug with @role members", inline=False)
    embed.add_field(name=",8ball question", value="Gives the user an answer to their question", inline=False)
    embed.add_field(name=",coinflip", value="Heads or Tails", inline=False)
    embed.add_field(name=",collect", value="Collect one of the time-limited event roles", inline=False)
    embed.add_field(name=",trade \"role1\" @user \"role2\" ", value="Trade role1 with another users role 2", inline=False)
    embed.add_field(name=",randomnumber a b", value="Displays a random number between a and b inclusvely", inline=False)
    embed.add_field(name=",fw message", value="Seperate the message with sparkles", inline=False)
    embed.add_field(name=",spaced message", value="Add spaces into the message", inline=False)
    embed.add_field(name=",spongebob message", value="Convert the message into Spongebob Meme Format", inline=False)
    embed.add_field(name=",ping", value="Pong", inline=False)
    embed.add_field(name=",roles", value="Display a list of colour roles", inline=False)
    embed.add_field(name=",activate \"role\" ", value="Activate the role as your colour", inline=False)
    embed.add_field(name=",help", value="Display this message", inline=False)
    await ctx.send(embed=embed)

client.run(os.environ['TOKEN'])
