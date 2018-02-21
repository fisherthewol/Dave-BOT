import requests
import re


class weather:
    """Holds API key and provides get functions."""
    def __init__(self, key):
        self.key = key
        self.baseurl = "https://api.openweathermap.org/data/2.5/weather?"
        self.nameurl = self.baseurl + "q={},{}&appid=" + self.key
        self.idurl = self.baseurl + "id={}&appid=" + self.key
        self.latlonurl = self.baseurl + "lat={}&lon={}&appid=" + self.key
        self.zipurl = self.baseurl + "zip={},us&appid=" + self.key
        self.regcomp = re.compile(r"\d{5}([ \-]\d{4})?")

    def by_cityname(cityname, country):
        """Returns based on name and country."""
        r = requests.get(self.nameurl.format(cityname, country))
        return r.json()

    def by_id(cityid):
        """Returns based on city id."""
        r = requests.get(self.idurl.format(cityid))
        return r.json()

    def by_latlon(latitude, longitude):
        """Returns based on latitude and longitude."""
        r = requests.get(self.latlonurl.format(latitude, longitude))
        return r.json()

    def by_zip(zipcode):
        if self.regcomp.match(zipcode):
            r = requests.get(self.zipurl.format(zipcode))
            return r.json()
        else:
            raise ValueError("Zipcode is invalid (wrong or none-US).")
