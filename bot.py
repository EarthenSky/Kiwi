import discord
import asyncio
import os
import random
import mysql.connector
from discord.ext import commands, tasks

#TODO: Have bot add members to database with according values when it is run
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = ',',intents=intents)
client.remove_command('help')

rolesList = ['Dodo Red','Dodo Orange','Dodo Yellow','Dodo Green','Dodo Teal','Dodo Copyright','Dodo Cyan','Dodo Blue','Dodo Grape','Dodo Purple','Dodo Rose','Dodo Pink','Dodo Salmon']
activateRoles = ['Red','Orange','Yellow','Green','Teal','Copyright','Cyan','Blue','Grape','Purple','Rose','Pink','Salmon']
autoroles = ['Dodo Proper', '--------------- Colours---------------','------------- Holiday Roles -------------','--------------- Misc ---------------']


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


@client.event
async def on_member_join(member):
    guild = client.get_guild(744817281871249428)
    channel = guild.get_channel(800965152132431892)
    db = mysql.connector.connect(
    host= os.environ['HOST'],
    user = os.environ['USER'],
    password = os.environ['PASSWORD'],
    database = os.environ['DATABASE']
)

    c = db.cursor()
    c.execute(f"""INSERT INTO dodos 
                  VALUES ('{member.id}',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
              """)
    db.commit()
    c.close()
    db.close()
    await channel.send(f"Added {member} to database")

@client.event
async def on_member_leave(member):
    guild = client.get_guild(744817281871249428)
    channel = guild.get_channel(800965152132431892)
    db = mysql.connector.connect(
    host= os.environ['HOST'],
    user = os.environ['USER'],
    password = os.environ['PASSWORD'],
    database = os.environ['DATABASE']
)

    c = db.cursor()
    c.execute(f"""DELETE FROM dodos 
                  WHERE id = {member.id}
              """)
    db.commit()
    c.close()
    db.close()
    await channel.send(f"Added {member} to database")



@client.event
async def on_command_error(ctx,error):
    guild = client.get_guild(744817281871249428)
    channel = guild.get_channel(800965152132431892)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please pass in all required arguments. Use ,help for a list of commands")
        await channel.send(f"{ctx.message.author} didn't pass all arguments {error}")
    elif isinstance(error,commands.CommandOnCooldown):
        pass
    elif isinstance(error,commands.CommandNotFound):
        await ctx.send(f"That command does not exist. Use ,help for a list of commands")
        await channel.send(f"{ctx.message.author} tried to use a command that does not exist {error}")



@client.command()
async def ping(ctx):
    await ctx.send(f'Pong!')


@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="All Commands For Kiwi Bot",color=0x59cbf0)
    embed.set_thumbnail(url="https://i.imgur.com/Yx2cH7O.png")
    embed.add_field(name="Help Commands", value="**,help** - shows this message \n**,ping** - check if kiwi is still up", inline=False)
    embed.add_field(name="Mention A User Commands", value="**,waves @user** - waves at a user \n**,wavesRole @role** - waves at a group \n**,hugs @user** - gives the selected user a hug \n**,hugsRole @role** - group hug", inline=False)
    embed.add_field(name="Determine An Outcome Commands", value="**,8ball question** - ask Kiwi a question \n**,coinflip** - flip a coin \n**,poll \"Question\" option1 option2 ... option10** - Display a poll with n (2 <= n <= 10) options or a yes/no without any options shown" , inline=False)
    embed.add_field(name="Role Based Commands", value="**,collect** - obtain a role! 12 hour cooldown \n**,activate role** - activate a ,collect role\n**,trade \"your role\" @user \"their role\"**\n**,myroles** - display a list of your roles \n**,roles** - display a list of collectable roles", inline=False)
    embed.add_field(name="String Manipulation", value="**,fw message** - add sparkles between words \n**,spaced message** - space out your message \n**,spongebob message** - SpOnGeBoB MeMe", inline=False)
    embed.add_field(name="Economy", value="**,daily** - Recieve between 1 and 1000 discord dollars \n**,bal** - View your balance", inline=False)
    embed.add_field(name="Other", value="**,randomnumber a b ** - display rng [a,b] \n **,kittyclap** - send a kittyclap", inline=False)
    await ctx.send(embed=embed)


client.run(os.environ['TOKEN'])

