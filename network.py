from mapper import Mapper
from cabot import groups, pubs

if __name__ == "__main__":
    p = Mapper(title="Network Members")
    p.importXLS("network.xlsx", "all", "A", False)
    p.addMarkers(groups("yellow"))
    p.addMarkers(pubs("magenta"))
    p.makeMap(file="network.pdf", paper="a3", orientation="landscape")
