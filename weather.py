from __future__ import print_function
from datetime import datetime as dt
from datetime import timedelta as td
from ndfd.weather import NDFD
from ndfd.elements import Elements
from ndfd.latlon import LatLon


ORLANDO = LatLon((28.5380556, -81.3794444))
ELEMENTS = [Elements.MAX_TEMP, Elements.MIN_TEMP, Elements.WEATHER]
START = dt.now()
FUTURE_FIVE = td(days=+5)
END = dt.today() + FUTURE_FIVE

DATA = NDFD(ORLANDO, ELEMENTS, 'time-series', START, END)
DATA.request()
RES = DATA.parse()

def time_by_id(key):
    """"""
    for time in RES['time-layout']:
        if time.key == key:
            return time


def temp(temp_type, temps):
    for temp in temps:
        if temp.type == temp_type:
            return temp


# print time_by_id(RES['temperature'][0].time_layout)
HIGHS = temp('maximum', RES['temperature'])
LOWS = temp('minimum', RES['temperature'])

HIGH_TIMES = time_by_id(HIGHS.time_layout)

# Iterate over all the start times of the maximum temp values
for i, date in enumerate(HIGH_TIMES.start):
    # Throw the high, low, and date into vars
    the_high = HIGHS.values[i]
    the_low = LOWS.values[i]
    the_date = date.strftime("%D")
    print(u"%s %d\xb0/%d\xb0" % (the_date, the_high, the_low))
