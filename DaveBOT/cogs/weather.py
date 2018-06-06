import json
import re
import sys
import traceback

import aiohttp
from discord.ext import commands


class Weather:
    """Weather functions and commands."""
    def __init__(self, bot):
        self.client = bot
        self.key = bot.wk
        self.session = aiohttp.ClientSession()
        self.baseurl = "https://api.openweathermap.org/data/2.5/weather?"
        self.nameurl = self.baseurl + "q={},{}&appid=" + self.key
        self.idurl = self.baseurl + "id={}&appid=" + self.key
        self.zipurl = self.baseurl + "zip={},us&appid=" + self.key
        self.regcomp = re.compile(r"\d{5}([ \-]\d{4})?")
        with open("data/cond.json") as op:
            self.conditions = json.load(op)

    def __unload(self):
        self.session.close()

    async def getJson(self, url):
        resp = await self.session.get(url)
        jsn = await resp.json()
        resp.close()
        return jsn

    def wSF(self, jtf):
        cond = self.retcond(str(jtf["weather"][0]["id"]))
        temp = jtf["main"]["temp"] - 273.15
        return ("Weather in {}, {}:"
                "\nConditions: {}"
                "\nTemp: {} °C"
                "\nHumidity: {} %"
                "\nPressure: {} hPa"
                "\nWind Speed: {} m/s".format(jtf["name"],
                                              jtf["sys"]["country"],
                                              cond,
                                              round(temp, 2),
                                              jtf["main"]["humidity"],
                                              jtf["main"]["pressure"],
                                              jtf["wind"]["speed"]))

    def retcond(self, conditionid):
        retval = ""
        try:
            retval = self.conditions[conditionid]
        except KeyError:
            return None
        return retval["label"].title()

    async def by_cityname(self, cityname, country):
        """Returns based on name and country."""
        url = self.nameurl.format(cityname, country)
        return await self.getJson(url)

    async def by_id(self, cityid):
        """Returns based on city id."""
        url = self.idurl.format(cityid)
        return await self.getJson(url)

    async def by_zip(self, zipcode):
        if self.regcomp.match(str(zipcode)):
            url = self.zipurl.format(zipcode)
            return await self.getJson(url)
        else:
            raise ValueError("Zipcode is invalid (wrong or none-US).")

    async def on_command_error(self, error, ctx):
        """Event triggered on error raise."""
        if hasattr(ctx.command, "on_error"):
            return

        error = getattr(error, "original", error)

        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await self.client.send_message(ctx.author,
                                                      "{} can't be used in DMs.".format(ctx.command))
            except:
                pass

        if isinstance(error, commands.MissingRequiredArgument):
            params = ctx.command.clean_params.keys()
            for param in params:
                if param in error.args[0]:
                    frstparam = param
            missedparams = []
            for i in reversed(params):
                missedparams.append(i)
                if i == frstparam:
                    break
            return await self.client.send_message(ctx.message.channel,
                                                  "Error: missing parameters: {}".format(list(reversed(missedparams))))
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        return await self.client.send_message(ctx.message.channel,
                                              "Error in command; issue has been logged.")

    @commands.group(pass_context=True)
    async def weather(self, ctx):
        """Provides weather data."""
        if ctx.invoked_subcommand is None:
            await self.client.say("Unrecognised command; see !help weather.")

    @weather.command(pass_context=True)
    async def city(self, ctx, city: str, country: str):
        """Gets weather for city given."""
        await self.client.send_typing(ctx.message.channel)
        retjs = await self.by_cityname(city, country)
        if retjs["cod"] == "404":
            await self.client.say("Error: City not found.")
        else:
            msg = await self.client.loop.run_in_executor(None,
                                                         self.wSF,
                                                         retjs)
            await self.client.say(msg)

    @weather.command(pass_context=True)
    async def id(self, ctx, cityid: int):
        """Gets weather for city with valid <id>.
           IDs can be found at
           http://bulk.openweathermap.org/sample/city.list.json.gz
        """
        await self.client.send_typing(ctx.message.channel)
        retjs = await self.by_id(cityid)
        if retjs["cod"] == "404":
            await self.client.edit_message("Error: City not found.")
        else:
            msg = await self.client.loop.run_in_executor(None,
                                                         self.wSF,
                                                         retjs)
            await self.client.say(msg)

    @weather.command(pass_context=True)
    async def zip(self, ctx, zipcode: int):
        """Gets weather for US city with <zipcode>."""
        await self.client.send_typing(ctx.message.channel)
        try:
            retjs = await self.by_zip(zipcode)
        except ValueError as e:
            await self.client.say("Error: {}".format(e))
            return
        if retjs["cod"] == "404":
            await self.client.say("Error: Zip not found.")
        else:
            msg = await self.client.loop.run_in_executor(None,
                                                         self.wSF,
                                                         retjs)
            await self.client.say(msg)


def setup(bot):
    bot.add_cog(Weather(bot))
