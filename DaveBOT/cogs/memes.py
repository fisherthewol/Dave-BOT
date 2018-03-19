from discord.ext import commands


class Memes():
    """Meme commands."""
    def __init__(self, bot):
        self.client = bot
        self.known = {"hams": ["data/hms.txt", "https://youtu.be/mkX3dO6KN54"],
                      "can't": [0, "https://youtu.be/wKbU8B-QVZk"]}

    @commands.group(pass_context=True)
    async def meme(self, ctx):
        """Provides !meme cmds, see !help meme"""
        if ctx.invoked_subcommand is None:
            await self.client.say("Unrecognised command; see !help meme")

    @meme.command(pass_context=True)
    async def lst(self, ctx):
        """List all known memes. Usage: !meme lst"""
        await self.client.say("Listing memes:")
        await self.client.say(str(self.known))

    @meme.command(pass_context=True)
    async def f(self, ctx, name: str):
        """Replies with file of known meme."""
        msg = await self.client.say("Finding meme...")
        if name in self.known:
            await self.client.edit_message(msg, "Meme found, uploading!")
            filename = self.known[name][0]
            if filename:
                chan = ctx.message.channel
                with open(filename, "rb") as tt:
                    await self.client.send_file(chan, tt)
                await self.client.edit_message(msg, "Meme:")
            else:
                await self.client.edit_message(msg,
                                               "Meme doesn't have a file.")
        else:
            self.client.edit_message(msg, "Meme not found, try again!")

    @meme.command(pass_context=True)
    async def yt(self, ctx, name: str):
        """Replies with youtube link of known meme."""
        msg = await self.client.say("Finding meme...")
        if name in self.known:
            await self.client.edit_message(msg, "Meme found, linking!")
            link = self.known[name][1]
            if link:
                await self.client.edit_message(msg,
                                               str(link))
            else:
                await self.client.edit_message(msg,
                                               "Meme doesn't have a yt.")
        else:
            self.client.edit_message(msg, "Meme not found, try again!")


def setup(bot):
    bot.add_cog(Memes(bot))
