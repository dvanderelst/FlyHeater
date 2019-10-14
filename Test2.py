import MyPhidgets
import time
from matplotlib import pyplot

relay = MyPhidgets.MyTile(hub_serial=560175, hub_port=0)
thermo = MyPhidgets.MyThermo(hub_serial=560175, hub_port=1)

relay.set_duty_cylces([0.1, 0,0,0])

time.sleep(5)