import discord, feedparser, datetime, praw,
from discord.ext import commands

now = datetime.datetime.now()
h = now.hour
description = "This is a WIP bot to work discord."
bot_prefix = "!"
client = commands.Bot(description=description, command_prefix=bot_prefix)

reddit = praw.Reddit('prequelbot',
                     user_agent='prequelbot:v{}:t3rr0r_f3rr3t'.format(__version__))
subreddit = reddit.subreddit("prequelmemes")
global a
a = 0
global topattr
topattr = {"title": "", "img": "", "id": ""}


def prawin():
    topsub = subreddit.top("day", limit=1)
    oldsub = {"title": "", "img": "", "id": ""}
    topattr = {"title": "", "img": "", "id": ""}
    global a
    if a == 0:
        for submission in topsub:
            oldsub["title"] = str(submission.title)
            oldsub["img"] = str(submission.url)
            oldsub["id"] = str(submission.id)
        logger("init, returning top now")
        print("init, returning top now")
        return oldsub


def discout():
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
        global a
        a = 0
        topbot = prawin()
        await client.say(" \nImage: {}\nTitle = {}\nComments = "
                         "https://redd.it/{}\n".format(
                         topbot["img"],topbot["title"],topbot["id"]))

    client.run("inserthere")


if __name__ == "__main__":
    logger("Main File; discout is being called.")
    print("Main File; discout is being called.")
    try:
        discout()
    except:
        logger("Error while calling/in main(); exiting.")
        print("Error while calling/in main(); exiting.")
        sys.exit()
