import machine, time, onewire, ds18x20
from umqtt.simple import MQTTClient
# the device is on GPIO12
dat = machine.Pin(12)

# create the onewire object
ds = ds18x20.DS18X20(onewire.OneWire(dat))

# scan for devices on the bus
sensors = ds.scan()

myMqttClient = "moj-mqtt-client"  # can be anything unique
adafruitIoUrl = "io.adafruit.com"
adafruitUsername = "mroozon"
adafruitAioKey = "cd97ba06801746a59750f6a4766d5fc7"
c = MQTTClient(myMqttClient, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)
c.connect()

while True:
  m = 1
  for sensor in sensors:
    ds.convert_temp()
    time.sleep_ms(750)
    temperature = ds.read_temp(sensor)
    c.publish("mroozon/feeds/feed-temperature%d" % m, str(temperature))
    time.sleep(5)  # number of seconds between each Publish
    m += 1
