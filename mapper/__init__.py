import csv
from pathlib import Path
from openpyxl import load_workbook
import urllib.parse
import requests
import matplotlib.pyplot as pl
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import numpy

from pprint import pprint


class PostcodeMapper(object):

    endpoint = "http://api.getthedata.com/postcode/"
    coords = []

    csvfields = ["postcode", "longitude", "latitude"]
    cache = dict()
    cachefile = None
    recache = False

    # Number of bins for histogram - smaller = less resolution
    xbins = 28
    ybins = 28

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
        # Import coordinates of Units to add to plot
        units = numpy.array()

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

        units = self.getUnits()
        unps = ax.projection.transform_points(
            ccrs.Geodetic(), units[:, 1].astype(float), units[:, 0].astype(float)
        )
        # pl.scatter(unps[:,0], unps[:,1], s=100, c=units[:,2], marker='D')
        pl.scatter(unps[:, 0], unps[:, 1], s=100, c="purple", marker="D")

        # ax.set_extent([51.526760, 51.454065, -2.698467, -2.564378])
        pl.margins(0.5)

        # pl.show()
        pl.savefig(
            "figure.pdf",
            orientation="landscape",
            papertype="a3",
            format="pdf",
            dpi=600,
            bbox_inches="tight",
        )
