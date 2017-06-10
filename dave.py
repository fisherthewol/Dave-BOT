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
    def prawin(self,sub,sort):
        """Praw-Based function for /r/prequelmemes."""
        """
           reddit is a PRAW instance we operate on;
           Pulls client_id & _secret from praw.ini.
        """
        reddit = praw.Reddit('prequelbot',
                             user_agent='davebot:v1.2:t3rr0r_f3rr3t')
        subreddit = reddit.subreddit(sub)
        topsub = subreddit.sort("day", limit=1)
        post = {"title": "", "img": "", "id": ""}
        for submission in topsub:
            post["title"] = str(submission.title)
            post["img"] = str(submission.url)
            post["id"] = str(submission.id)
        return post

    def discout(self):
        """Provides discord output."""

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
            await client.say("\nAvailible commands:\n"
                             "!bothelp -- What you're seeing now.\n"
                             "!news -- See top news stories now.\n"
                             "!prequel -- See day's top post from "
                             "/r/prequelmemes.\n"
                             "!pie -- get latest JPie Vid.\n")

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
            post = main.prawin(prequelmemes, top)
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(
                             post["img"],post["title"],post["id"]))

        # V provides !pie command.
        @client.command(pass_context=True)
        async def pie(ctx):
            print("!pie")
            pie = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCO79NsDE5FpMowUH1YcBFcA")
            await client.say(pie.entries[0]['link'])

        # V provides !subreddit command.
        @client.group(pass_context=True)
        async def subreddit(ctx):
            print("!subreddit")
            if ctx.invoked_subcommand is None:
                await client.say("Invalid subreddit; try again.")

        @subreddit.command()
        async def top(sub: str):
            print("!subreddit top")
            post = main.prawin(sub,top)
            await client.say("Image: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(
                             post["img"],post["title"],post["id"]))


        client.run("MzIxNjgwNDExNDgwNjg2NTk0.DB1Q0g.oVVKQQHpdznXqjVhHN8J-cf3DA8")


if __name__ == "__main__":
    print("Main File; discout is being called.")
    main = Dave()
    main.discout()
