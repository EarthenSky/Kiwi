import discord
import asyncio
import os
import random
from discord.ext import commands, tasks

client = commands.Bot(command_prefix = ',')
client.remove_command('help')

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
    embed.add_field(name=",banAlly", value="Speak the truth", inline=False)
    embed.add_field(name=",ping", value="Pong", inline=False)
    embed.add_field(name=",roles", value="Display a list of collectable roles", inline=False)
    embed.add_field(name=",help", value="Display this message", inline=False)
    await ctx.send(embed=embed)

# @client.event
# async def on_member_join(member):
#     db = sqlite3.connect('dodo.sqlite')
#     cursor = db.cursor()
#     cursor.execute(f"SELECT member FROM Members WHERE name = {member}")
#     result = cursor.fetchone()
#     if result is None:
#         sql = (f"INSERT INTO Member(name,money,santa,elf,frosty,gift,reindodo,grinch) VALUES(?,?,?,?,?,?,?,?)")
#         val = (f"{member},0,0,0,0,0,0,0")
    


# @client.event
# async def on_member_remove(member):
#     channel = client.get_channel(777046531214671902)    
#     await channel.send(f"Goodbye {member.display_name}")


#Blackbox
f = open("specialCode.txt", "r")
Token = str(f.readline()).strip('\n')
client.run(Token)
