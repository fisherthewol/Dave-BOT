import json
import re
import sys

import requests
from discord.ext import commands


class Weather:
    """Weather functions and commands."""
    def __init__(self, bot):
        self.client = bot
        self.key = bot.wk
        self.baseurl = "https://api.openweathermap.org/data/2.5/weather?"
        self.nameurl = self.baseurl + "q={},{}&appid=" + self.key
        self.idurl = self.baseurl + "id={}&appid=" + self.key
        self.zipurl = self.baseurl + "zip={},us&appid=" + self.key
        self.regcomp = re.compile(r"\d{5}([ \-]\d{4})?")
        with open("data/cond.json") as op:
            self.conditions = json.load(op)

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

    def by_cityname(self, cityname, country):
        """Returns based on name and country."""
        r = requests.get(self.nameurl.format(cityname, country))
        return r.json()

    def by_id(self, cityid):
        """Returns based on city id."""
        r = requests.get(self.idurl.format(cityid))
        return r.json()

    def by_zip(self, zipcode):
        if self.regcomp.match(str(zipcode)):
            r = requests.get(self.zipurl.format(zipcode))
            return r.json()
        else:
            raise ValueError("Zipcode is invalid (wrong or none-US).")

    async def on_command_error(self, error, ctx):
        """Event triggered on error raise."""
        if hasattr(ctx.command, "on_error"):
            return
        error = getattr(error, "original", error)
        if isinstance(error, commands.DisabledCommand):
            return await self.client.send_message(ctx.message.channel,
                                                  "{} is disabled.".format(ctx.command))
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await self.client.send_message(ctx.author,
                                                      "{} can't be used in DMs.".format(ctx.command))
            except:
                pass
        # If it's not one of these, print traceback:
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        return await self.client.send_message(ctx.message.channel,
                                              "Error in command; issue has been logged.")

    @commands.group(pass_context=True)
    async def weather(self, ctx):
        """Provides weather data."""
        if ctx.invoked_subcommand is None:
            await self.client.say("Unrecognised command; see !weather help.")

    @weather.command(pass_context=True)
    async def city(self, ctx, city: str, country: str):
        """Gets weather for city given."""
        await self.client.send_typing(ctx.message.channel)
        retjs = await self.client.loop.run_in_executor(None,
                                                       self.by_cityname,
                                                       city,
                                                       country)
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
        retjs = await self.client.loop.run_in_executor(None,
                                                       self.by_id,
                                                       cityid)
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
            retjs = await self.client.loop.run_in_executor(None,
                                                           self.by_zip,
                                                           zipcode)
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
