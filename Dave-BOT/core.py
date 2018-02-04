import discord, feedparser  # Need installing.
from discord.ext import commands
import logging, os, platform  # Builtins.
from Dave-BOT import redditclient

logging.basicConfig(level=logging.WARNING)

# Set up discord vars.
class Dave:
    """Main class for BOT."""
    def __init__(self, code):
        self.code = code
        self.description = "This is a WIP bot to work discord. Use !bothelp."
        self.bot_prefix = "!"
        global client
        client = commands.Bot(description=description, command_prefix=bot_prefix)

    def uptimeFunc(self):
        """Returns host uptime nicely."""
        if "Linux" in platform.system():
            from datetime import timedelta
            with open("/proc/uptime", "r") as f:
                uptime_seconds = float(f.readline().split()[0])
                uptime_string = str(timedelta(seconds=uptime_seconds))
            return uptime_string
        else:
            return "incomp host."


    def discout(self):
        """Provides discord output. Could be called main(), but not now so as
           to provide future compatability.
        """

        @client.event
        async def on_ready():
            """Outputs on successful launch."""
            print("Login Successful")
            print("Name : {}" .format(client.user.name))
            print("ID : {}" .format(client.user.id))

        @client.command(pass_context=True)
        async def bothelp(ctx):
            """!bothelp, gives help on how to use the bot."""
            print("!bothelp")
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
            print("!news")
            bbc = feedparser.parse("https://feeds.bbci.co.uk/news/world/"
                                   "europe/rss.xml")
            game = feedparser.parse("https://www.gameinformer.com/b/"
                                    "mainfeed.aspx?Tags=feature")
            await client.say(bbc.entries[0]["link"])
            await client.say(game.entries[0]["link"])

        @client.command(pass_context=True)
        async def prequel(ctx):
            """Gives top post from /r/prequelmemes."""
            print("!prequel")
            post = redditclient.prawin("prequelmemes", "top")
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(
                              post["img"], post["title"], post["id"]))

        @client.command(pass_context=True)
        async def pie(ctx):
            """Gives latest Jonathan Pie."""
            print("!pie")
            pie = feedparser.parse("https://www.youtube.com/feeds/videos.xml?"
                                   "channel_id=UCO79NsDE5FpMowUH1YcBFcA")
            await client.say(pie.entries[0]['link'])

        @client.command(pass_context=True)
        async def dave(ctx):
            print("!dave")
            if "linux" in platform.system().lower():
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
                await client.say("\nHost not linux; this feature coming soon.\n")

        @client.command(pass_context=True)
        async def sbrthp(ctx):
            print("!subhelp")
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
            print("!subreddit")
            if ctx.invoked_subcommand is None:
                await client.say("Invalid subreddit; see !sbrthp.")

        @subreddit.command()
        async def top(sub: str):
            """sub needs to be string, or prawin() breaks."""
            print("!subreddit top")
            post = redditclient.prawin(sub, "top")
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(post["img"],
                                                           post["title"],
                                                           post["id"]))

        @subreddit.command()
        async def new(sub: str):
            print("!subreddit new")
            post = redditclient.prawin(sub, "new")
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(post["img"],
                                                           post["title"],
                                                           post["id"]))

        @subreddit.command()
        async def rising(sub: str):
            print("!subreddit rising")
            post = redditclient.prawin(sub, "rising")
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(post["img"],
                                                           post["title"],
                                                           post["id"]))

        @subreddit.command()
        async def hot(sub: str):
            print("!subreddit hot")
            post = redditclient.prawin(sub, "hot")
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(post["img"],
                                                           post["title"],
                                                           post["id"]))

        client.run(str(self.code))


if __name__ == "__main__":
    raise SystemExit("This is an import file, don't run directly.")
