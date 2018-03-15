import praw
from discord.ext import commands


class Reddit():
    """Class for reddit functions and commands."""
    def __init__(self, bot):
        self.client = bot
        self.prawclient = praw.Reddit(client_id=bot.rid,
                                      client_secret=bot.rsc,
                                      user_agent="dave:v104:t3rr0r_f3rr3t")
        self.fstr = "Image: {}\nTitle = {}\nComments = https://redd.it/{}\n"

    def prawin(self, sub, sort):
        """Praw-Based function, reads from reddit.
           Always returns top/first post for given sort.
        """
        subreddit = self.prawclient.subreddit(str(sub))
        if sort == "top":
            postsort = subreddit.top("day", limit=1)
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

    @commands.group(pass_context=True)
    async def subreddit(self, ctx):
        """Provides !subreddit cmds; see !subreddit help."""
        if ctx.invoked_subcommand is None:
            await self.client.say("Invalid subreddit; see !subreddit help.")

    @subreddit.command()
    async def help(self):
        await self.client.say("\n!subreddit help: "
                              "\nSyntax: ```!subreddit sort sub```"
                              "where ```sort``` is reddit sort type:\n"
                              "```-top\n-new\n-rising\n-hot```"
                              "```sub``` is any valid subreddit.\n"
                              "Command should return "
                              "```Invalid subreddit; try again.``` "
                              "if an error is thrown.\n")

    @subreddit.command()
    async def top(self, sub: str):
        post = self.prawin(sub, "top")
        await self.client.say(self.fstr.format(post["img"],
                                               post["title"],
                                               post["id"]))

    @subreddit.command()
    async def new(self, sub: str):
        post = self.prawin(sub, "new")
        await self.client.say(self.fstr.format(post["img"],
                                               post["title"],
                                               post["id"]))

    @subreddit.command()
    async def rising(self, sub: str):
        post = self.prawin(sub, "rising")
        await self.client.say(self.fstr.format(post["img"],
                                               post["title"],
                                               post["id"]))

    @subreddit.command()
    async def hot(self, sub: str):
        post = self.prawin(sub, "hot")
        await self.client.say(self.fstr.format(post["img"],
                                               post["title"],
                                               post["id"]))

    @commands.command(pass_context=True)
    async def prequel(self, ctx):
        """Gives top post from /r/prequelmemes."""
        post = self.prawin("prequelmemes", "top")
        await self.client.say(self.fstr.format(post["img"],
                                               post["title"],
                                               post["id"]))


def setup(bot):
    bot.add_cog(Reddit(bot))
