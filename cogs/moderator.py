import discord
from discord.ext import commands
import random
import os
from discord.ext.commands import has_permissions, has_role
from discord.utils import get
import re

pollOptions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

# Temporarily supressing possibly invalid code
'''
class Moderator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @has_permissions(manage_roles=True)
    @commands.command()
    async def createrole(self, ctx, colour, *, role):
        if get(ctx.guild.roles, name=f"{role}"):
            await ctx.send("Role already exists")
            return
        regex = "^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
        p = re.compile(regex)
        if re.search(p, str(colour)):
            guild = ctx.guild
            colour_of_role = '0x' + str(colour)
            print(colour_of_role)
            await guild.create_role(name=role, color=discord.Colour(int(f'{colour}', 16)))
            print("role Created")
            await ctx.send(f"{role} created with colour code {colour_of_role}")
        else:
            await ctx.send("Enter a valid hex colour code")

    @has_role(item='Dodo Op')
    @commands.command()
    async def echo(self, ctx, *, statement):
        await ctx.message.delete(delay=0)
        await ctx.send(f"{statement}")


def setup(client):
    client.add_cog(Moderator(client))
'''