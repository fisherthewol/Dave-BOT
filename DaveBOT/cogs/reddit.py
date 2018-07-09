import datetime

import praw
import discord
from discord.ext import commands


class Reddit:
    """Reddit functions and commands."""
    def __init__(self, bot):
        self.client = bot
        self.prawclient = praw.Reddit(client_id=bot.rid,
                                      client_secret=bot.rsc,
                                      user_agent="dave:testing:t3rr0r_f3rr3t")
        self.knownExtensions = [".jpg", ".jpeg", ".png",
                                ".webp", ".webm", ".gif", ".svg"]

    async def genembed(self, post):
        e = discord.Embed(title=f"{str(post.title)}",
                          type="rich",
                          url=post.shortlink,
                          colour=0xFF5700,
                          timestamp=datetime.datetime.utcnow())
        e.set_footer(text=f"From /r/{str(post.subreddit.display_name)}")
        if post.is_self:
            e.description = f"{post.selftext[0:len(post.selftext) // 4]}..."
            return e
        else:
            for ext in self.knownExtensions:
                if ext in post.url:
                    image = True
                    break
                else:
                    image = False
                    continue
            if image:
                e.set_image(url=post.url)
                return e
            else:
                e.description = post.url
                return e

    def prawin(self, sub, sort, time="day"):
        """Praw-Based function, reads from reddit.
           Always returns top/first post for given sort.
        """
        subreddit = self.prawclient.subreddit(str(sub))
        functions = {"top": subreddit.top(time, limit=1),
                     "new": subreddit.new(limit=1),
                     "rising": subreddit.rising(limit=1),
                     "hot": subreddit.hot(limit=1)}
        posts = functions.get(sort)
        if posts:
            for post in posts:
                return (post, subreddit.over18)
        else:
            return None

    async def nsfwGuard(self, post, channelname):
        """Provides nsfw guard."""
        if post is None:
            return "Error: invalid sort."
        elif post[1]:
            if "nsfw" in channelname:
                return await self.genembed(post[0])
            else:
                return "E: Subreddit is NSFW, but command is from SFW channel."
        else:
            return await self.genembed(post[0])

    @commands.command(pass_context=True)
    async def reddit(self, ctx, sub: str, sort: str):
        """Gets first post in <sub>, sorted by <sort>.
           If sort is top, time limit is day.
           Valid sorts are:
           top, new, rising, hot.
           If the subreddit is 18+, bot will not post in channels without
           "nsfw" in their name.
        """
        channel = ctx.message.channel
        await self.client.send_typing(channel)
        post = await self.client.loop.run_in_executor(None,
                                                      self.prawin,
                                                      sub,
                                                      sort)
        msg = await self.nsfwGuard(post, channel.name)
        if type(msg) is discord.Embed:
            await self.client.say(embed=msg)
        else:
            await self.client.say(msg)

    @commands.command(pass_context=True)
    async def top(self, ctx, sub: str, time: str):
        """Use for !reddit top but with time limit.
           Valid <time>:
           month, day, hour, week, all, year
           If the subreddit is 18+, bot will not post in channels without
           "nsfw" in their name.
        """
        channel = ctx.message.channel
        await self.client.send_typing(channel)
        post = await self.client.loop.run_in_executor(None,
                                                      self.prawin,
                                                      sub,
                                                      "top",
                                                      time)
        msg = await self.nsfwGuard(post, channel.name)
        if type(msg) is discord.Embed:
            await self.client.say(embed=msg)
        else:
            await self.client.say(msg)

    @commands.command(pass_context=True)
    async def prequel(self, ctx):
        """Get top post of the day from /r/prequelmemes."""
        await self.client.send_typing(ctx.message.channel)
        post = await self.client.loop.run_in_executor(None,
                                                      self.prawin,
                                                      "prequelmemes",
                                                      "top",
                                                      "day")
        msg = await self.nsfwGuard(post, ctx.message.channel)
        if type(msg) is discord.Embed:
            await self.client.say(embed=msg)
        else:
            await self.client.say(msg)


def setup(bot):
    bot.add_cog(Reddit(bot))
