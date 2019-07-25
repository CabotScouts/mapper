import csv
from pathlib import Path
from openpyxl import load_workbook
import urllib.parse
import requests
import matplotlib.pyplot as pl
# import cartopy.crs as ccrs
# import cartopy.io.img_tiles as cimgt

class PostcodeMapper(object):

	endpoint = "http://api.getthedata.com/postcode/"
	csvfields = ['postcode', 'latitude', 'longitude']
	cache = dict()
	coords = dict()

	# Number of bins for histogram - smaller = less resolution
	xbins = 30
	ybins = 30

	def __init__(self, cache = None) :
		cachefile = cache if cache else "postcodes.csv"
		self.cachefile = Path(cachefile)
		self.loadCache()

	def loadCache(self) :
		# Retrieves cached coordinates, if they exist
		if self.cachefile.is_file() :
			with open(self.cachefile, 'r') as c :
				d = csv.DictReader(c, fieldnames=self.csvfields)
				next(d, None) # Skip header row
				for row in d :
					self.cache[row['postcode']] = (float(row['longitude']), float(row['latitude']))

	def saveCache(self) :
		with open(self.cachefile, 'w') as c :
			d = csv.DictWriter(c, fieldnames=self.csvfields)
			d.writeheader()
			for k, v in self.cache.items() :
				d.writerow({'postcode': k, 'latitude': v[0], 'longitude': v[1]})

	def importXLS(self, file, sheet, column, header) :
		# Read in postcodes from xlsx, convert to coords, then write back to a csv
		wb = load_workbook(filename = file)
		ws = wb[sheet]

		postcodes = [ cell.value for cell in ws[column] ]

		if header :
			del postcodes[0]

		self.coords = self.convertPostcodes(postcodes)
		self.saveCache()

	def convertPostcodes(self, postcodes) :
		return { postcode: self.coordFromPostcode(postcode) for postcode in postcodes }

	def coordFromPostcode(self, postcode) :
		if postcode in self.cache :
			return self.cache[postcode]
		else :
			request = requests.get(self.endpoint + urllib.parse.quote_plus(postcode))
			response = request.json()

			if response['status'] == 'match' :
				coords = ( float(response['data']['latitude']), float(response['data']['longitude']) )
				self.cache[postcode] = coords
				return coords
			else :
				return False

	def heatmap(self) :
		x = [ m[0] for n, m in self.coords.items() if m ]
		y = [ m[1] for n, m in self.coords.items() if m ]

		# request = cimgt.OSM()
		# fig, ax = pl.subplots(figsize=(10,16), subplot_kw=dict(projection=request.crs))
		# extent = [ min(x) - 0.5, min(y) - 0.5, max(x) + 0.5, max(y) + 0.5 ]
		# ax.set_extent(extent)
		# ax.add_image(request, 8)
		#
		# xynps = ax.projection.transform_points(ccrs.Geodetic(), x, y)
		#
		# m = ax.hist2d(xynps[:,0], xynps[:,1], bins=[ self.xbins, self.ybins ], zorder=10, alpha=0.5)
		# cbar = pl.colorbar(m[3], ax=ax, shrink=0.45, format='%.1f')
		m = pl.hist2d(x, y, [ self.xbins, self.ybins ])
		pl.show()
