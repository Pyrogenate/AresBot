from datetime import datetime
from discord import Intents
from discord import Embed
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from ..db import db

PREFIX = "/"
OWNER_IDS = [654159767526441000]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            intents=Intents.all(),
        )

    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running Bot....")
        super().run(self.TOKEN, reconnect=True)


    async def print_message(self):
        channel = self.get_channel(727213049974489212)
        await channel.send("Remember to Read the Rules!")


    async def on_connect(self):
        print("Bot Connected")

    async def on_disconnect(self):
        print("Bot Disconnected")


    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong :(")

        raise




    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass

        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.scheduler.start()
            self.scheduler.add_job(self)
            print("Bot Ready")

            channel = self.get_channel(727213049974489212)
            await channel.send("Now Online!")

            #embed = Embed(title="Now online!", description="Ares is now online.",timestamp=datetime.utcnow(), color=0xFF0000)
            #fields = [("Name", "Value", True),
                     # ("Another field", "This field is next to the other one", True),
                     # ("A non-inline field", "This field will appear on it's own row", False)]
            #for name, value, inline in fields:
               # embed.add_field(name=name, value=value, inline=inline)
               # embed.set_footer(text="This is a footer!")
            #await channel.send(embed=embed)




        else:
            print("Bot Reconnected")



    async def on_message(self, message):
        pass


bot = Bot()
