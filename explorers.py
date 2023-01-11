from mapper import PostcodeMapper

units = [
    [51.472855, -2.584198, "red"], # Arizona
    [51.4786941724208, -2.598413827911372, "red"],  # Brabazon
    [51.486130609067075, -2.589508893981929, "orange"],  # Concorde
    [51.47463134806349, -2.583211067214961, "orange"],  # Phoenix
    [51.512744513854194, -2.6151856808814955, "green"],  # Pirates
    [51.487019158751714, -2.6184016494903517, "orange"],  # Spaniorum
    [51.46631052970262, -2.600189450279231, "green"],  # Spitfire
    [51.48641788642314, -2.6240557460937453, "red"],  # Steama
    [51.48279004181177, -2.6097863941345167, "orange"],  # White Tree
]

if __name__ == "__main__":
    p = PostcodeMapper()
    p.importXLS("input.xlsx", "all", "A", False)
    p.addMarkers(units)
    p.makeMap(file="joining_list.pdf", paper="a3", orientation="landscape")
