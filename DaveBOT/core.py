import logging
import logging.handlers
import platform
import queue
import signal
import sys

import discord
import feedparser
from DaveBOT import owmaw
from discord.ext import commands


class Dave:
    """Main class for Bot."""
    def __init__(self, code, loglevel, redid, redsc, wk):
        self.client = commands.Bot(command_prefix="!")
        self.code = code
        self.cogs = []
        if (redid and redsc):
            self.client.rid = redid
            self.client.rsc = redsc
            self.cogs.append("cogs.reddit")
        self.weather = owmaw.weather()
        self.setupLogging(loglevel)
        if "Linux" in platform.system():
            self.host_is_Linux = True
        else:
            self.host_is_Linux = False
        signal.signal(signal.SIGTERM, self.sigler)
        # Load cogs:
        for cog in self.cogs:
            try:
                self.client.load_extension(cog)
            except Exception as e:
                self.logger.critical("Failed load {}, exception {}".format(cog,
                                                                           e))
                sys.exit("Failed load {}, exception {}".format(cog,
                                                               e))

    def sigler(self, signal, frame):
        """Set the response to sigterm."""
        self.logger.critical("SIGTERM recieved, ending.")
        sys.exit("SIGTERM recieved, ending.")

    def setupLogging(self, loglev):
        """Sets up logging"""
        # Setup queue and queue handler:
        que = queue.Queue(-1)
        queue_handler = logging.handlers.QueueHandler(que)
        queue_handler.setLevel(loglev)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(queue_handler)
        # Setup listener:
        streamhandle = logging.StreamHandler()
        streamhandle.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s"
            " [in %(pathname)s:%(lineno)d]"))
        streamhandle.setLevel(loglev)
        listener = logging.handlers.QueueListener(que, streamhandle)
        listener.start()
        self.logger.warning("Logging is setup.")

    def uptimeFunc(self):
        """Returns host uptime nicely."""
        if self.host_is_Linux:
            from datetime import timedelta
            with open("/proc/uptime", "r") as f:
                uptime_seconds = float(f.readline().split()[0])
                uptime_string = str(timedelta(seconds=uptime_seconds))
            return uptime_string
        else:
            self.logger.warning("Host is not linux, uptimeFunc not supported.")
            return "incomp host."

    def wtherStrFrmttr(self, jsontoformat):
        city = jsontoformat["name"]
        coun = jsontoformat["sys"]["country"]
        cond = self.weather.retcond(str(jsontoformat["weather"][0]["id"]))
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

    def discout(self):
        """Discord functions and client running."""
        @self.client.event
        async def on_ready():
            """Outputs on successful launch."""
            self.logger.warning("Login Successful")
            self.logger.warning("Name : {}" .format(self.client.user.name))
            self.logger.warning("ID : {}" .format(self.client.user.id))
            self.logger.info("Successful self.client launch.")
            await self.client.change_presence(game=discord.Game(name="Use !help"))

        @self.client.command(pass_context=True)
        async def news(ctx):
            """Returns top news from bbc and gameinformer."""
            self.logger.info("!news called.")
            bbcmsg = await self.client.say("Fetching bbc news...")
            gmimsg = await self.client.say("Fetching gameinformer news...")
            bbc = feedparser.parse("https://feeds.bbci.co.uk/news/world/"
                                   "europe/rss.xml")
            game = feedparser.parse("https://www.gameinformer.com/b/"
                                    "mainfeed.aspx?Tags=feature")
            await self.client.edit_message(bbcmsg, bbc.entries[0]["link"])
            await self.client.edit_message(gmimsg, game.entries[0]["link"])

        @self.client.command(pass_context=True)
        async def pie(ctx):
            """Gives latest Jonathan Pie Video."""
            self.logger.info("!pie called.")
            piemsg = await self.client.say("Fetching video.")
            pie = feedparser.parse("https://www.youtube.com/feeds/videos.xml?"
                                   "channel_id=UCO79NsDE5FpMowUH1YcBFcA")
            await self.client.edit_message(piemsg, pie.entries[0]['link'])

        @self.client.command(pass_context=True)
        async def dave(ctx):
            self.logger.info("!dave called.")
            if self.host_is_Linux:
                uptime = self.uptimeFunc()
                version = platform.python_version()
                compi = platform.python_compiler()
                # next 3 lines will be depreceated in py3.7; find alternative?
                lindist = platform.linux_distribution()
                lindistn = lindist[0]
                lindistv = lindist[1]
                await self.client.say("\nHost Uptime: {}"
                                      "\nPython Version: {}\n"
                                      "\nPython Compiler: {}"
                                      "\nDistro: {};v{}".format(uptime,
                                                                version,
                                                                compi,
                                                                lindistn,
                                                                lindistv))
            else:
                self.logger.warning("Host not linux, !dave is not supported.")
                await self.client.say("Host !=linux; feature coming soon.\n")

        @self.client.group(pass_context=True)
        async def weather(ctx):
            """Provides !weather; see !weather help."""
            self.logger.info("!weather called.")
            if ctx.invoked_subcommand is None:
                await self.client.say("Invalid command; see !weather help.")

        @weather.command()
        async def help():
            self.logger.info("!weather help called.")
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
        async def city(citcun: str):
            self.logger.info("!weather city called.")
            wthrmsg = await self.client.say("Fetching weather...")
            sngs = citcun.split(",")
            retjs = self.weather.by_cityname(sngs[0], sngs[1])
            if retjs["cod"] == "404":
                await self.client.edit_message(wthrmsg, "Error: "
                                                        "City not found.")
            else:
                await self.client.edit_message(wthrmsg,
                                               self.wtherStrFrmttr(retjs))

        @weather.command()
        async def id(cityid: int):
            self.logger.info("!weather id called.")
            wthrmsg = await self.client.say("Fetching weather...")
            retjs = self.weather.by_id(cityid)
            if retjs["cod"] == "404":
                await self.client.edit_message(wthrmsg, "Error: "
                                                        "City not found.")
            else:
                await self.client.edit_message(wthrmsg, self.wtherStrFrmttr(retjs))

        @weather.command()
        async def zip(zipcode: int):
            self.logger.info("!weather id called.")
            wthrmsg = await self.client.say("Fetching weather...")
            try:
                retjs = self.weather.by_zip(zipcode)
            except ValueError as e:
                await self.client.edit_message(wthrmsg, "Error: {}".format(e))
            if retjs["cod"] == "404":
                await self.client.edit_message(wthrmsg, "Error: "
                                                        " Zip not found.")
            else:
                await self.client.edit_message(wthrmsg, self.wtherStrFrmttr(retjs))

        self.client.run(str(self.code))


if __name__ == "__main__":
    raise sys.exit("This is an import file, please do not run directly.")
