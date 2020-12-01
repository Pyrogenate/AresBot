from discord.ext.commands import Cog
from discord import Member
from typing import Optional
from discord import Embed
from random import choice
from aiohttp import request
from discord.ext.commands import command, cooldown, BucketType


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='hi')
    @cooldown(1, 2, BucketType.user)
    async def say_hi(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Heya', 'Hiya', 'Hey'))} {ctx.author.mention}!")

    @command(name="dice", aliases=["roll"])
    @cooldown(1, 2, BucketType.user)
    async def roll_dice(self, ctx):
        dicelist = ['1', '2', '3', '4', '5', '6']
        await ctx.send(f"You rolled a {choice(dicelist)}!")

    @command(name='bonk')
    @cooldown(1, 2, BucketType.user)
    async def slap_person(self, ctx, member: Member, *, reason: Optional[str] = " No Reason"):
        await ctx.send(f"{ctx.author.display_name} bonked {member.mention} for {reason}!")

    @command(name='echo', aliases=['say'])
    async def echo_message(self, ctx, *, message):
        await ctx.send(message)

    @command(name="fact")
    @cooldown(1, 2, BucketType.user)
    async def animal_fact(self, ctx, animal: str):
        if animal in ("Dog", "Cat", "Panda", "Fox", "Koala","dog", "cat", "panda", "fox", "koala" ):
            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url = f"https://some-random-api.ml/img/{animal}"
            async with request("GET", image_url) as response:
                if response.status == 200:
                    data = await response.json()
                    image = data["link"]


                else:
                    image = None
            async with request("GET", fact_url) as response:

                if response.status == 200:
                    data = await response.json()

                    embed = Embed(title=f"{animal} fact",
                                  description=data["fact"],
                                  color=ctx.author.color)


                    if image is not None:
                        embed.set_image(url=image)




                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API returned a {response.status} status")

        else:
            await ctx.send("No facts are available for this animal :(")


    @command()
    @cooldown(1, 2, BucketType.user)
    async def meme(self, ctx):
        meme_url = "https://some-random-api.ml/meme"


        async with request("GET", meme_url) as response:
            if response.status == 200:
                data = await response.json()
                meme = data["image"]

                embed = Embed(title=f"Here is a meme for you {ctx.author.display_name}!",
                              color=ctx.author.color,
                              footer='By Pyrogenate#1206')

                if meme is not None:
                    embed.set_image(url=meme)

                await ctx.send(embed=embed)







    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))
