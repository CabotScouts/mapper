from mapper import Mapper

markers = [
    [51.501640, -0.141122, "yellow"],  # Buckingham Palace
    [51.507802, -0.076103, "orange"],  # Tower of London
]

if __name__ == "__main__":
    p = Mapper(title="An Example Map")
    p.importPostcodesFromCSV(
        file="example.csv",  # input csv file
        column="postcodes",  # column of postcodes
        header=True,  # does the column have a header?
    )
    p.addMarkers(markers)
    p.makeMap(file="example_map.pdf", paper="a4", orientation="landscape")
