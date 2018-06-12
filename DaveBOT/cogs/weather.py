import datetime
import json
import re

import aiohttp
import discord
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

    async def genembed(self, jtf):
        cond = await self.retcond(str(jtf["weather"][0]["id"]))
        temp = jtf["main"]["temp"] - 273.15
        e = discord.Embed(title=f"Weather in {jtf['name']}, "
                                f"{jtf['sys']['country']}",
                          type="rich",
                          description="Provided by openweathermap.org",
                          url="https://openweathermap.org/",
                          colour=0xFF8C18,
                          timestamp=datetime.datetime.utcnow())
        e.add_field(name="Weather Conditions",
                    value=cond,
                    inline=True)
        e.add_field(name="Temperature",
                    value=f"{round(temp, 2)} °C",
                    inline=True)
        e.add_field(name="Humidity",
                    value=f"{jtf['main']['humidity']} %",
                    inline=True)
        e.add_field(name="Air Pressure",
                    value=f"{jtf['main']['pressure']} hPa",
                    inline=True)
        e.add_field(name="Wind Speed",
                    value=f"{jtf['wind']['speed']} m/s",
                    inline=True)
        return e

    async def retcond(self, conditionid):
        retval = self.conditions.get(conditionid)
        if retval:
            return retval["label"].title()
        else:
            return retval

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

    @commands.group(pass_context=True)
    async def weather(self, ctx):
        """Provides weather data."""
        if ctx.invoked_subcommand is None:
            await self.client.say("Unrecognised subcmd; see !help weather.")

    @weather.command(pass_context=True)
    async def city(self, ctx, city: str, country: str):
        """Gets weather for city given."""
        await self.client.send_typing(ctx.message.channel)
        retjs = await self.by_cityname(city, country)
        if retjs["cod"] == "404":
            await self.client.say("Error: City not found.")
        else:
            e = await self.genembed(retjs)
            await self.client.say(embed=e)

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
            e = await self.genembed(retjs)
            await self.client.say(embed=e)

    @weather.command(pass_context=True)
    async def zip(self, ctx, zipcode: int):
        """Gets weather for US city with <zipcode>."""
        await self.client.send_typing(ctx.message.channel)
        try:
            retjs = await self.by_zip(zipcode)
        except ValueError as e:
            await self.client.say(f"Error: {e}")
            return
        if retjs["cod"] == "404":
            await self.client.say("Error: Zip not found.")
        else:
            e = await self.genembed(retjs)
            await self.client.say(embed=e)


def setup(bot):
    bot.add_cog(Weather(bot))
