from discord.ext import commands


def adminonly():
    def predicate(ctx):
        return ctx.message.author.id == "193471911878066176"
    return commands.check(predicate)
