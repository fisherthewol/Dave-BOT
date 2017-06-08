import discord, feedparser, praw  # Need installing.
import logging  # Builtins.
from discord.ext import commands

logging.basicConfig(level=logging.WARNING)

# Sets up discord stuff.
description = "This is a WIP bot to work discord. Use !bothelp."
bot_prefix = "!"
global client
client = commands.Bot(description=description, command_prefix=bot_prefix)

# Initilaises a praw isntance
reddit = praw.Reddit('prequelbot',
                     user_agent='davebot:v1.1:t3rr0r_f3rr3t')
subreddit = reddit.subreddit("prequelmemes")


class Dave:
    """Main class for BOT."""
    def prawin(self):
        """Praw-Based function for /r/prequelmemes."""
        topsub = subreddit.top("day", limit=1)
        post = {"title": "", "img": "", "id": ""}
        for submission in topsub:
            post["title"] = str(submission.title)
            post["img"] = str(submission.url)
            post["id"] = str(submission.id)
        return post

    def discout(self):
        """Provides disocrd output."""
        @client.event
        async def on_ready():
            print("Login Successful")
            print("Name : {}" .format(client.user.name))
            print("ID : {}" .format(client.user.id))

        @client.command(pass_context=True)
        async def bothelp(ctx):
            print("!bothelp")
            await client.say("\nAvailible commands:\n"
                             "!bothelp -- What you're seeing now.\n"
                             "!news -- See top news stories now.\n"
                             "!prequel -- See top post from /r/prequelmemes.\n")

        @client.command(pass_context=True)
        async def news(ctx):
            print("!news")
            bbc = feedparser.parse("https://www.reddit.com/domain/bbc.com/"
                                   "top/.rss")
            game = feedparser.parse("https://www.gameinformer.com/b/mainfeed"
                                    ".aspx?Tags=feature")
            await client.say(bbc.entries[0]['link'])
            await client.say(game.entries[0]['link'])

        @client.command(pass_context=True)
        async def prequel(ctx):
            print("!prequel")
            topbot = main.prawin()
            await client.say(" \nImage: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(
                             topbot["img"],topbot["title"],topbot["id"]))

        client.run("")


if __name__ == "__main__":
    print("Main File; discout is being called.")
    main = Dave()
    main.discout()
