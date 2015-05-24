import plugintypes
import sys

sys.path.append('./plugins.repos/telegram-pybot-weather') # TODO Ugly Hack, find a better way

from py3owm import OpenWeatherMap
from py3wu import WeatherUnderground

class WeatherPlugin(plugintypes.TelegramPlugin):
    """
    Weather
    """

    patterns = [
        "^!weather? ([0-9]{5}|.*)",
    ]

    usage = [
        "!weather location"
    ]

    def activate_plugin(self):
        if not self.has_option("api key"):
            self.write_option("api key", "")
        if not self.has_option("units"):
            self.write_option("units", "imperial")
        if not self.has_option("backend"):
            self.write_option("backend", "openweathermap")

        api_key = self.read_option("api key")
        units = self.read_option("units")

        if self.read_option("backend") == "openweathermap":
            self.backend = OpenWeatherMap(api_key, units)
        elif self.read_option("backend") == "weatherunderground":
            if api_key == "":
                raise Exception("Weather Underground requires an API Key")
            self.backend = WeatherUnderground(api_key, units)
        else:
            raise Exception("Invalid backend selected")

    def run(self, msg, matches):
        try:
            if self.read_option("backend") == "wunderground":
                w = self.backend.weather_data(search=matches.group(1))
            else:
                w = self.backend.weather_data(zipcode=matches.group(1))
            if w:
                report = u"{} ({}) {}{}\n{} {}".format(w.name, w.country, w.temp,
                                                       w.unit_symbol, w.description, w.icon)
                return report
        except Exception as e:
            print("Exception {}".format(e))

        return "Error getting weather data"


