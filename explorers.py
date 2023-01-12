from mapper import Mapper
from cabot import units

if __name__ == "__main__":
    p = Mapper()
    p.importXLS("input.xlsx", "all", "A", False)
    p.addMarkers(units)
    p.makeMap(file="joining_list.pdf", paper="a3", orientation="landscape")
