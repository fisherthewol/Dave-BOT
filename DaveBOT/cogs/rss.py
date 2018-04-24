import json
import sys

import aiohttp
import feedparser
from discord.ext import commands


class RSS:
    """Commands involving feedparser."""
    def __init__(self, bot):
        self.client = bot
        with open("data/feeds.json") as op:
            self.feeds = json.load(op)
        self.session = aiohttp.ClientSession()

    def __unload(self):
        self.session.close()

    async def getData(self, url):
        resp = await self.session.get(url)
        text = await resp.text()
        resp.close()
        return text

    async def parse(self, data):
        return await self.client.loop.run_in_executor(None,
                                                      feedparser.parse,
                                                      data)

    async def on_command_error(self, error, ctx):
        """Event triggered on error raise."""
        if hasattr(ctx.command, "on_error"):
            return
        error = getattr(error, "original", error)
        if isinstance(error, commands.DisabledCommand):
            return await self.client.send_message(ctx.message.channel,
                                                  "{} is disabled.".format(ctx.command))
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await self.client.send_message(ctx.author,
                                                      "{} can't be used in DMs.".format(ctx.command))
            except:
                pass
        # If it's not one of these, print traceback:
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        return await self.client.send_message(ctx.message.channel,
                                              "Error in command; issue has been logged.")


    @commands.command(pass_context=True)
    async def news(self, ctx):
        """Returns top news from bbc and gameinformer."""
        for feed in self.feeds:
            await self.client.send_typing(ctx.message.channel)
            data = await self.getData(feed)
            news = await self.parse(data)
            await self.client.say(news.entries[0]["link"])

    @commands.command(pass_context=True)
    async def pie(self, ctx):
        """Returns latest Jonathan Pie video."""
        await self.client.send_typing(ctx.message.channel)
        pie = await self.getData("https://www.youtube.com/feeds/videos.xml?channel_id=UCO79NsDE5FpMowUH1YcBFcA")
        pie = await self.parse(pie)
        await self.client.say(pie.entries[0]["link"])


def setup(bot):
    bot.add_cog(RSS(bot))
