import os
from datetime import datetime
import importlib
import hashlib
import xml.etree.ElementTree as ET
import requests
import elements
from exception import ConnectionException
from latlon import LatLon
import timelayout

class NDFD(object):

    BASE_URI = "http://graphical.weather.gov/"
    BASE_PATH = "xml/sample_products/browser_interface/ndfdXMLclient.php"
    REQUIRED_QS = ["lat", "lon", "product", "begin", "end"]

    latlon = None

    def __init__(self, position, elements, products, begin, end):
        self.latlon = position
        self.elements = elements
        self.products = products
        self.begin = begin.replace(microsecond=0)
        self.end = end.replace(microsecond=0)

    def request(self):
        if self._valid_cache():
            with open(self.get_filename(), 'r') as fh:
                cache = fh.read()
            self.result = cache
            return cache

        url = self.BASE_URI + self.BASE_PATH + "?"

        start = self.begin.isoformat()
        end = self.end.isoformat()

        required = [
            "product=" + self.products,
            "begin=" + start,
            "end=" + end,
            "lat=" + str(self.latlon.latitude),
            "lon=" + str(self.latlon.longitude)
        ]

        elms = []
        for elm in self.elements:
            elms.append("{elm}={elm}".replace("{elm}", elm))

        query_string = "&".join(elms)

        url = url + "&".join(required) + "&" + "&".join(elms)
        print(url)
        res = requests.get(url)

        with open(self.get_filename(), 'w') as fh:
            fh.write(res.text)


        res.raise_for_status()
        if res.status_code != 200:
            raise ConnectionException('Bad connection with NWS')
        self.result = res

    def parse(self):
        root = ET.fromstring(self.result)
        correlations = {
            'time-layout': 'TimeLayout',
            'temperature': 'Temperature'
        }

        return_dict = dict()
        _tmp = []
        for tl in root.findall('./data/time-layout'):
            module = importlib.import_module('ndfd.timelayout')
            class_ = getattr(module, correlations[tl.tag])
            instance = class_()

            # Dump the attributes
            for attrib in tl.attrib:
                instance.set(attrib.replace("time-", ""), tl.attrib[attrib])

            instance.set('key', tl[0].text)

            _start = []
            for start in tl.findall('start-valid-time'):
                _start.append(datetime.strptime(start.text[:19], "%Y-%m-%dT%H:%M:%S"))
            instance.start = _start

            _end = []
            for end in tl.findall('end-valid-time'):
                _end.append(datetime.strptime(end.text[:19], "%Y-%m-%dT%H:%M:%S"))
            instance.end = _end
            _tmp.append(instance)

            return_dict['time-layout'] = _tmp

        module = importlib.import_module('ndfd.timelayout')

        for param in root.findall('./data/parameters/'):
            if param.tag in correlations:
                if param.tag not in return_dict.keys():
                    return_dict[param.tag] = list()
                class_ = getattr(module, correlations[param.tag])
                attribs = param.attrib
                if param.tag == 'temperature':
                    caption = param[0].text
                    values = []
                    for value in param.findall('value'):
                        values.append(int(value.text))
                    instance = class_(attribs, caption, values)
                    return_dict[param.tag].append(instance)

        return return_dict

    def get_time_layouts(self):
        time = {}
        layouts = self.res.findall('./data/time-layout')
        for i, layout in enumerate(layouts):
            _tmp = {}
            _tmp2 = []
            key = layout[0].text
            for j, t in enumerate(layout):
                if j == 0:
                    continue
                _tmp2.append((t.tag, t.text))
            time[key] = _tmp2
        self.time_layouts = time
        return time

    
    def get_filename(self):
        parts = [
            self.begin.strftime("%Y-%m-%dT%H"),
            self.end.strftime("%Y-%m-%dT%H"),
            str(self.latlon.latitude),
            str(self.latlon.longitude)
        ]

        for elm in self.elements:
            parts.append(elm)
        filename = "".join(parts)
        sha = hashlib.sha1(filename)
        return sha.hexdigest() + '.xml'


    def _valid_cache(self):
        # file = self.begin + "-" + self.end + "-" + "-".join(self.elements)
        # print(file)
        return True if os.path.isfile(self.get_filename()) else False


