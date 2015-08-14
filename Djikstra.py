class Djikstra:
	def __init__(self, packets, startnode):
		''' useless
		ports = [packet.ports for packets in nodes]
		nodes = set([])
		for port in ports:
			nodes = nodes.union(port)
		print nodes
		self.nodes = packets
		
		
		for node in nodes:
			if node.ports
		'''
		for packet in packets:
					
		
		G = {}					# the full graph of nodes, not just those attached to startnode
		D = {startnode:0}	#this node, distance is 0 to 'itself'
		inf = float("inf")	#infinity
		
		

		for node in G.keys:
			if startnode in G[node].keys:
				D[key] = G
			else:
				D[key] = inf



	# builds the graph. as a dictionary of dictionaries such that G[A][B] == (dist A<->B)
	# This idea was reference from joyrexus/dijkstra on github 
	# https://github.com/joyrexus/dijkstra/blob/master/dijkstra.py
	def buildGraph(packets):
		G = {}
		for packet in packets:
			new = packet.ports.pop()
			if G[new] == None:
				G[new] = { packet.port.pop(): packet.dist }
			else:
				G[new][packet.port.pop()] = packet.dist
		return G
				
