from sense_energy import Senseable

class SenseClient:
  def __init__(self, email: str, password: str):
    self.email = email
    self.password = password
    self.sense = Senseable(email, password)
  
  def update(self):
    try:
      self.sense.update_realtime()
      self.sense.update_trend_data()
    except:
      print("Error occurred accessing Sense API - reauthenticating and retrying")
      self.sense.authenticate(self.email, self.password)
      self.sense.update_realtime()
      self.sense.update_trend_data()

  @property
  def power_consumed_w(self):
    return self.sense.active_power

  @property
  def solar_output_w(self):
    return self.sense.active_solar_power

  @property
  def daily_solar_generated_kwh(self):
    return self.sense.daily_production

