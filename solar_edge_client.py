import requests
import json

class SolarEdgeClient:
  def __init__(self, api_key:str):
    self.api_key = api_key
    self.debug = False
    self.__solar_output_w = 0
    self.__daily_solar_generated_w = 0
    self.url = "https://monitoringapi.solaredge.com/site/2005097/overview"

  def update(self):
    querystring = {
      "api_key": self.api_key,
    }
    response = requests.request("GET", self.url, params=querystring)
    
    result = json.loads(response.text)
    overview = result["overview"]
    
    currentPowerNode = overview["currentPower"]
    self.__solar_output_w = currentPowerNode["power"]
    if(self.debug):
      print(f"currentPower: {self.__solar_output_w}")
    
    lastDayDataNode = overview["lastDayData"]
    self.__daily_solar_generated_w = lastDayDataNode["energy"]

    if(self.debug):
      print(f"dailyEnergyProduced: {self.__daily_solar_generated_w}")

  @property
  def solar_output_w(self):
    return self.__solar_output_w

  @property
  def daily_solar_generated_w(self):
    return self.__daily_solar_generated_w