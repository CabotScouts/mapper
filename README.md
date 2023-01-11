# mapper
This modules acts as a wrapper for the `matplotlib` and `cartopy` libraries, creating a fairly simple way of plotting postcode data
from a spreadsheet (e.g. exported from OnlineScoutManager) onto a map.

Also allows for the plotting of coloured markers to identify points of interest (Explorer Unit meeting places, Scout Groups etc.).

## Installation
* [libgeos](https://libgeos.org/usage/install/)
* cartopy + dependencies - `pip install -r requirements.txt`

## Generating a map
`example.py` gives an example of loading postcodes from a spreadsheet, plotting two markers, and then saving the map as a pdf (A4 landscape)

## Future development
* Caching of postcodes into local csv (is it possible to get all postcodes in the UK in advance and skip calling the API altogether?)
* Expand map tiles to fill paper
* Add a border around plotted points (find min/max extents from coords and expand slightly)
* Add more paper sizes
* Import of postcodes from csv (create example file with postcodes around Central London)
* Static method to load markers from a CSV into numpy array