class Djikstra:
	def __init__(self, packages):
		ports = [package.ports for package in nodes]
		nodes = set([])
		for port in ports:
			nodes = nodes.union(port)
		print nodes
