from discord.ext import commands


class Memes():
    """Meme commands."""
    def __init__(self, bot):
        self.client = bot
        self.known = {"hams": "data/hams.txt"}

    @commands.command(pass_context=True)
    async def memed(self, ctx, name: str):
        """Replies with file of known meme."""
        loadmsg = await self.client.say("Finding meme...")
        if name in self.known:
            await self.client.edit_message(loadmsg, "Meme found, uploading!")
            filename = self.known[name]
            chan = ctx.message.channel
            with open(filename, "rb") as tt:
                await self.client.send_file(chan, tt)
            await self.client.edit_message(loadmsg, "Meme:")
        else:
            self.client.edit_message(loadmsg, "Meme not found, try again!")


def setup(bot):
    bot.add_cog(Memes(bot))
