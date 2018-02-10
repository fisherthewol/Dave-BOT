import discord, feedparser  # Need installing.
from discord.ext import commands
import os, platform, logging  # Builtins.
from DaveBOT import redditclient


class Dave:
    """Main class for BOT."""
    def __init__(self, code, loglevel=logging.WARNING):
        self.code = code
        self.description = "This is a WIP bot to work discord. Use !bothelp."
        self.bot_prefix = "!"
        global client
        client = commands.Bot(command_prefix=self.bot_prefix,
                              description=self.description)
        self.setupLogging(loglevel)
        if "Linux" in platform.system():
            self.host_is_Linux = True
        else:
            self.host_is_Linux = False

    def setupLogging(self, loglev):
        self.logger = logging.getLogger(__name__)
        handle = logging.StreamHandler()
        handle.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s"
            " [in %(pathname)s:%(lineno)d]"))
        self.logger.addHandler(handle)
        self.logger.setLevel(loglev)
        self.logger.info("Logging is setup.")

    def uptimeFunc(self):
        """Returns host uptime nicely."""
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
        @client.event
        async def on_ready():
            """Outputs on successful launch."""
            self.logger.warning("Login Successful")
            self.logger.warning("Name : {}" .format(client.user.name))
            self.logger.warning("ID : {}" .format(client.user.id))
            self.logger.info("Successful client launch.")
            await client.change_presence(game=discord.Game(name="Use !bothelp"))

        @client.command(pass_context=True)
        async def bothelp(ctx):
            """!bothelp, gives help on how to use the bot."""
            self.logger.info("!bothelp called.")
            await client.say("\nAvailible commands:"
                             "\n!bothelp -- What you're seeing now."
                             "\n!news -- See top news stories now."
                             "\n!prequel -- See the day's top post (so far) "
                             "from /r/prequelmemes."
                             "\n!pie -- get latest JPie Vid."
                             "\n!subreddit -- see !subhelp."
                             "\n!dave -- get bot stats.")

        @client.command(pass_context=True)
        async def news(ctx):
            """!news, returns top news from bbc and gameinformer."""
            self.logger.info("!news called.")
            bbc = feedparser.parse("https://feeds.bbci.co.uk/news/world/"
                                   "europe/rss.xml")
            game = feedparser.parse("https://www.gameinformer.com/b/"
                                    "mainfeed.aspx?Tags=feature")
            await client.say(bbc.entries[0]["link"])
            await client.say(game.entries[0]["link"])

        @client.command(pass_context=True)
        async def prequel(ctx):
            """Gives top post from /r/prequelmemes."""
            self.logger.info("!prequel called.")
            post = redditclient.prawin("prequelmemes", "top")
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(
                              post["img"], post["title"], post["id"]))

        @client.command(pass_context=True)
        async def pie(ctx):
            """Gives latest Jonathan Pie."""
            self.logger.info("!pie called.")
            pie = feedparser.parse("https://www.youtube.com/feeds/videos.xml?"
                                   "channel_id=UCO79NsDE5FpMowUH1YcBFcA")
            await client.say(pie.entries[0]['link'])

        @client.command(pass_context=True)
        async def dave(ctx):
            self.logger.info("!dave called.")
            if self.host_is_Linux:
                uptime = self.uptimeFunc()
                version = platform.python_version()
                compi = platform.python_compiler()
                # next 3 lines will be depreceated in py3.7; find alternative?
                lindist = platform.linux_distribution()
                lindistn = lindist[0]
                lindistv = lindist[1]
                await client.say("\nHost Uptime: {}"
                                 "\nPython Version: {}\n"
                                 "\nPython Compiler: {}"
                                 "\nDistro: {};v{}".format(uptime,
                                                           version,
                                                           compi,
                                                           lindistn,
                                                           lindistv))
            else:
                self.logger.warning("Host not linux, !dave is not supported.")
                await client.say("Host !=linux; feature coming soon(tm).\n")

        @client.command(pass_context=True)
        async def subhelp(ctx):
            self.logger.info("!subhelp called.")
            await client.say("\n!subreddit help: "
                             "\nSyntax: ```!subreddit sort sub```"
                             "where ```sort``` is reddit sort type:\n"
                             "```-top\n-new\n-rising\n-hot```"
                             "```sub``` is any valid subreddit.\n"
                             "Command should return "
                             "```Invalid subreddit; try again.``` "
                             "if an error is thrown.\n")

        @client.group(pass_context=True)
        async def subreddit(ctx):
            """Provides !subreddit group of cmds."""
            self.logger.info("!subreddit called.")
            if ctx.invoked_subcommand is None:
                await client.say("Invalid subreddit; see !subhelp.")

        @subreddit.command()
        async def top(sub: str):
            """sub needs to be string, or prawin() breaks."""
            self.logger.info("!subreddit top called.")
            post = redditclient.prawin(sub, "top")
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(post["img"],
                                                           post["title"],
                                                           post["id"]))

        @subreddit.command()
        async def new(sub: str):
            self.logger.info("!subreddit new called.")
            post = redditclient.prawin(sub, "new")
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(post["img"],
                                                           post["title"],
                                                           post["id"]))

        @subreddit.command()
        async def rising(sub: str):
            self.logger.info("!subreddit rising called.")
            post = redditclient.prawin(sub, "rising")
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(post["img"],
                                                           post["title"],
                                                           post["id"]))

        @subreddit.command()
        async def hot(sub: str):
            self.logger.info("!subreddit hot called.")
            post = redditclient.prawin(sub, "hot")
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(post["img"],
                                                           post["title"],
                                                           post["id"]))

        client.run(str(self.code))


if __name__ == "__main__":
    raise SystemExit("This is an import file, do not run directly.")
