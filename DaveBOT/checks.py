from discord.ext import commands


def alloweduser(userid: str):
    def predicate(ctx):
        return ctx.message.author.id == userid
    return commands.check(predicate)
