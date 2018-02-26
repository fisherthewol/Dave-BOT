import requests
import re
import json
import os


class weather:
    """Holds API key and provides get functions."""
    def __init__(self, key=os.environ.get("weather")):
        self.key = key
        self.baseurl = "https://api.openweathermap.org/data/2.5/weather?"
        self.nameurl = self.baseurl + "q={},{}&appid=" + self.key
        self.idurl = self.baseurl + "id={}&appid=" + self.key
        self.zipurl = self.baseurl + "zip={},us&appid=" + self.key
        self.regcomp = re.compile(r"\d{5}([ \-]\d{4})?")
        with open("DaveBOT/owmaw/cond.json") as op:
            cond = json.load(op)
        self.conditions = cond

    def retcond(self, conditionid):
        retval = ""
        try:
            retval = self.conditions[conditionid]
        except KeyError:
            return "Invalid weather code."
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
