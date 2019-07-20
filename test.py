from mapper import PostcodeMapper

if __name__ == "__main__" :
	p = PostcodeMapper('postcodes.xlsx', 'Sheet1', 'A', True)
	m = p.heatmap(p.coords)
