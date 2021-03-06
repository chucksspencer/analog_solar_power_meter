import sys
import time
import configparser
from datetime import datetime
from volt_meter import VoltMeter
from sense_client import SenseClient
from solar_edge_client import SolarEdgeClient

daily_power_meter = VoltMeter(25, .03, 2.35)
power_consumed_meter = VoltMeter(23, .03, 2.25)
solar_output_meter = VoltMeter(17, .03, 2.25)

config = configparser.ConfigParser()
config.read('config.txt')
sense_email = config['DEFAULT']['sense_email']
sense_password = config['DEFAULT']['sense_password']
solar_edge_api_key = config['DEFAULT']['solar_edge_api_key']

sense_client = SenseClient(sense_email, sense_password)
solar_edge_client = SolarEdgeClient(solar_edge_api_key)

def main_loop():
    while True:
        try:
          now = datetime.now()
          timestr = now.strftime('%H:%M:%S')
          print(f'>>>>>>>>>>--------------------------- UPDATING {timestr} ------------------------------------<<<<<<<<<<<')
          sense_client.update()
          solar_edge_client.update()
          print(f'Solar power {round(solar_edge_client.solar_output_w)} watts')
          solar_output_meter.set_meter_value(solar_edge_client.solar_output_w, 0, 12000)
          print('------------')
          print(f'Total daily solar power {round(solar_edge_client.daily_solar_generated_w)} watts')
          daily_power_meter.set_meter_value(solar_edge_client.daily_solar_generated_w, 0, 60000)
          print('------------')
          print(f'Power consumed {round(sense_client.power_consumed_w)} watts')
          power_consumed_meter.set_meter_value(sense_client.power_consumed_w, 0, 12000)
        except:
          print('Unexpected error:', sys.exc_info()[0])

        time.sleep(60)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print ('\nExiting by user request.\n')
        sys.exit(0)
