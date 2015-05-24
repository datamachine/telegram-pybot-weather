import plugintypes
import sys

sys.path.append('./plugins')

from py3owm import OpenWeatherMap

OWM_icon_emoji_map = {
    "01d": u'\U0001F31E',
    "02d": u'\U000026C5',
    "03d": u'\U00002601',
    "03d": u'\U00002601',
    "09d": u'\U0001F302',
    "10d": u'\U00002614',
    "11d": u'\U000026A1',
    "13d": u'\U00002744',
    "50d": u'\U0001F301'
}

class WeatherPlugin(plugintypes.TelegramPlugin):
    """
    Weather
    """

    patterns = [
        "^!weather? ([0-9]{5})"
    ]

    usage = [
        "!weather <zip code>"
    ]

    def activate_plugin(self):
        if not self.has_option("api key"):
            self.write_option("api key", "")
        if not self.has_option("units"):
            self.write_option("units", "imperial")
        if not self.has_option("units"):
            self.write_option("backend", "openweathermap")

        api_key = self.read_option("api key")
        units = self.read_option("units")

        if self.read_option("backend") == "openweathermap":
            self.owm = OpenWeatherMap(api_key, units)
        elif self.read_option("backend") == "wunderground":
            if api_key == "":
                raise Exception("Wunderground requires an API Key")
            self.wunderground = Wunderground(api_key, units)

    def __get_emoji(self, icon):
        if self.read_option("backend") == "openweathermap":
            if icon in OWM_icon_emoji_map.keys():
                return OWM_icon_emoji_map[icon]
            return u'\U00002610'
        elif:
            return u'\U00002610'


    def run(self, msg, matches):
        if self.read_option("backend") == "openweathermap":
            w = self.owm.weather_data(zipcode=matches.group(1))
            if w:
                emoji = self.__get_emoji(w.icon)
                report = u"{} ({}) {}{}\n{} {}".format(w.name, w.country, w.temp, w.unit_symbol, w.description, emoji)
                return report
        elif self.read_option("backend") == "wunderground":
            pass

        return "Error getting weather data"


