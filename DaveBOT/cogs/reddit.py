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
        # TODO: if subreddit.over18 << This is the check for 18+ subs.
        subreddit = self.prawclient.subreddit(str(sub))
        if sort == "top":
            postsort = subreddit.top(time, limit=1)
        elif sort == "new":
            postsort = subreddit.new(limit=1)
        elif sort == "rising":
            postsort = subreddit.rising(limit=1)
        elif sort == "hot":
            postsort = subreddit.hot(limit=1)
        post = {"title": "", "img": "", "id": ""}
        for submission in postsort:
            post["title"] = str(submission.title)
            post["img"] = str(submission.url)
            post["id"] = str(submission.id)
        return post

    @commands.command()
    async def reddit(self, sub: str, sort: str):
        """Gets first post in <sub>, sorted by <sort>.
           If sort is top, time limit is day.
           Valid sorts are:
           top, new, rising, hot.
        """
        msg = await self.client.say("Getting post.")
        post = self.prawin(sub, sort)
        await self.client.edit_message(msg,
                                       self.fstr.format(post["img"],
                                                        post["title"],
                                                        post["id"]))

    @commands.command()
    async def top(self, sub: str, time: str):
        """Use for !reddit top but with time limit.
           Valid <time>:
           month, day, hour, week, all, year
        """
        msg = await self.client.say("Getting post...")
        post = self.prawin(sub, "top", time=time)
        await self.client.edit_message(msg,
                                       self.fstr.format(post["img"],
                                                        post["title"],
                                                        post["id"]))


def setup(bot):
    bot.add_cog(Reddit(bot))
