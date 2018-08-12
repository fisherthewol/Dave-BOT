import datetime
import json
import os
import re
import socket

import aiohttp
import discord
from discord.ext import commands


class Weather:
    """Weather functions and commands."""
    def __init__(self, bot):
        self.client = bot
        self.key = os.environ.get("weather")
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(family=socket.AF_INET))
        self.regcomp = re.compile(r"\d{5}([ \-]\d{4})?")
        with open("data/cond.json") as op:
            self.conditions = json.load(op)

    def __unload(self):
        self.session.close()

    async def genembed(self, jtf):
        e = discord.Embed(title=f"Weather in {jtf['name']}, "
                                f"{jtf['sys']['country']}",
                          type="rich",
                          description="Provided by openweathermap.org",
                          url="https://openweathermap.org/",
                          colour=0xFF8C18,
                          timestamp=datetime.datetime.utcnow())
        e.set_thumbnail(url=f"https://openweathermap.org/img/w/{jtf['weather'][0]['icon']}.png")
        cond = await self.retcond(str(jtf["weather"][0]["id"]))
        e.add_field(name="Weather Conditions",
                    value=cond,
                    inline=True)
        temp = jtf["main"]["temp"] - 273.15
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
        params = {"appid": self.key, "q": cityname+","+country}
        resp = await self.session.get("https://api.openweathermap.org"
                                      "/data/2.5/weather",
                                      params=params)
        jsn = await resp.json()
        resp.close()
        return jsn

    async def by_id(self, cityid):
        """Returns based on city id."""
        params = {"appid": self.key, "id": cityid}
        resp = await self.session.get("https://api.openweathermap.org"
                                      "/data/2.5/weather",
                                      params=params)
        jsn = await resp.json()
        resp.close()
        return jsn

    async def by_zip(self, zipcode):
        if self.regcomp.match(str(zipcode)):
            params = {"appid": self.key, "zip": str(zipcode)+",us"}
            resp = await self.session.get("https://api.openweathermap.org"
                                          "/data/2.5/weather",
                                          params=params)
            jsn = await resp.json()
            resp.close()
            return jsn
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
            await self.client.say("Error: City not found.")
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
