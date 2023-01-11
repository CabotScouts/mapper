from mapper import PostcodeMapper

colour = "yellow"

# TODO: Expand this to include all Groups in the District
groups = [
    [51.478694172420, -2.598413827911, colour], # 1st Bishopston
    [51.486130609067, -2.589508893981, colour], # 62nd Bristol
    [51.474631348063, -2.583211067214, colour], # 63rd Bristol
    [51.512744513854, -2.615185680881, colour], # 169th Bristol
    [51.487019158751, -2.618401649490, colour], # 26th Bristol
    [51.466310529702, -2.600189450279, colour], # 18th Bristol
    [51.486417886423, -2.624055746093, colour], # 167th Bristol
    [51.482790041811, -2.609786394134, colour], # 44th Bristol
]

if __name__ == "__main__":
    p = PostcodeMapper()
    p.importXLS("network_2023.xlsx", "all", "A", False)
    # p.addMarkers(groups)
    p.makeMap(file="network.pdf", paper="a3", orientation="landscape")
