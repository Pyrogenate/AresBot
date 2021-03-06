from datetime import datetime
from asyncio import sleep
from glob import glob
from discord.ext.commands import when_mentioned_or
from discord.errors import HTTPException, Forbidden
from discord import Intents
from discord import Embed
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown
from discord.ext.commands import command, has_permissions
from ..db import db

OWNER_IDS = []
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


def get_prefix(bot , message):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        self.cogs_ready = Ready()

        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=get_prefix,
            owner_ids=OWNER_IDS,
            intents=Intents.all(),
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded")

        print("Setup Complete")

    def run(self, version):
        self.VERSION = version

        print("Running Setup...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running Bot....")
        super().run(self.TOKEN, reconnect=True)

    async def print_message(self):

        await self.stdout.send("Remember to Read the Rules!")

    async def on_connect(self):
        print("Bot Connected")

    async def on_disconnect(self):
        print("Bot Disconnected")


    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went Wrong :(")

        await self.stdout.send("An error occured.")
        raise

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):

            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing")


        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"Whoa there slow down sonic! Try again in {exc.retry_after:,.2f} secs.")

        elif hasattr(exc, "original"):
            if isinstance(exc.original, Forbidden):
                await ctx.send("I do not have permission to do that.")





        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.scheduler.start()
            self.stdout = self.get_channel(727213049974489212)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print("Bot Ready")
            await self.stdout.send("Now Online!")





        else:
            print("Bot Reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
