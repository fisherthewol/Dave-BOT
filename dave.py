import discord, feedparser, datetime
from discord.ext import commands

now = datetime.datetime.now()
h = now.hour
description = "This is a WIP bot to replace newsreaders."
bot_prefix = "!"
client = commands.Bot(description=description, command_prefix=bot_prefix)

@client.event
async def on_ready():
    print("Login Successful")
    print("Name : {}" .format(client.user.name))
    print("ID : {}" .format(client.user.id))

@client.command(pass_context=True)
async def helpnews(ctx):
    print("!helpnews")
    await client.say("\nAvailible commands:\n"
                     "!helpnews -- What you're seeing now.\n"
                     "!news         -- See top news stories now.\n")

@client.command(pass_context=True)
async def news(ctx):
    print("!news")
    bbc = feedparser.parse("https://www.reddit.com/domain/bbc.com/"
                           "top/.rss")
    game = feedparser.parse("https://www.gameinformer.com/b/mainfeed"
                            ".aspx?Tags=feature")
    await client.say(bbc.entries[0]['link'])
    await client.say(game.entries[0]['link'])

#@client.event
#async def timer():
#    while True:
#        if(h == 9) or (h == 18) or (h == 0) or (h == 3):
#            bbc = feedparser.parse("https://www.reddit.com/domain/bbc.com/"
#                                   "top/.rss")
#            game = feedparser.parse("https://www.gameinformer.com/b/mainfeed"
#                                    ".aspx?Tags=feature")
#            await client.say(bbc.entries[0]['link'])
#            await client.say(game.entries[0]['link'])

client.run("")
