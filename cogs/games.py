import discord
from discord.ext import commands
import os
import random
import asyncio
import mysql

numbers = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
suits = ["🍇", "🍉", "🍒", "🍍"]


# Mentions
class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['21'])
    async def blackjack(self, ctx, bet):
        cards_dictionary = {
            "A": 4,
            2: 4,
            3: 4,
            4: 4,
            5: 4,
            6: 4,
            7: 4,
            8: 4,
            9: 4,
            10: 4,
            "J": 4,
            "Q": 4,
            "K": 4
        }

        bet = int(bet)
        if bet <= 0:
            await ctx.send("You must bet at least 1 Dodo Dollar")
            return
        else:
            db = mysql.connector.connect(
                host=os.environ['HOST'],
                user=os.environ['USER'],
                password=os.environ['PASSWORD'],
                database=os.environ['DATABASE']
            )
            c = db.cursor()
            c.execute(f"""SELECT money
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

            """)
            balance = ''.join(map(str, c.fetchall()[0]))
            if bet > int(balance):
                await ctx.send("You do not have that much money!")
            else:
                embed = discord.Embed(title="Dodo Club Casino | Blackjack", color=0x99c0dd)
                user_blackjack = False
                user_cards = []
                user_int = 0
                user_int2 = 0
                user_description = ''

                dealer_blackjack = False
                mystery_score = 0
                mystery_score2 = 0
                dealer_cards = []
                dealer_int = 0
                dealer_int2 = 0
                dealer_description = ''

                for i in range(0, 2):
                    user_card = random.choice(numbers)
                    while cards_dictionary[user_card] == 0:
                        user_card = random.choice(numbers)

                    cards_dictionary[user_card] = cards_dictionary[user_card] - 1
                    user_suit = random.choice(suits)
                    while str(user_card) + user_suit in user_cards or str(user_card) + user_suit in dealer_cards:
                        user_suit = random.choice(suits)

                    user_cards.append(str(user_card) + user_suit)
                    if user_card == "J" or user_card == "K" or user_card == "Q":
                        user_int = user_int + 10
                        user_int2 = user_int2 + 10
                    elif user_card == "A":
                        user_int = user_int + 1
                        if user_int2 + 11 <= 21:
                            user_int2 = user_int2 + 11
                        else:
                            user_int2 = user_int2 + 1
                    else:
                        user_int = user_int + user_card
                        user_int2 = user_int2 + user_card

                    dealer_card = random.choice(numbers)
                    while cards_dictionary[dealer_card] == 0:
                        dealer_card = random.choice(numbers)

                    cards_dictionary[dealer_card] = cards_dictionary[dealer_card] - 1
                    dealer_suit = random.choice(suits)
                    while str(dealer_card) + dealer_suit in user_cards or str(dealer_card) + dealer_suit in dealer_cards:
                        dealer_suit = random.choice(suits)
                    dealer_cards.append(str(dealer_card) + dealer_suit)
                    if dealer_card == "J" or dealer_card == "K" or dealer_card == "Q":
                        dealer_int = dealer_int + 10
                        dealer_int2 = dealer_int2 + 10
                    elif dealer_card == "A":
                        dealer_int = dealer_int + 1
                        if dealer_int2 + 11 <= 21:
                            dealer_int2 = dealer_int2 + 11
                        else:
                            dealer_int2 = dealer_int2 + 1
                    else:
                        dealer_int = dealer_int + dealer_card
                        dealer_int2 = dealer_int2 + dealer_card

                    if i == 0:
                        mystery_score = mystery_score + dealer_int
                        if mystery_score == 1:
                            mystery_score2 = mystery_score2 + dealer_int2
                        else:
                            mystery_score2 = mystery_score2 + dealer_int

                # Check for instant blackjack
                if user_int == 21 or user_int2 == 21:
                    user_blackjack = True

                    # Check for instant blackjack
                if dealer_int == 21 or dealer_int2 == 21:
                    dealer_blackjack = True

                for cards in user_cards:
                    user_description = user_description + cards + " "

                # initial setup to show face down card
                dealer_description = dealer_description + dealer_cards[0] + " [ ]"

                user_description = f"{user_description} \n \nScore: {user_int} or {user_int2}"
                dealer_description = f"{dealer_description} \n \nScore: {mystery_score} or {mystery_score2}"
                embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}", inline=True)
                embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                embed.add_field(name=f"What would you like to do? You have 20 seconds to decide", value="Hit or Stand",
                                inline=False)
                game_message = await ctx.send(embed=embed)

                while 1:
                    if user_int >= 22 and user_int2 >= 22:
                        break

                    elif user_int == 21 or user_int2 == 21:
                        break

                    try:
                        msg = await self.client.wait_for(
                            "message",
                            timeout=20,
                            check=lambda message: message.author == ctx.message.author and message.channel == ctx.channel
                        )

                        msg_str = msg.content.strip().lower()
                        if msg_str == "hit":
                            embed = discord.Embed(title="Dodo Club Casino | Blackjack", color=0x99c0dd)
                            user_description = ''
                            user_card = random.choice(numbers)
                            while cards_dictionary[user_card] == 0:
                                user_card = random.choice(numbers)

                            cards_dictionary[user_card] = cards_dictionary[user_card] - 1
                            user_suit = random.choice(suits)
                            while str(user_card) + user_suit in user_cards or str(user_card) + user_suit in dealer_cards:
                                user_suit = random.choice(suits)
                            user_cards.append(str(user_card) + user_suit)
                            if user_card == "J" or user_card == "K" or user_card == "Q":
                                user_int = user_int + 10
                                user_int2 = user_int2 + 10
                            elif user_card == "A":
                                user_int = user_int + 1
                                if user_int2 + 11 <= 21:
                                    user_int2 = user_int2 + 11
                                else:
                                    user_int2 = user_int2 + 1
                            else:
                                user_int = user_int + user_card
                                user_int2 = user_int2 + user_card

                            for cards in user_cards:
                                user_description = user_description + cards + " "
                            user_description = f"{user_description} \n \n Score: {user_int} or {user_int2}"
                            embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}",
                                            inline=True)
                            embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                            embed.add_field(name=f"What would you like to do? You have 20 seconds to decide",
                                            value="Hit or Stand", inline=False)
                            await msg.delete(delay=0)
                            await game_message.edit(embed=embed)
                        else:
                            await msg.delete(delay=0)
                            break

                    except asyncio.TimeoutError:
                        break

                embed = discord.Embed(title="Dodo Club Casino | Blackjack", color=0x99c0dd)
                if user_int >= 22 and user_int2 >= 22:
                    embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}",
                                    inline=True)
                    embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                    embed.add_field(name=f"Outcome", value=f"Bust! You have lost {str(bet)}", inline=False)
                    await game_message.edit(embed=embed)
                    c.execute(f"""UPDATE dodos
                        SET money = money - {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                    db.commit()

                else:
                    if user_int <= user_int2 <= 21:
                        user_int = user_int2

                    elif user_int2 <= user_int <= 21:
                        user_int = user_int

                    elif user_int2 <= 21 < user_int:
                        user_int = user_int2

                    elif user_int <= 21 < user_int2:
                        user_int = user_int

                    if user_blackjack is False and dealer_blackjack is False:
                        while 1:
                            if (dealer_int >= 22) and (dealer_int2 >= 22):
                                break
                            elif dealer_int >= 17 or dealer_int2 >= 17:
                                break
                            elif dealer_int >= user_int:
                                break
                            else:
                                dealer_card = random.choice(numbers)
                                while cards_dictionary[dealer_card] == 0:
                                    dealer_card = random.choice(numbers)
                                cards_dictionary[dealer_card] = cards_dictionary[dealer_card] - 1
                                dealer_suit = random.choice(suits)
                                while str(dealer_card) + dealer_suit in user_cards or str(dealer_card) + dealer_suit in dealer_cards:
                                    dealer_suit = random.choice(suits)
                                dealer_cards.append(str(dealer_card) + dealer_suit)
                                if dealer_card == "J" or dealer_card == "K" or dealer_card == "Q":
                                    dealer_int = dealer_int + 10
                                    dealer_int2 = dealer_int2 + 10
                                elif dealer_card == "A":
                                    dealer_int = dealer_int + 1
                                    if dealer_int2 + 11 <= 21:
                                        dealer_int2 = dealer_int2 + 11
                                    else:
                                        dealer_int2 = dealer_int2 + 1
                                else:
                                    dealer_int = dealer_int + dealer_card
                                    dealer_int2 = dealer_int2 + dealer_card

                    if dealer_int >= 22 and dealer_int2 >= 22:
                        dealer_int = dealer_int

                    elif dealer_int <= dealer_int2 <= 21:
                        temp = dealer_int
                        dealer_int = dealer_int2
                        dealer_int2 = temp

                    elif dealer_int2 <= dealer_int <= 21:
                        dealer_int = dealer_int

                    elif dealer_int2 <= 21 < dealer_int:
                        temp = dealer_int
                        dealer_int = dealer_int2
                        dealer_int2 = temp

                    elif dealer_int <= 21 < dealer_int2:
                        dealer_int = dealer_int

                    embed = discord.Embed(title="Dodo Club Casino | Blackjack", color=0x99c0dd)
                    dealer_description = ' '
                    for cards in dealer_cards:
                        dealer_description = dealer_description + cards + " "
                    dealer_description = f"{dealer_description} \n \n Score: {dealer_int} or {dealer_int2}"

                    if user_blackjack is True:
                        bet = bet * 2
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}",
                                        inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                        embed.add_field(name=f"Outcome", value=f"**Blackjack! You have won {str(bet)} Dodo Dollars!**",
                                        inline=False)
                        await game_message.edit(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money + {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

                    elif dealer_blackjack is True:
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}",
                                        inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                        embed.add_field(name=f"Outcome", value=f"**You have lost {str(bet)} Dodo Dollars! Kiwi wins!**",
                                        inline=False)
                        await game_message.edit(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money - {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

                    elif user_int < dealer_int < 22:
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}",
                                        inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                        embed.add_field(name=f"Outcome", value=f"**You have lost {str(bet)} Dodo Dollars! Kiwi wins!**",
                                        inline=False)
                        await game_message.edit(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money - {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

                    elif dealer_int == user_int:
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}",
                                        inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                        embed.add_field(name=f"Outcome", value=f"**You have tied! No one wins**", inline=False)
                        await game_message.edit(embed=embed)

                    else:
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}",
                                        inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                        embed.add_field(name=f"Outcome", value=f"**You have won {str(bet)}!**", inline=False)
                        await game_message.edit(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money + {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

                    print(cards_dictionary)
                    del user_cards
                    del dealer_cards

            c.close()
            db.close()

    @blackjack.error
    async def blackjack_error(self, ctx, error):
        channel = ctx.guild.get_channel(os.environ['CHANNEL'])
        await channel.send(f"{ctx.message.author} experienced a error using blackjack. {error}")

    @commands.command(aliases=['cup', 'cups'])
    async def cupshuffle(self, ctx, bet):
        bet = int(bet)
        if bet < 1:
            await ctx.send("You must bet at least 1 Dodo Dollar")
        else:
            db = mysql.connector.connect(
                host=os.environ['HOST'],
                user=os.environ['USER'],
                password=os.environ['PASSWORD'],
                database=os.environ['DATABASE']
            )
            c = db.cursor()
            c.execute(f"""SELECT money
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

            """)
            balance = ''.join(map(str, c.fetchall()[0]))
            if bet > int(balance):
                await ctx.send("You do not have that much money!")
            else:
                gem = random.randint(1, 3)
                embed_description = "Which Kiwi has the hidden gem \n 🥝 🥝 🥝"
                ending_description = ""
                embed = discord.Embed(title="Dodo Club Casino | Cup Shuffle", description=embed_description,
                                      color=0x99c0dd)
                await ctx.send(embed=embed)
                await ctx.send(f'Which Kiwi would you like to pick 1, 2, 3? If you do not answer in 20 seconds I will randomly pick for you')

                try:
                    msg = await self.client.wait_for(
                        "message",
                        timeout=20,
                        check=lambda message: message.author == ctx.message.author and message.channel == ctx.channel
                    )
                    msg = msg.content.strip().lower()
                    try:
                        msg = int(msg)
                    except:
                        await ctx.send("Gonna give you a random variable for not following rules.")
                        msg = random.randint(1, 4)
                    if msg == gem:
                        for i in range(1, 4):
                            if i == gem:
                                ending_description = ending_description + "🏆 "
                            else:
                                ending_description = ending_description + "🥝 "
                        embed = discord.Embed(title="Dodo Club Casino | Cup Shuffle", description=ending_description,
                                              color=0x99c0dd)
                        embed.add_field(name=f"Outcome", value=f"**You have won {str(bet)}!**", inline=False)
                        await ctx.send(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money + {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()
                    else:
                        for i in range(1, 4):
                            if i == gem:
                                ending_description = ending_description + "🏆 "
                            elif i == msg:
                                ending_description = ending_description + "❌ "
                            else:
                                ending_description = ending_description + "🥝 "
                        embed = discord.Embed(title="Dodo Club Casino | Cup Shuffle", description=ending_description,
                                              color=0x99c0dd)
                        embed.add_field(name=f"Outcome", value=f"**You have lost {str(bet)}!**", inline=False)
                        embed.set_footer(text=f"Winning Kiwi was number {gem}")
                        await ctx.send(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money - {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

                except asyncio.TimeoutError:
                    user_guess = random.randint(1, 3)
                    await ctx.send(f"Assuming you meant to guess kiwi number: {user_guess}")
                    if user_guess == gem:
                        for i in range(1, 4):
                            if i == gem:
                                ending_description = ending_description + "🏆 "
                            else:
                                ending_description = ending_description + "🥝 "
                        embed = discord.Embed(title="Dodo Club Casino | Cup Shuffle", description=ending_description,
                                              color=0x99c0dd)
                        embed.add_field(name=f"Outcome", value=f"**You have won {str(bet)}!**", inline=False)
                        await ctx.send(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money + {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()
                    else:
                        for i in range(1, 4):
                            if i == gem:
                                ending_description = ending_description + "🏆 "
                            elif i == user_guess:
                                ending_description = ending_description + "❌ "
                            else:
                                ending_description = ending_description + "🥝 "
                        embed = discord.Embed(title="Dodo Club Casino | Cup Shuffle", description=ending_description,
                                              color=0x99c0dd)
                        embed.add_field(name=f"Outcome", value=f"**You have lost {str(bet)}!**", inline=False)
                        embed.set_footer(text=f"Winning Kiwi was number {gem}")
                        await ctx.send(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money - {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

            c.close()
            db.close()

    @cupshuffle.error
    async def cupshuffle_error(self, ctx, error):
        channel = ctx.guild.get_channel(os.environ['CHANNEL'])
        await ctx.send("Syntax for this command is: **,cupshuffle bet**")
        await channel.send(f"{ctx.message.author} experienced a error using cupshuffle. {error}")


def setup(client):
    client.add_cog(Games(client))
