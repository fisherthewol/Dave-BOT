import aiohttp
import feedparser
from discord.ext import commands


class RSS:
    """Commands involving feedparser."""
    def __init__(self, bot):
        self.client = bot
        self.session = aiohttp.ClientSession()

    async def getData(self, url):
        resp = await self.session.get(url)
        text = await resp.text()
        resp.close()
        return text

    async def parse(self, data):
        return await self.client.loop.run_in_executor(None,
                                                      feedparser.parse,
                                                      data)

    @commands.command(pass_context=True)
    async def news(self, ctx):
        """Returns top news from bbc and gameinformer."""
        await self.client.send_typing(ctx.message.channel)
        bbc = await self.getData("https://feeds.bbci.co.uk/news/world/europe/rss.xml")
        game = await self.getData("https://www.gameinformer.com/b/mainfeed.aspx?Tags=feature")
        bbc = await self.parse(bbc)
        game = await self.parse(game)
        await self.client.say(bbc.entries[0]["link"])
        await self.client.say(game.entries[0]["link"])

    @commands.command(pass_context=True)
    async def pie(self, ctx):
        """Returns latest Jonathan Pie video."""
        await self.client.send_typing(ctx.message.channel)
        pie = await self.getData("https://www.youtube.com/feeds/videos.xml?channel_id=UCO79NsDE5FpMowUH1YcBFcA")
        pie = await self.parse(pie)
        await self.client.say(pie.entries[0]["link"])


def setup(bot):
    bot.add_cog(RSS(bot))
