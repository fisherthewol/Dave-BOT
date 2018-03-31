import praw
from discord.ext import commands


class Reddit:
    """Class for reddit functions and commands."""
    def __init__(self, bot):
        self.client = bot
        self.prawclient = praw.Reddit(client_id=bot.rid,
                                      client_secret=bot.rsc,
                                      user_agent="dave:testing:t3rr0r_f3rr3t")
        self.fstr = "Content: {}\nTitle = {}\nComments = https://redd.it/{}\n"

    def prawin(self, sub, sort, time="day"):
        """Praw-Based function, reads from reddit.
           Always returns top/first post for given sort.
        """
        subreddit = self.prawclient.subreddit(str(sub))
        functions = {"top": subreddit.top(time, limit=1),
                     "new": subreddit.new(limit=1),
                     "rising": subreddit.rising(limit=1),
                     "hot": subreddit.hot(limit=1)}
        posts = functions[sort]
        prop = {"title": "", "img": "", "id": "", "adult": subreddit.over18}
        for post in posts:
            prop["title"] = str(post.title)
            prop["img"] = str(post.url)
            prop["id"] = str(post.id)
        return prop

    def nsfwGuard(self, post, channelname):
        """Provides nsfw guard."""
        if post["adult"]:
            if "nsfw" in channelname:
                return self.fstr.format(post["img"],
                                        post["title"],
                                        post["id"])
            else:
                return "E: Subreddit is NSFW, but command is from SFW channel."
        else:
            return self.fstr.format(post["img"],
                                    post["title"],
                                    post["id"])

    @commands.command(pass_context=True)
    async def reddit(self, ctx, sub: str, sort: str):
        """Gets first post in <sub>, sorted by <sort>.
           If sort is top, time limit is day.
           Valid sorts are:
           top, new, rising, hot.
           If the subreddit is 18+, bot will not post in channels without
           "nsfw" in their name.
        """
        msg = await self.client.say("Getting post...")
        post = await self.client.loop.run_in_executor(None,
                                                      self.prawin,
                                                      sub,
                                                      sort)
        reply = await self.client.loop.run_in_executor(None,
                                                       self.nsfwGuard,
                                                       post,
                                                       ctx.message.channel.name)
        await self.client.edit_message(msg, reply)

    @commands.command(pass_context=True)
    async def top(self, ctx, sub: str, time: str):
        """Use for !reddit top but with time limit.
           Valid <time>:
           month, day, hour, week, all, year
           If the subreddit is 18+, bot will not post in channels without
           "nsfw" in their name.
        """
        msg = await self.client.say("Getting post...")
        post = await self.client.loop.run_in_executor(None,
                                                      self.prawin,
                                                      sub,
                                                      "top",
                                                      time)
        reply = await self.client.loop.run_in_executor(None,
                                                       self.nsfwGuard,
                                                       post,
                                                       ctx.message.channel.name)
        await self.client.edit_message(msg, reply)

    @commands.command()
    async def prequel(self):
        """Get top post from /r/prequelmemes."""
        msg = await self.client.say("Getting post...")
        post = await self.client.loop.run_in_executor(None,
                                                      self.prawin,
                                                      "prequelmemes",
                                                      "top",
                                                      "day")
        await self.client.edit_message(msg,
                                       self.fstr.format(post["img"],
                                                        post["title"],
                                                        post["id"]))


def setup(bot):
    bot.add_cog(Reddit(bot))
