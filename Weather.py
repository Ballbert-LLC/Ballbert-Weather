import json

import requests

from Hal.Classes import Response
from Hal.Decorators import reg
from Hal.Skill import Skill

class Weather(Skill):
    def __init__(self):
        pass

    def query_weather(self, enpoint, method="get", data={}, query_params={}):
        api_key = self.get("API_KEY")

        full_url = f"http://api.weatherapi.com/v1/{enpoint}?key={api_key}"

        for key, value in query_params.items():
            full_url += f"&{key}={value}"

        if method == "get":
            result = requests.get(
                full_url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                data=data,
            )
        elif method == "post":
            result = requests.post(
                full_url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                data=json.dumps(data),
            )

        try:
            json_data = json.loads(result.text)
        except Exception as e:
            json_data = result.text

        return json_data

    @reg(name="get_current_weather")
    def get_current_weather(self, location, units="metric"):
        """
        Gets the current Weather

        :param string location: The location you want the weather at
        :param string units: (Optional) The system of measurement you want the result to be in either "metric" or "imperial" defaults to metric
        """
        json_data = self.query_weather(
            "current.json", query_params={"q": location})

        result_data = {}

        result_data["location"] = {
            "name": json_data["location"]["name"],
            "region": json_data["location"]["region"],
            "country": json_data["location"]["country"],
            "lat": json_data["location"]["lat"],
            "lon": json_data["location"]["lon"],
        }

        result_data["last_updated"] = json_data["current"]["last_updated"]
        result_data["units"] = units

        if units == "imperial":
            result_data["current_weather"] = {
                "temp": json_data["current"]["temp_f"],
                "condition": json_data["current"]["condition"]["text"],
                "wind": json_data["current"]["wind_mph"],
                "wind_degree": json_data["current"]["wind_degree"],
                "wind_dir": json_data["current"]["wind_dir"],
                "pressure": json_data["current"]["pressure_in"],
                "precip": json_data["current"]["precip_in"],
                "humidity": json_data["current"]["humidity"],
                "cloud": json_data["current"]["cloud"],
                "feelslike": json_data["current"]["feelslike_f"],
                "visability": json_data["current"]["vis_miles"],
                "uv": json_data["current"]["uv"],
                "gust_speed": json_data["current"]["gust_mph"],
            }
        else:
            result_data["current_weather"] = {
                "temp": json_data["current"]["temp_c"],
                "condition": json_data["current"]["condition"]["text"],
                "wind": json_data["current"]["wind_kph"],
                "wind_degree": json_data["current"]["wind_degree"],
                "wind_dir": json_data["current"]["wind_dir"],
                "pressure": json_data["current"]["pressure_mb"],
                "precip": json_data["current"]["precip_mm"],
                "humidity": json_data["current"]["humidity"],
                "cloud": json_data["current"]["cloud"],
                "feelslike": json_data["current"]["feelslike_c"],
                "visability": json_data["current"]["vis_km"],
                "uv": json_data["current"]["uv"],
                "gust_speed": json_data["current"]["gust_kph"],
            }

        return Response(True, data=result_data)

    @reg(name="get_forcasted_weather")
    def get_forcasted_weather(self, location, units="metric", day=0, hour=None):
        """
        Gets the current Weather

        :param string location: The location you want the weather at
        :param string units: (Optional) The system of measurement you want the result to be in either "metric" or "imperial" defaults to metric
        :param integer day: (Optional) The day you want to get the forcast of.  Number 0-2 0 being the current day.
        :param integer hour: (Optional) The hour you want to get the forcast of.  24 hour time format. Integer 0-23. Leave blank if you want a summery for the whole day.


        """
        if day > 2:
            return Response(False, data="Unable to predect that far in advance")
        elif day < 0:
            return Response(False, data="Unable to predect the past")

        if hour != None and (hour > 23 or hour < 0):
            return Response(False, data="Invalid hour")

        json_data = self.query_weather(
            "forecast.json", query_params={"q": location, "days": day+1})

        result_data = {}

        result_data["location"] = {
            "name": json_data["location"]["name"],
            "region": json_data["location"]["region"],
            "country": json_data["location"]["country"],
            "lat": json_data["location"]["lat"],
            "lon": json_data["location"]["lon"],
        }

        result_data["last_updated"] = json_data["current"]["last_updated"]
        result_data["units"] = units

        relavent_day = json_data["forecast"]["forecastday"][day]

        if hour == None:
            if units == "imperial":
                result_data["weather"] = {
                    "max_temp": relavent_day["day"]["maxtemp_f"],
                    "min_temp": relavent_day["day"]["mintemp_f"],
                    "avg_temp": relavent_day["day"]["avgtemp_f"],
                    "maxwind": relavent_day["day"]["maxwind_mph"],
                    "totalprecip": relavent_day["day"]["totalprecip_in"],
                    "avgvis": relavent_day["day"]["avgvis_miles"],
                    "avghumidity": relavent_day["day"]["avghumidity"],
                    "daily_will_it_rain": relavent_day["day"]["daily_will_it_rain"],
                    "daily_chance_of_rain": relavent_day["day"]["daily_chance_of_rain"],
                    "daily_will_it_snow": relavent_day["day"]["daily_will_it_snow"],
                    "daily_chance_of_snow": relavent_day["day"]["daily_chance_of_snow"],
                    "uv": relavent_day["day"]["uv"],
                    "condition": relavent_day["day"]["condition"]["text"]
                }
            else:
                result_data["weather"] = {
                    "max_temp": relavent_day["day"]["maxtemp_c"],
                    "min_temp": relavent_day["day"]["mintemp_c"],
                    "avg_temp": relavent_day["day"]["avgtemp_c"],
                    "maxwind": relavent_day["day"]["maxwind_kph"],
                    "totalprecip": relavent_day["day"]["totalprecip_mm"],
                    "avgvis": relavent_day["day"]["avgvis_km"],
                    "avghumidity": relavent_day["day"]["avghumidity"],
                    "daily_will_it_rain": relavent_day["day"]["daily_will_it_rain"],
                    "daily_chance_of_rain": relavent_day["day"]["daily_chance_of_rain"],
                    "daily_will_it_snow": relavent_day["day"]["daily_will_it_snow"],
                    "daily_chance_of_snow": relavent_day["day"]["daily_chance_of_snow"],
                    "uv": relavent_day["day"]["uv"],
                    "condition": relavent_day["day"]["condition"]["text"]
                }
        else:
            relavent_hour = relavent_day["hour"][hour]

            if units == "imperial":
                result_data["current_weather"] = {
                    "temp": relavent_hour["temp_f"],
                    "condition": relavent_hour["condition"]["text"],
                    "wind": relavent_hour["wind_mph"],
                    "wind_degree": relavent_hour["wind_degree"],
                    "wind_dir": relavent_hour["wind_dir"],
                    "pressure": relavent_hour["pressure_in"],
                    "precip": relavent_hour["precip_in"],
                    "humidity": relavent_hour["humidity"],
                    "cloud": relavent_hour["cloud"],
                    "feelslike": relavent_hour["feelslike_f"],
                    "visability": relavent_hour["vis_miles"],
                    "uv": relavent_hour["uv"],
                    "gust_speed": relavent_hour["gust_mph"],
                }
            else:
                result_data["current_weather"] = {
                    "temp": relavent_hour["temp_c"],
                    "condition": relavent_hour["condition"]["text"],
                    "wind": relavent_hour["wind_kph"],
                    "wind_degree": relavent_hour["wind_degree"],
                    "wind_dir": relavent_hour["wind_dir"],
                    "pressure": relavent_hour["pressure_mb"],
                    "precip": relavent_hour["precip_mm"],
                    "humidity": relavent_hour["humidity"],
                    "cloud": relavent_hour["cloud"],
                    "feelslike": relavent_hour["feelslike_c"],
                    "visability": relavent_hour["vis_km"],
                    "uv": relavent_hour["uv"],
                    "gust_speed": relavent_hour["gust_kph"],
                }

        return Response(True, data=result_data)
