import SocketServer
import sys
import argparse
import socket
execfile("UdpHelper2.py")

class MyLinkStateHandler:
	"""
	This class works similar to the TCP handler class, except that
	self.request consists of a pair of data and client socket, and since
	there is no connection the client address must be given explicitly
	when sending data back via sendto().
	"""
	def __init__(self, links, me, last):
		self.me = me			# (hostname, port)
		self.links = links		# my directly connected links
		self.packets = []		# all previously received packets (links)
		self.last = last			# boolean (indication of last)
		 # build the socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
		self.sock.bind(me)
		# start the server
		self.runServer()

	def startflood(self):
		print "Message flooding started."
		for link in self.links:
			print "links", link.ports
			self.trysend(self.sock, link, me, links)

	#try to send the given obj to all the direct 'links'
	def trysend(self, sock, obj, me, links):
		for link in links:
			to = link.ports.difference([me[1]]).pop()
			print "sending obj to",to
			if not SendObj(sock, obj, ("localhost", to )):
				print "Node (Port {0}) can not reach Node (Port {1})".format(me[1],
					 to)
				print "Link failure occured. Program terminated."
				#TODO try to initiate reverify
				self.close()
			else:
				self.packets.append(obj)

	def forwardPackets(self, sock, me, links, packets, rcvdpackets):
		for rcvdpacket in rcvdpackets:
			#check if the packet is in the already-sent-packets list (and check distance)...
			packet = findLink(packets, rcvdpacket)
			self.checkLink( rcvdpacket, packet )
			#if we don't have them, then forward!
			if packet == None:
				print "forwarding packet"
				self.trysend(sock, packet, me, links)
		return packets

	def checkLink(self, link, packet):
		if link != None and packet != None:
			print "checklink", link, packet
			if link.dist != packet.dist:
				print "Link cost from Node (Port {0} to Node (Port {1}) is {2}".format(rcvdAddr[1],
						 me.port, obj.dist)
				print "Link cost from Node (Port {0} to Node (Port {1}) is {2}".format(me.port,
						rcvdAddr[1], mySender.dist )
				print "Link cost does not match. Program terminated."
			
				#TODO restart verification
			
				self.close()
	"""
		def handle(self):
			#self.server? raise some exception when table is updated?
			data = self.request[0].strip()
			sock = self.request[1]
			rcvdAddr = (self.client_address[0], self.client_address[1])
			obj = unpackData(data)
		
			#servermode functions....
			if isinstance(obj, Link):
				print "inside"
				SendACK(sock, rcvdAddr)
				forwardPackets(sock, self.me, self.links, self.packets, [obj])
	"""
	def close(self):
		if self.sock != None:
			self.sock.close()
			self.sock = None
		#shutdown()
		sys.exit()
	"""
	server = SocketServer.UDPServer(me, MyUDPHandler)
		server.me = me
		server.links = links #) # = links
		try:
			server.serve_forever()
	"""
	def runServer(self):
		#links = links #local links to other nodes
		
		if self.last:
			self.startflood()
		try:
			while True:
				obj, rcvdAddr = ReceiveObj(self.sock, None)
				if isinstance(obj, Link):
					SendACK(self.sock, rcvdAddr)
					if len(self.packets) == 0:
						self.startflood()
					self.packets = self.forwardPackets(self.sock, self.me, self.links, self.packets, [obj])
				elif isinstance(obj, ACK):
					print 'unknown ack received from {0}'.format(rcvdAddr)
				elif isinstance(obj, Err):
					print 'Err received from {0}: {1}'.format(rcvdAddr, obj.errmsg)
		except KeyboardInterrupt:
			print "Program Terminated"
			self.close()



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Simple link-state routing')

	parser.add_argument('port', metavar='<local-port>', type=int,
                   help='The UDP listening port number of the node.')
	parser.add_argument('neighbors', nargs='*' , type=int,
			metavar='<neighbor-port> <neighbor-dist>',
			help='Pairs of [neighor-port, distance]')
	parser.add_argument('last', nargs=1, metavar='<last>',
                   help='Indication of last node in the network')
	#print( parser.format_help() )
	args = parser.parse_args()

	print args.last
	if not args.last[0] == 'last':
		args.neighbors.append(int(args.last[0]))
		args.last = False
	else:
		args.last = True
	if len(args.neighbors)%2 == 1:
		print( parser.format_help() )
		print 
		sys.exit()
	
	me = ("localhost", args.port )
	links = []
	i=0
	while i< len(args.neighbors):
		links.append( Link(me[1], args.neighbors[i], args.neighbors[i+1]) )
		i = i+2

	for link in links:
		print link.ports, link.dist

	server = MyLinkStateHandler(links, me, args.last)


	
