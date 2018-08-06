import os
from discord.ext import commands


def adminonly():
    def predicate(ctx):
        return ctx.message.author.id == os.environ.get("adminid")
    return commands.check(predicate)
