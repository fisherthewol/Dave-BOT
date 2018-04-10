import logging
import logging.handlers
import platform
import queue
import signal
import sys

import discord
import feedparser
from discord.ext import commands


class Dave:
    """Main class for Bot."""
    def __init__(self, code, loglevel, redid, redsc, wk):
        self.client = commands.Bot(command_prefix="!")
        self.code = code
        self.cogs = []
        if (redid and redsc):
            # Enable reddit cog.
            self.client.rid = redid
            self.client.rsc = redsc
            self.cogs.append("DaveBOT.cogs.reddit")
        if wk:
            # Enable weather cog.
            self.client.wk = wk
            self.cogs.append("DaveBOT.cogs.weather")
        # enable meme cog
        self.cogs.append("DaveBOT.cogs.memes")
        self.loadcogs()
        self.setupLogging(loglevel)
        self.host_is_Linux = True if ("Linux" in platform.system()) else False
        signal.signal(signal.SIGTERM, self.sigterm)

    def loadcogs(self):
        """Load discordpy cogs."""
        for cog in self.cogs:
            try:
                self.client.load_extension(cog)
            except Exception as e:
                self.logger.critical("Failed load {}, exception {}".format(cog,
                                                                           e))

    def setupLogging(self, loglev):
        """Sets up logging"""
        # Setup queue and queue handler:
        que = queue.Queue(-1)
        queue_handler = logging.handlers.QueueHandler(que)
        queue_handler.setLevel(loglev)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(queue_handler)
        # Setup listener:
        streamhandle = logging.StreamHandler()
        streamhandle.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s"
            " [in %(pathname)s:%(lineno)d]"))
        streamhandle.setLevel(loglev)
        listener = logging.handlers.QueueListener(que, streamhandle)
        listener.start()
        self.logger.warning("Logging is setup in core.py")

    def sigterm(self, signal, frame):
        """Response to sigterm."""
        self.logger.critical("SIGTERM recieved, ending.")
        sys.exit("SIGTERM recieved, ending.")

    def uptimeFunc(self):
        """Returns formatted host uptime."""
        if self.host_is_Linux:
            from datetime import timedelta
            with open("/proc/uptime", "r") as f:
                uptime_seconds = float(f.readline().split()[0])
                uptime_string = str(timedelta(seconds=uptime_seconds))
            return uptime_string
        else:
            self.logger.warning("Host is not linux, uptimeFunc not supported.")
            return "incomp host."

    def discout(self):
        """Discord functions and client running."""
        @self.client.event
        async def on_ready():
            """Outputs on successful launch."""
            self.logger.warning("Login Successful")
            self.logger.warning("Name : {}" .format(self.client.user.name))
            self.logger.warning("ID : {}" .format(self.client.user.id))
            self.logger.info("Successful self.client launch.")
            await self.client.change_presence(game=discord.Game(name="for !help", type=3))

        @self.client.command(pass_context=True)
        async def dave(ctx):
            """Provides data about Dave and the system it's running on."""
            self.logger.info("!dave called.")
            if self.host_is_Linux:
                uptime = self.uptimeFunc()
                version = platform.python_version()
                compi = platform.python_compiler()
                # next 3 lines will be depreceated in py3.7; find alternative?
                lindist = platform.linux_distribution()
                lindistn = lindist[0]
                lindistv = lindist[1]
                await self.client.say("\nHost Uptime: {}"
                                      "\nPython Version: {}\n"
                                      "\nPython Compiler: {}"
                                      "\nDistro: {};v{}".format(uptime,
                                                                version,
                                                                compi,
                                                                lindistn,
                                                                lindistv))
            else:
                self.logger.warning("Host not linux, !dave is not supported.")
                await self.client.say("Host !=linux; feature coming soon.\n")

        @self.client.command(pass_context=True)
        async def news(ctx):
            """Returns top news from bbc and gameinformer."""
            self.logger.info("!news called.")
            bbcmsg = await self.client.say("Fetching bbc news...")
            gmimsg = await self.client.say("Fetching gameinformer news...")
            bbc = feedparser.parse("https://feeds.bbci.co.uk/news/world/"
                                   "europe/rss.xml")
            game = feedparser.parse("https://www.gameinformer.com/b/"
                                    "mainfeed.aspx?Tags=feature")
            await self.client.edit_message(bbcmsg, bbc.entries[0]["link"])
            await self.client.edit_message(gmimsg, game.entries[0]["link"])

        @self.client.command(pass_context=True)
        async def pie(ctx):
            """Replies with latest Jonathan Pie video"""
            self.logger.info("!pie called.")
            piemsg = await self.client.say("Fetching video.")
            pie = await self.client.loop.run_in_executor(None,
                                                         feedparser.parse,
                                                         "https://www.youtube.com/feeds/videos.xml?channel_id=UCO79NsDE5FpMowUH1YcBFcA")
            await self.client.edit_message(piemsg, pie.entries[0]['link'])

        self.client.run(str(self.code))


if __name__ == "__main__":
    raise sys.exit("This is an import file, please do not run directly.")
