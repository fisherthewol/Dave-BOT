import praw
from discord.ext import commands


class Reddit:
    """Class for reddit functions and commands."""
    def __init__(self, bot):
        self.client = bot
        self.prawclient = praw.Reddit(client_id=bot.rid,
                                      client_secret=bot.rsc,
                                      user_agent="dave:v104:t3rr0r_f3rr3t")
        self.fstr = "Image: {}\nTitle = {}\nComments = https://redd.it/{}\n"

    def prawin(self, sub, sort, time="day"):
        """Praw-Based function, reads from reddit.
           Always returns top/first post for given sort.
        """
        subreddit = self.prawclient.subreddit(str(sub))
        prop = {"title": "", "img": "", "id": "", "adult": subreddit.over18}
        if sort == "top":
            posts = subreddit.top(time, limit=1)
        elif sort == "new":
            posts = subreddit.new(limit=1)
        elif sort == "rising":
            posts = subreddit.rising(limit=1)
        elif sort == "hot":
            posts = subreddit.hot(limit=1)
        for post in posts:
            prop["title"] = str(post.title)
            prop["img"] = str(post.url)
            prop["id"] = str(post.id)
        return prop

    @commands.command(pass_context=True)
    async def reddit(self, ctx, sub: str, sort: str):
        """Gets first post in <sub>, sorted by <sort>.
           If sort is top, time limit is day.
           Valid sorts are:
           top, new, rising, hot.
           If the subreddit is 18+, bot will not post in channels without
           "nsfw" in their name.
        """
        msg = await self.client.say("Getting post.")
        post = self.prawin(sub, sort)
        if post["adult"]:
            if "nsfw" in ctx.message.channel.name:
                await self.client.edit_message(msg,
                                               self.fstr.format(post["img"],
                                                                post["title"],
                                                                post["id"]))
            else:
                await self.client.edit_message(msg,
                                               "E: NSFW sub but SFW channel.")
        else:
            await self.client.edit_message(msg,
                                           self.fstr.format(post["img"],
                                                            post["title"],
                                                            post["id"]))

    @commands.command(pass_context=True)
    async def top(self, ctx, sub: str, time: str):
        """Use for !reddit top but with time limit.
           Valid <time>:
           month, day, hour, week, all, year
           If the subreddit is 18+, bot will not post in channels without
           "nsfw" in their name.
        """
        msg = await self.client.say("Getting post...")
        post = self.prawin(sub, "top", time=time)
        if post["adult"]:
            if "nsfw" in ctx.message.channel.name:
                await self.client.edit_message(msg,
                                               self.fstr.format(post["img"],
                                                                post["title"],
                                                                post["id"]))
            else:
                await self.client.edit_message(msg,
                                               "E: NSFW sub but SFW channel.")
        else:
            await self.client.edit_message(msg,
                                           self.fstr.format(post["img"],
                                                            post["title"],
                                                            post["id"]))


def setup(bot):
    bot.add_cog(Reddit(bot))
