from volt_meter import VoltMeter

#volt_meter = VoltMeter(17, .03, 2.25)
volt_meter = VoltMeter(23, .03, 2.25)
#volt_meter = VoltMeter(25, .03, 2.35)

def get_input():
    value1 = input("Input value from 0 to 100: ")
    volt_meter.set_meter_value(float(value1), 0, 100)
    get_input()


if __name__ == "__main__":
    get_input()
