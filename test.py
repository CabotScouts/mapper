from mapper import PostcodeMapper

if __name__ == "__main__" :
	p = PostcodeMapper()
	p.importXLS('postcodes.xlsx', 'Spaniorum', 'A', True)
	p.heatmap()
