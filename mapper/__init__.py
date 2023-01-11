import csv
from pathlib import Path
import urllib.parse

from pprint import pprint

from openpyxl import load_workbook
import requests
import matplotlib.pyplot as pl
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import numpy

class PostcodeMapper(object):

    endpoint = "http://api.getthedata.com/postcode/"
    coords = []
    csvfields = ["postcode", "longitude", "latitude"]
    cache = dict()
    cachefile = None
    recache = False
    xbins = 40 # Number of bins for histogram - smaller = less resolution
    ybins = 40
    tiledepth = 16
    markers = None # numpy array of [lat, long, colour] for each point to mark
    figure = None # matplotlib figure

    def __init__(self, cache=None):
        cachefile = cache if cache else "postcodes.csv"
        self.cachefile = Path(cachefile)
        self.loadCache()

    def loadCache(self):
        # Retrieves cached coordinates, if they exist
        if self.cachefile.is_file():
            with open(self.cachefile, "r") as c:
                d = csv.DictReader(c, fieldnames=self.csvfields)
                next(d, None)  # Skip header row
                for row in d:
                    self.cache[row["postcode"]] = (
                        float(row["longitude"]),
                        float(row["latitude"]),
                    )

    def saveCache(self):
        if self.recache:
            with open(self.cachefile, "w") as c:
                d = csv.DictWriter(c, fieldnames=self.csvfields)
                d.writeheader()
                for k, v in self.cache.items():
                    d.writerow({"postcode": k, "longitude": v[0], "latitude": v[1]})

    def importXLS(self, file, sheet, column, header):
        # Read in data from xlsx, convert to coords, then write back to a csv
        wb = load_workbook(filename=file)
        ws = wb[sheet]

        postcodes = [cell.value for cell in ws[column]]

        if header:
            del postcodes[0]

        self.convertPostcodes(postcodes)

    def convertPostcodes(self, postcodes):
        # pc = { postcode: self.coordFromPostcode(postcode) for postcode in postcodes }
        # self.saveCache()
        # pprint(pc)
        for postcode in postcodes:
            self.coords.append(self.coordFromPostcode(postcode))
        # return pc

    def coordFromPostcode(self, postcode):
        if postcode in self.cache:
            return self.cache[postcode]
        else:
            self.recache = True
            request = requests.get(self.endpoint + urllib.parse.quote_plus(postcode))
            response = request.json()

            if response["status"] == "match":
                coords = (
                    float(response["data"]["longitude"]),
                    float(response["data"]["latitude"]),
                )
                self.cache[postcode] = coords
                return coords
            else:
                return False

    def importPostcodes(file, sheet, column, header):
        pass

    def addMarkers(self, markers) :
        self.markers = numpy.array(markers)

    def makeMap(self, **kwargs):
        sizes = {
            "a3": (11.693, 16.535, ), # a3 landscape
            "a4": (8.268, 11.693), # a4 landscape
        }
        
        size = kwargs.get("paper", "a4")
        oriented = (sizes[size][0], sizes[size][1]) if (kwargs.get("orientation", "landscape") == 'portrait') else (sizes[size][1], sizes[size][0])
        self.figure = pl.figure(figsize=oriented)

        request = cimgt.QuadtreeTiles()
        ax = pl.axes(projection=request.crs)
        ax.add_image(request, self.tiledepth)

        if len(self.coords) > 0:
            x = numpy.asarray([m[0] for m in self.coords if m])
            y = numpy.asarray([m[1] for m in self.coords if m])

            xynps = ax.projection.transform_points(ccrs.Geodetic(), x, y)
            m = ax.hist2d(
                xynps[:, 0],
                xynps[:, 1],
                bins=[self.xbins, self.ybins],
                alpha=0.5,
                cmap=pl.cm.jet,
                cmin=1,
            )

            bounds = list(range(1, 10))
            cbar = pl.colorbar(m[3], ax=ax, shrink=0.4, format="%.0f", ticks=bounds, label='People per bin')

        if self.markers is not None:
            unps = ax.projection.transform_points(
                ccrs.Geodetic(), self.markers[:, 1].astype(float), self.markers[:, 0].astype(float)
            )
            pl.scatter(unps[:,0], unps[:,1], s=30, c=self.markers[:,2], marker='D')

        pl.tight_layout(pad=4)

        file = kwargs.get("file", None)
        if file:
            self.saveMap(file)

    def saveMap(self, filename) :
        if self.figure:
            self.figure.savefig(
                filename,
                dpi=self.figure.dpi,
            )
        
