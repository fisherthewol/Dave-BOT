import json
import sys
import traceback

from discord.ext import commands


class Memes():
    """Meme commands."""
    def __init__(self, bot):
        self.client = bot
        with open("data/memes.json") as op:
            self.known = json.load(op)

#    async def on_command_error(self, error, ctx):
#        """Event triggered on error raise."""
#        if hasattr(ctx.command, "on_error"):
#            return
#        error = getattr(error, "original", error)
#        if isinstance(error, commands.DisabledCommand):
#            return await self.client.send_message(ctx.message.channel,
#                                                  "{} is disabled.".format(ctx.command))
#        elif isinstance(error, commands.NoPrivateMessage):
#            try:
#                return await self.client.send_message(ctx.author,
#                                                      "{} can't be used in DMs.".format(ctx.command))
#            except:
#                pass
#        # If it's not one of these, print traceback:
#        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
#        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
#        return await self.client.send_message(ctx.message.channel,
#                                              "Error in command; issue has been logged.")

    @commands.group(pass_context=True)
    async def meme(self, ctx):
        """Provides !meme cmds, see !help meme"""
        if ctx.invoked_subcommand is None:
            await self.client.say("Unrecognised command; see !help meme")

    @meme.command(pass_context=True)
    async def lst(self, ctx):
        """List all known memes. Usage: !meme lst"""
        await self.client.send_typing(ctx.message.channel)
        await self.client.say("Listing memes:")
        await self.client.say(", ".join(self.known.keys()))

    @meme.command(pass_context=True)
    async def f(self, ctx, name: str):
        """Replies with file of known meme."""
        await self.client.send_typing(ctx.message.channel)
        if name in self.known:
            await self.client.say("Meme found, uploading!")
            filename = self.known.get(name)[0]
            if filename:
                await self.client.say("Meme:")
                with open(filename, "rb") as t:
                    await self.client.send_file(ctx.message.channel, t)
            else:
                await self.client.say("Meme doesn't have a file.")
        else:
            self.client.say("Meme not found.")

    @meme.command(pass_context=True)
    async def yt(self, ctx, name: str):
        """Replies with youtube link of known meme."""
        await self.client.send_typing(ctx.message.channel)
        if name in self.known:
            msg = await self.client.say("Meme found, attempting to link...")
            link = self.known[name][1]
            if link:
                await self.client.edit_message(msg, str(link))
            else:
                await self.client.edit_message(msg, "Meme doesn't have a youtube link.")
        else:
            self.client.edit_message(msg, "Meme not found, try again!")


def setup(bot):
    bot.add_cog(Memes(bot))
