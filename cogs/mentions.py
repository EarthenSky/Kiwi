import discord
import asyncio
from discord.ext import commands
import mysql
import os

#Roles List 
activateRoles = ['Red','Orange','Yellow','Green','Teal','Copyright','Cyan','Blue','Grape','Purple','Rose','Pink','Salmon','Spring','Matcha','Mint','Ice','Bbblu','Lavender','Special']



#Mentions
class Interactions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['wave'])
    async def waves(self,ctx,member : discord.Member):
        await ctx.message.delete(delay = 0)
        await ctx.send(f"{ctx.message.author.mention} waves to {member.mention}")
        await ctx.send("https://media.tenor.com/images/ba69533b59d3ceaae8775a0550ff8037/tenor.gif")
    
    @waves.error
    async def waves_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Make sure you have mentioned a user to wave at")
        await channel.send(f"{ctx.message.author} experienced a error using wave")  

    @commands.command(aliases = ['hug'])
    async def hugs(self,ctx,member : discord.Member):
        await ctx.message.delete(delay = 0)
        await ctx.send(f"{ctx.message.author.mention} gibs beeeeg hug to {member.mention}")
        await ctx.send("https://media.tenor.com/images/0a1652de311806ce55820a7115993853/tenor.gif")

    @hugs.error
    async def hugs_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Make sure you have mentioned a user to hug")
        await channel.send(f"{ctx.message.author} experienced a error using hug") 

    @commands.command(aliases = ['hugRole','hugsrole','grouphug'])
    async def hugsRole(self,ctx,role : discord.Role):
        await ctx.message.delete(delay = 0)
        await ctx.send(f"{ctx.message.author.mention} gibs beeeeg group hug to {role.mention}")
        await ctx.send("https://media.tenor.com/images/0a1652de311806ce55820a7115993853/tenor.gif")

    @hugsRole.error
    async def hugsRole_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Make sure you have mentioned a role to give a group hug to")
        await channel.send(f"{ctx.message.author} experienced a error using grouphug") 

    @commands.command(aliases = ['waveRole','waverole','groupwave'])
    async def wavesRole(self,ctx,role : discord.Role):
        await ctx.message.delete(delay = 0)
        await ctx.send(f"{ctx.message.author.mention} waves to {role.mention}")
        await ctx.send("https://media4.giphy.com/media/3pZipqyo1sqHDfJGtz/200.gif")
    
    @wavesRole.error
    async def wavesRole_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Make sure you have mentioned a role to wave at a group")
        await channel.send(f"{ctx.message.author} experienced a error using wavesRole") 

    @commands.command(aliases = ["bringpeace"])
    async def banAlly(self,ctx):
        await ctx.send('Yes let us ban Ally!! Let us also ban Kyle!!')

    @commands.command()
    async def info(self,ctx, member : discord.Member):
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )
        c = db.cursor() 
        embedDescription = "**Role Information** \n"
        user = str(ctx.message.author)
        
        for role in activateRoles:
            c.execute(f"""SELECT {role}
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

        """)
            roleCount = ''.join(map(str,c.fetchall()[0]))
            embedDescription = embedDescription + roleCount + " Dodo " + role  + " roles" + "\n"
        embed=discord.Embed(title= user + "'s Information", description = embedDescription, color=0xe392fe)    
        embed.set_author(name= ctx.message.author, icon_url=ctx.member.avatar_url)
        
        c.execute(f"""SELECT money
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

        """)
        money = ''.join(map(str,c.fetchall()[0]))
        c.execute(f"""SELECT birthday
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

        """)
        birthday = ''.join(map(str,c.fetchall()[0]))
        embed.add_field(name=f"Money Balance", value=f"{money}" , inline=True)
        if(birthday == '0000'):
            embed.add_field(name=f"Birthday", value=f"N/A" , inline=True)
        else:
            embed.add_field(name=f"Birthday", value=f"{birthday}" , inline=True)
        c.close()
        db.close()


        

def setup(client):
    client.add_cog(Interactions(client))