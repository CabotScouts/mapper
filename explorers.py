from mapper import PostcodeMapper
from cabot import units

if __name__ == "__main__":
    p = PostcodeMapper()
    p.importXLS("input.xlsx", "all", "A", False)
    p.addMarkers(units)
    p.makeMap(file="joining_list.pdf", paper="a3", orientation="landscape")
