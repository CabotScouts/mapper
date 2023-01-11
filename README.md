# mapper
## Installation
* libgeos - `sudo apt -y install libgeos-dev`
* cartopy + dependencies - `pip install -r requirements.txt`

## Development
### TODO:
* Caching of postcodes into local csv (is it possible to get all postcodes in the UK in advance and skip calling the API altogether?)
* Expand map tiles to fill paper
* Add more paper sizes?
* Import of postcodes from csv (create example file with postcodes around Central London)
* Static method to load markers from a CSV into numpy array