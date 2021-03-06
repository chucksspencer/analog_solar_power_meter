from gpiozero import PWMLED
import math

class VoltMeter:
  """
  The VoltMeter class will use pulse width modulation and some math to send the needed
  voltage to the given GPIO in order to drive a physical analog volt meter.
  """

  def __init__(self, 
               gpio: int, 
               low_end_adjuster_factor: float = .03, 
               inner_factor:float = 2.25):
    """
    Constructor

    Parameters
    ----------
    gpio: The number of the GPIO pin the positive output goes through
    low_end_adjuster_factor : An outer factor, a power to which the over all formula is raised to steepen the curve. Defaults to 4.7
    multiplier: A value by which inner values in the formula are multiplied, effects magnitude of the curve. Defaults to 0.965
    factor: A value by which the input value is raised to control range. Defaults to 0.425
    """
    self.debug = False
    self.low_end_adjuster_factor = low_end_adjuster_factor
    self.factor = inner_factor
    self.voltageouput = PWMLED(gpio)


  def set_meter_value(self, value: float, min_value: float = 0, max_value: float = 1):
    """
    Set the value of the meter. 

    Parameters
    ----------
    value: The value to display. Should be between the min and max values
    min_value: The minimum value in the range the meter should display. Defaults to zero.
    max_value: The maximum value in the range the meter should display. Defaults to 1.
    """
    if value < min_value:
        print(f"Value {value} cannot be below range minimum of {min_value}")
        return
    if value > max_value:
        print(f"Value {value} cannot be above range maximum of {max_value}")
        return

    relative_value = (value - min_value) / (max_value - min_value)
    low_end_adjuster = (math.sin(relative_value*math.pi*1.75)+.8)*self.low_end_adjuster_factor
    calculated = (relative_value**self.factor) + low_end_adjuster

    if(calculated) > 1:
      calculated = 1

    if(self.debug):
        print(f"================================")
        print(f"Normalized value of {round(value,2)} with range min {round(min_value,2)} to max {round(max_value,2)} = {round(relative_value,2)}")
        print(f"Adjusted: {round(calculated,3)}")
        print(f"Theoretical Voltage: {relative_value*3.3} ")
        print(f"Raw Voltage: {round(calculated,3)*3.3} ")
        print(f"Adjusted Voltage: {round(calculated,3)*3.3*4.545} ")
    self.voltageouput.value = calculated
