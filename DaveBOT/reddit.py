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
            raise NotImplementedError

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
