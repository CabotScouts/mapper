from mapper import PostcodeMapper

colour = "yellow"
groups = [
    [51.478694, -2.598413, colour], # 1st Bishopston
    [51.480797, -2.600790, colour], # 3rd Bristol
    [51.455414, -2.620371, colour], # 7th Bristol
    [51.466310, -2.600189, colour], # 18th Bristol
    [51.487019, -2.618401, colour], # 26th Bristol
    [51.480802, -2.632638, colour], # 43rd Bristol
    [51.482790, -2.609786, colour], # 44th Bristol
    [51.486130, -2.589508, colour], # 62nd Bristol
    [51.474631, -2.583211, colour], # 63rd Bristol
    [51.492844, -2.617409, colour], # 90th Bristol
    [51.479488, -2.589410, colour], # 91st Bristol
    [51.486301, -2.651812, colour], # 126th Bristol
    [51.486417, -2.624055, colour], # 167th Bristol
    [51.512744, -2.615185, colour], # 169th Bristol
    [51.490045, -2.680752, colour], # 191st Bristol
    [51.490904, -2.608534, colour], # 227th Bristol
]

if __name__ == "__main__":
    p = PostcodeMapper()
    p.importXLS("network_2023.xlsx", "all", "A", False)
    p.addMarkers(groups)
    p.makeMap(file="network.pdf", paper="a3", orientation="landscape")
