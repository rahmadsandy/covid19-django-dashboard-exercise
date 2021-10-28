import json
from urllib.request import urlopen

import plotly.graph_objs as go
from plotly.offline import plot


from . import getdata


def usa_map():
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
