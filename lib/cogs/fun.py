from discord.ext.commands import Cog
from discord import Member
from typing import Optional
from discord import Embed
from random import choice
from aiohttp import request
from discord.ext.commands import command, cooldown, BucketType
import praw
import random
from asyncio import sleep


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='hi', brief='Says Hi , Hiya, Heya, Hey, Or Hello to You o.0')
    @cooldown(1, 2, BucketType.user)
    async def say_hi(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Heya', 'Hiya', 'Hey'))} {ctx.author.mention}!")

    @command(name="dice", aliases=["roll"], brief='Rolls an imaginary dice :o')
    @cooldown(1, 2, BucketType.user)
    async def roll_dice(self, ctx):
        dicelist = ['1', '2', '3', '4', '5', '6']
        await ctx.send(f"You rolled a {choice(dicelist)}!")

    @command(name='bonk', brief='Violently bonks the other user')
    @cooldown(1, 2, BucketType.user)
    async def slap_person(self, ctx, member: Member, *, reason: Optional[str] = " No Reason"):
        await ctx.send(f"{ctx.author.display_name} bonked {member.mention} for {reason}!")

    @command(name='echo', aliases=['say'], brief='Ares says what you tell it to!')
    async def echo_message(self, ctx, *, message):
        await ctx.send(message)

    @command(name="fact",
             brief='Gives you a random animal fact according to the animal you specify. Also shows an image')
    @cooldown(1, 2, BucketType.user)
    async def animal_fact(self, ctx, animal: str):
        if animal in ("Dog", "Cat", "Panda", "Fox", "Koala", "dog", "cat", "panda", "fox", "koala"):
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

    @command(name='meme', brief='Posts a random meme')
    @cooldown(1, 2, BucketType.user)
    async def gordon(self, ctx):
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

    @command(name='8ball', brief='Ask the almighty 8ball a question and it shall answer')
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]

        embed = Embed(title="8ball", description="Ask The Almighty 8ball", color=ctx.author.color)
        embed.add_field(name="Question", value=f'{question}')
        embed.add_field(name=f"{ctx.author.display_name}, the answer to your question is ",
                        value=f'{random.choice(responses)}')
        embed.add_field(name="Made By", value="Pyrogenate")

        await ctx.send(content=None, embed=embed)



    @command(brief='Auto Posts Memes every 5 seconds')
    async def automeme(self, ctx):
        reddit = praw.Reddit(client_id='p668-DbYvlTe4w',
                             client_secret='GGdtizGTGNBI6UwvcvbtACN_Rf0',
                             user_agent='memer')
        memes_submissions = reddit.subreddit('memes').hot()
        post_to_pick = random.randint(1, 2000)
        for i in range(0, post_to_pick):
            await sleep(5)
            submission = next(x for x in memes_submissions if not x.stickied)

            embed = Embed(title=f"Here is a meme for you {ctx.author.display_name}!",
                          color=ctx.author.color,
                          description='By Pyrogenate#1206')


            embed.set_image(url=submission.url)

            await ctx.send(embed=embed)


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))
