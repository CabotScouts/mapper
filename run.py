from mapper import PostcodeMapper

if __name__ == "__main__":
    p = PostcodeMapper()
    p.importXLS("input.xlsx", "all", "A", True)
    p.makeMap()
