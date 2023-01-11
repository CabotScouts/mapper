from mapper import PostcodeMapper

markers = [
    [51.501640, -0.141122, "green"],  # Buckingham Palace
    [51.507802, -0.076103, "orange"],  # Tower of London
]

if __name__ == "__main__":
    p = PostcodeMapper(title="An Example Map")
    p.importXLS(
        "example.xslx",  # input xlsx file
        "all",  # name of workbook
        "A",  # column of postcodes
        True,  # does the column have a header?
    )
    p.addMarkers(markers)
    p.makeMap(file="map.pdf", paper="a4", orientation="landscape")
