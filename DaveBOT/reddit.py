import praw


class Reddit():
    """Class for reddit functions and commands."""
    def __init__(self, reddit_id, reddit_sc, discli, ini=False):
        self.id = reddit_id
        self.client = discli
        if not ini:
            self.prawclient = praw.Reddit(client_id=self.id,
                                          client_secret=reddit_sc,
                                          user_agent="dave:v104:t3rr0r_f3rr3t")
        else:
            raise NotImplementedError("Not implmented ini sites.")

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

    def redditCommands(self):
        """Discord commands."""
        @self.client.group(pass_context=True)
        async def subreddit(ctx):
            """Provides !subreddit group of cmds; see !subhelp."""
            self.logger.info("!subreddit called.")
            if ctx.invoked_subcommand is None:
                await self.client.say("Invalid subreddit; see !subhelp.")

        @subreddit.command()
        async def top(sub: str):
            self.logger.info("!subreddit top called.")
            post = self.reddit.prawin(sub, "top")
            await self.client.say("Image: {}\nTitle = {}\nComments = "
                                  "https://redd.it/{}\n".format(post["img"],
                                                                post["title"],
                                                                post["id"]))

        @subreddit.command()
        async def new(sub: str):
            self.logger.info("!subreddit new called.")
            post = self.reddit.prawin(sub, "new")
            await self.client.say("Image: {}\nTitle = {}\nComments = "
                                  "https://redd.it/{}\n".format(post["img"],
                                                                post["title"],
                                                                post["id"]))

        @subreddit.command()
        async def rising(sub: str):
            self.logger.info("!subreddit rising called.")
            post = self.reddit.prawin(sub, "rising")
            await self.client.say("Image: {}\nTitle = {}\nComments = "
                                  "https://redd.it/{}\n".format(post["img"],
                                                                post["title"],
                                                                post["id"]))

        @subreddit.command()
        async def hot(sub: str):
            self.logger.info("!subreddit hot called.")
            post = self.reddit.prawin(sub, "hot")
            await self.client.say("Image: {}\nTitle = {}\nComments = "
                                  "https://redd.it/{}\n".format(post["img"],
                                                                post["title"],
                                                                post["id"]))

        @self.client.command(pass_context=True)
        async def prequel(ctx):
            """Gives top post from /r/prequelmemes."""
            self.logger.info("!prequel called.")
            post = self.reddit.prawin("prequelmemes", "top")
            await self.client.say("Image: {}\nTitle = {}\nComments = "
                                  "https://redd.it/{}\n".format(
                                   post["img"], post["title"], post["id"]))
