from datetime import datetime
from datetime import time
from ndfd.weather import NDFD
from ndfd.elements import Elements
from ndfd.latlon import LatLon
from ndfd.exception import ConnectionException

ll = LatLon((28.5380556, -81.3794444))

elm = Elements()

elements = [
    elm.MAX_TEMP,
    elm.MIN_TEMP,
    elm.WIND_SPEED
]

try:
    test = NDFD(ll, elements, 'time-series', '2016-06-27T00:00:00', '2016-06-30T23:59:59')
    test.parse()
    # for elm in d.findall('./data/time-layout/'):
    #     print(elm)
    times = test.get_time_layouts()

    for idx, temp in enumerate(test.res.findall('./data/parameters/temperature')):
        time_id = temp.attrib['time-layout']
        for v, t in enumerate(temp):
            if t.tag == 'name':
                continue
            
            type = temp.attrib['type']
            value = 'high' if type == 'maximum' else 'low'
            date_obj = datetime.strptime(times[time_id][(v * 2) - 1][1][:19], "%Y-%m-%dT%H:%M:%S")
            the_time = date_obj.strftime("%A")
            # print("The %s for %s is %d%s" % (value, the_time, int(t.text), u'\u00b0'))
        # print("-"*80)


    for time in times:
        # print(time)
        layouts = test.res.findall('./data/parameters/temperature[@time-layout="' + time + '"]')
        # print(layouts)

    highs = test.res.findall('./data/parameters/temperature[@type="maximum"]')
    lows = test.res.findall('./data/parameters/temperature[@type="minimum"]')
    for idx, temp in enumerate(highs):
        time_key = temp.attrib['time-layout']
        start = test.res.find('./data/time-layout[layout-key="' + time_key + '"]')
        for j, t in enumerate(temp):
            if j == 0:
                continue
            high = t.text
            low = lows[idx][j].text
            date_obj = datetime.strptime(start[(j * 2) - 1].text[:19], "%Y-%m-%dT%H:%M:%S")
            the_time = date_obj.strftime("%A")
            print(u"%s %s\u00b0(%s\u00b0)" % (the_time, high, low))



except ConnectionException as e:
    print(e.message)