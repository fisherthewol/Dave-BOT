import praw

def prawin(sub, sort):
    """Praw-Based function, reads from reddit.
       reddit is a PRAW instance we operate on; Pulls client_id & _secret
       from praw.ini.
       Always returns top/first post for given sort.
    """
    reddit = praw.Reddit('prequelbot',
                         user_agent='davebot:v104:t3rr0r_f3rr3t')
    subreddit = reddit.subreddit(str(sub))
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
