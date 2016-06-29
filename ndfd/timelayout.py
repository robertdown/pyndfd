from latlon import LatLon

class Temperature(object):
    temp_type = ''
    units = ''
    time_layout = ''
    caption = ''
    values = []

    def __init__(self, attribs, caption, values):
        """Initialize a temperature"""
        attribs = list(attribs.items())
        for attrib in attribs:
            key = attrib[0].replace('-', '_')
            val = attrib[1]
            self.__setattr__(key, val)

        self.caption = caption
        self.values = values


class Location(object):
    key = ''
    point = []

class TimeLayout(object):
    coordinate = ''
    summarization = ''
    key = ''
    start = []
    end = []

    def set(self, attrib, value):
        self.__setattr__(attrib, value)
