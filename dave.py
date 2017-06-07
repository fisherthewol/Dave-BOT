import discord, feedparser, datetime, praw, time
from discord.ext import commands

global a
a = 0

def logger (msg):
    ti = time.strftime("%H:%M:%S")
    da = time.strftime("%Y%m%d")
    if a == 0:
        with open("log.txt", "w+") as f:
            f.write("{}; {}: {}\n".format(da, ti, msg))
    elif a == 1:
        with open("log.txt", "a+") as f:
            f.write("{}; {}: {}\n".format(da, ti, msg))


class Dave:
    """Main class for BOT"""
    def __init__(self):
        self.a = 0
        self.topattr = {"title": "",
                        "img": "",
                        "id": ""}

    now = datetime.datetime.now()
    h = now.hour
    description = "This is a WIP bot to work discord."
    bot_prefix = "!"
    client = commands.Bot(description=description, command_prefix=bot_prefix)
    reddit = praw.Reddit('prequelbot',
                         user_agent='davebot:v1:t3rr0r_f3rr3t')
    subreddit = reddit.subreddit("prequelmemes")


    def prawin(self):
        topsub = subreddit.top("day", limit=1)
        oldsub = {"title": "", "img": "", "id": ""}
        self.topattr = {"title": "", "img": "", "id": ""}
        if self.a == 0:
            for submission in topsub:
                oldsub["title"] = str(submission.title)
                oldsub["img"] = str(submission.url)
                oldsub["id"] = str(submission.id)
            logger("init, returning top now")
            print("init, returning top now")
            return oldsub

    def discout(self):
        @client.event
        async def on_ready():
            print("Login Successful")
            print("Name : {}" .format(client.user.name))
            print("ID : {}" .format(client.user.id))

        @client.command(pass_context=True)
        async def help(ctx):
            print("!help")
            await client.say("\nAvailible commands:\n"
                             "!help -- What you're seeing now.\n"
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
            # Always get top post at time.
            self.a= 0
            topbot = prawin()
            await client.say(" \nImage: {}\nTitle = {}\nComments = "
                             "https://redd.it/{}\n".format(
                             topbot["img"],topbot["title"],topbot["id"]))

        client.run("blank")


if __name__ == "__main__":
    logger("Main File; discout is being called.")
    print("Main File; discout is being called.")
    main = Dave()
    main.discout()
