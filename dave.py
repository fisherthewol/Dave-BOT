import discord, feedparser, praw  # Need installing.
import logging  # Builtins.
from discord.ext import commands

logging.basicConfig(level=logging.WARNING)

# Sets up discord stuff.
description = "This is a WIP bot to work discord. Use !bothelp."
bot_prefix = "!"
global client
client = commands.Bot(description=description, command_prefix=bot_prefix)


class Dave:
    """Main class for BOT."""
    def prawin(self, sub, sort):
        """Praw-Based function, reads from reddit.
           reddit is a PRAW instance we operate on; Pulls client_id & _secret
           from praw.ini.
           Always returns top/first post for given sort.
        """
        reddit = praw.Reddit('prequelbot',
                             user_agent='davebot:v1.3:t3rr0r_f3rr3t')
        subreddit = reddit.subreddit(str(sub))
        if sort == "top":
            postsort = subreddit.top("day", limit=1)
        elif sort == "new":
            postsort = subreddit.new(limit=1)
        elif sort == "rising":
            postsort = subreddit.rising(limit=1)
        elif sort == "hot":
            postsort = subreddit.hot(limit=1)
        post = {"title": "", "img": "", "id": ""}
        for submission in postsort:
            post["title"] = str(submission.title)
            post["img"] = str(submission.url)
            post["id"] = str(submission.id)
        return post

    def uptimeFunc(self):
        """Returns host uptime nicely. Breaks if not *nix."""
        from datetime import timedelta
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds=uptime_seconds))
        return uptime_string

    def discout(self):
        """Provides discord output. Could be called main(), but not now so as
           to provide future compatability.
        """

        # V provides output on Successful Launch.
        @client.event
        async def on_ready():
            print("Login Successful")
            print("Name : {}" .format(client.user.name))
            print("ID : {}" .format(client.user.id))

        # V provides !bothelp command.
        @client.command(pass_context=True)
        async def bothelp(ctx):
            print("!bothelp")
            await client.say("\nAvailible commands:"
                             "\n!bothelp -- What you're seeing now."
                             "\n!news -- See top news stories now."
                             "\n!prequel -- See theday's top post (so far) "
                             "from /r/prequelmemes."
                             "\n!pie -- get latest JPie Vid."
                             "\n!subreddit -- see !subreddit help."
                             "\n!dave -- get bot stats."
                             "\n!fparse -- see !fparse help.")

        # V provides !news command.
        @client.command(pass_context=True)
        async def news(ctx):
            print("!news")
            bbc = feedparser.parse("https://www.reddit.com/domain/bbc.com/"
                                   "top/.rss")
            game = feedparser.parse("https://www.gameinformer.com/b/mainfeed"
                                    ".aspx?Tags=feature")
            await client.say(bbc.entries[0]['link'])
            await client.say(game.entries[0]['link'])

        # V provides !prequel command.
        @client.command(pass_context=True)
        async def prequel(ctx):
            print("!prequel")
            post = main.prawin("prequelmemes", "top")
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(
                              post["img"], post["title"], post["id"]))

        # V provides !pie command.
        @client.command(pass_context=True)
        async def pie(ctx):
            print("!pie")
            pie = feedparser.parse("https://www.youtube.com/feeds/videos.xml?"
                                   "channel_id=UCO79NsDE5FpMowUH1YcBFcA")
            await client.say(pie.entries[0]['link'])

        # V provides !dave command.
        @client.command(pass_context=True)
        async def dave(ctx):
            print("!dave")
            import platform
            if "Linux" in platform.system():
                uptime = main.uptimeFunc()
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
                await client.say("\nHost incompatible with this function.\n")

        # V provides !subreddit command group.
        @client.group(pass_context=True)
        async def subreddit(ctx):
            print("!subreddit")
            if ctx.invoked_subcommand is None:
                await client.say("Invalid subreddit; try again.")

        @subreddit.command()
        async def help(ctx):
            print("!subreddit help")
            await client.say("\n!subreddit help:"
                             "\nSyntax: ```!subreddit sort sub```"
                             "\n```sort is reddit sort type:"
                             "\n-top\n-new\n-rising\n-hot"
                             "\n sub is any valid subreddit; should return "
                             "```Invalid subreddit; try again.``` if an error"
                             "is thrown.\n")

        @subreddit.command()
        async def top(sub: str):
            # ^ sub needs to be string, or prawin() breaks.
            print("!subreddit top")
            post = main.prawin(sub, "top")
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(post["img"],
                                                           post["title"],
                                                           post["id"]))

        @subreddit.command()
        async def new(sub: str):
            print("!subreddit new")
            post = main.prawin(sub, "new")
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(post["img"],
                                                           post["title"],
                                                           post["id"]))

        @subreddit.command()
        async def rising(sub: str):
            print("!subreddit rising")
            post = main.prawin(sub, "rising")
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(post["img"],
                                                           post["title"],
                                                           post["id"]))

        @subreddit.command()
        async def hot(sub: str):
            print("!subreddit hot")
            post = main.prawin(sub, "hot")
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(post["img"],
                                                           post["title"],
                                                           post["id"]))

        # V ALWAYS REMOVE THIS BEFORE COMMITTING PLEASE.
        client.run("")


if __name__ == "__main__":
    print("Main File; discout is being called.")
    main = Dave()
    main.discout()
