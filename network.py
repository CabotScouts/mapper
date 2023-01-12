from mapper import Mapper
from cabot import groups, pubs

if __name__ == "__main__":
    p = Mapper(title="Network Members")
    p.importPostcodesFromXLS(file="network.xlsx", sheet="all", column="A", header=False)
    p.addMarkers(groups("yellow"))
    p.addMarkers(pubs("magenta"))
    p.makeMap(file="network.pdf", paper="a3", orientation="landscape")
