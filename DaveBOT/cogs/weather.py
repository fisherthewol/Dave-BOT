import json
import re

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
            cond = json.load(op)
        self.conditions = cond

    def wtherStrFrmttr(self, jsontoformat):
        city = jsontoformat["name"]
        coun = jsontoformat["sys"]["country"]
        cond = self.retcond(str(jsontoformat["weather"][0]["id"]))
        temp = jsontoformat["main"]["temp"] - 273.15
        temp = round(temp, 2)
        humd = jsontoformat["main"]["humidity"]
        pres = jsontoformat["main"]["pressure"]
        sped = jsontoformat["wind"]["speed"]
        return ("Weather in {}, {}:"
                "\nConditions: {}"
                "\nTemp: {} °C"
                "\nHumidity: {} %"
                "\nPressure: {} hPa"
                "\nWind Speed: {} m/s".format(city,
                                              coun,
                                              cond,
                                              temp,
                                              humd,
                                              pres,
                                              sped))

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

    @commands.group(pass_context=True)
    async def weather(self, ctx):
        """Provides !weather cmds; see !weather help."""
        if ctx.invoked_subcommand is None:
            await self.client.say("Invalid command; see !weather help.")

    @weather.command()
    async def help(self):
        await self.client.say("\nPossible !weather commands:"
                              "\n-!weather city:"
                              "\n--Use\n"
                              "```!weather city <cityname>,"
                              "<countrycode>```"
                              "\n  where <city> is a city, and "
                              "<countrycode>"
                              "is a valid ISO 3166-1 alpha-2 code."
                              "\n-!weather id:"
                              "\n--Use\n"
                              "```!weather id <id>```"
                              "\n  where <id> is a valid city id from "
                              "http://bulk.openweathermap.org/sample/"
                              "city.list.json.gz"
                              "\n-!weather zip:"
                              "\n--Use\n"
                              "```!weather zip <zipcode>```"
                              "\n  where <zipcode> is a valid US zipcode.")

    @weather.command()
    async def city(self, citcun: str):
        wthrmsg = await self.client.say("Fetching weather...")
        sngs = citcun.split(",")
        retjs = self.by_cityname(sngs[0], sngs[1])
        if retjs["cod"] == "404":
            await self.client.edit_message(wthrmsg, "Error: "
                                                    "City not found.")
        else:
            await self.client.edit_message(wthrmsg,
                                           self.wtherStrFrmttr(retjs))

    @weather.command()
    async def id(self, cityid: int):
        wthrmsg = await self.client.say("Fetching weather...")
        retjs = self.by_id(cityid)
        if retjs["cod"] == "404":
            await self.client.edit_message(wthrmsg, "Error: "
                                                    "City not found.")
        else:
            await self.client.edit_message(wthrmsg, self.wtherStrFrmttr(retjs))

    @weather.command()
    async def zip(self, zipcode: int):
        wthrmsg = await self.client.say("Fetching weather...")
        try:
            retjs = self.by_zip(zipcode)
        except ValueError as e:
            await self.client.edit_message(wthrmsg, "Error: {}".format(e))
        if retjs["cod"] == "404":
            await self.client.edit_message(wthrmsg, "Error: "
                                                    " Zip not found.")
        else:
            await self.client.edit_message(wthrmsg, self.wtherStrFrmttr(retjs))


def setup(bot):
    bot.add_cog(Weather(bot))
