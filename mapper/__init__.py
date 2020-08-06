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

    # Number of bins for histogram - smaller = less resolution
    xbins = 25
    ybins = 25

    tiledepth = 16

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

    def getUnits(self):
        units = numpy.array(
            [
                [51.4786941724208, -2.598413827911372, "red"],  # Brabazon
                [51.455440, -2.620430, "purple"], # Clifton
                [51.486130609067075, -2.589508893981929, "orange"],  # Concorde
                [51.47463134806349, -2.583211067214961, "orange"],  # Phoenix
                [51.512744513854194, -2.6151856808814955, "green"],  # Pirates
                [51.487019158751714, -2.6184016494903517, "orange"],  # Spaniorum
                [51.46631052970262, -2.600189450279231, "orange"],  # Spitfire
                [51.48641788642314, -2.6240557460937453, "red"],  # Steama
                [51.48279004181177, -2.6097863941345167, "orange"],  # White Tree
            ]
        )

        return units

    def makeMap(self):
        pl.figure(figsize=(16.53, 11.69))

        x = numpy.asarray([m[0] for m in self.coords if m])
        y = numpy.asarray([m[1] for m in self.coords if m])

        # request = cimgt.GoogleTiles(style='street')
        # request = cimgt.Stamen('watercolor')
        request = cimgt.QuadtreeTiles()

        ax = pl.axes(projection=request.crs)
        ax.add_image(request, self.tiledepth)

        xynps = ax.projection.transform_points(ccrs.Geodetic(), x, y)
        m = ax.hist2d(
            xynps[:, 0],
            xynps[:, 1],
            bins=[self.xbins, self.ybins],
            alpha=0.5,
            cmap=pl.cm.jet,
            cmin=1,
        )
        cbar = pl.colorbar(m[3], ax=ax, shrink=0.4, format="%.1f")
        # pl.scatter(xynps[:,0], xynps[:,1], s=50, c="yellow", marker='o')

        units = self.getUnits()
        unps = ax.projection.transform_points(
            ccrs.Geodetic(), units[:, 1].astype(float), units[:, 0].astype(float)
        )
        pl.scatter(unps[:,0], unps[:,1], s=30, c=units[:,2], marker='D')
        # pl.scatter(unps[:, 0], unps[:, 1], s=100, c="purple", marker="D")

        # ax.set_extent([51.526760, 51.454065, -2.698467, -2.564378])
        pl.margins(0.5)

        # pl.show()
        pl.savefig(
            "figure.pdf",
            orientation="landscape",
            # papertype="a3",
            format="pdf",
            dpi=600,
            bbox_inches="tight",
        )
