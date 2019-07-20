from openpyxl import load_workbook
import urllib.parse
import requests
import matplotlib.pyplot as pl

class PostcodeMapper(object):

	endpoint = "http://api.getthedata.com/postcode/"
	postcodes = []
	coords = []

	xbins = 20
	ybins = 20

	def __init__(self, file = None, sheet = None, column = None, header = None) :


	def fromXLS(self, file, sheet, column, header) :
		wb = load_workbook(filename = file)
		ws = wb[sheet]

		postcodes = [ cell.value for cell in ws[column] ]

		if header :
			del postcodes[0]

		return postcodes

	def convertPostcodes(self, postcodes) :
		return [ self.coordFromPostcode(postcode) for postcode in postcodes ]

	def coordFromPostcode(self, postcode) :
		request = requests.get(self.endpoint + urllib.parse.quote_plus(postcode))
		response = request.json()

		if response['status'] == 'match' :
			return ( float(response['data']['latitude']), float(response['data']['longitude']) )
		else :
			return False

	def heatmap(self, coords) :
		x = [ n[0] for n in coords ]
		y = [ n[1] for n in coords ]

		m = pl.hist2d(x, y, [ xbins, ybins ])
		pl.show()
