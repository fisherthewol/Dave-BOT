from discord.ext import commands
from DaveBOT import checks


class Admin:
    """Admin-only commands."""
    def __init__(self, bot):
        self.client = bot
        global adid
        adid = self.client.adid

    @commands.command(hidden=True)
    @checks.alloweduser(adid)
    async def load(self, *, module: str):
        """Load a module."""
        try:
            self.client.load_extension(module)
        except Exception as e:
            await self.client.say(f"{type(e).__name__}: {e}")
        else:
            await self.client.say("Module loaded.")

    @commands.command(hidden=True)
    @checks.alloweduser(adid)
    async def unload(self, *, module: str):
        """Unload a module."""
        try:
            self.client.unload_extension(module)
        except Exception as e:
            await self.client.say(f"{type(e).__name__}: {e}")
        else:
            await self.client.say("Module unloaded.")

    @commands.command(hidden=True)
    @checks.alloweduser(adid)
    async def reload(self, *, module: str):
        """Reload a module."""
        try:
            self.client.unload_extension(module)
            self.client.load_extension(module)
        except Exception as e:
            await self.client.say(f"{type(e).__name__}: {e}")
        else:
            await self.client.say("Module unloaded.")


def setup(bot):
    bot.add_cog(Admin(bot))
