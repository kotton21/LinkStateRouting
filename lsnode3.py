import SocketServer
import sys
import argparse
import socket
from threading import Timer
execfile("UdpHelper3.py")

class MyLinkStateHandler:
	def __init__(self, links, me, last):
		self.me = me			# (hostname, port)
		self.t = None 			# timer for the initiating thread
		self.links = links			# my directly connected links
		#self.confirmed = [] 	# confirmed links during the verify stage
		
		self.packets = []		# all previously received packets (links)
		self.last = last			# boolean (indication of last)
		 # build the socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
		self.sock.bind(me)
		
		# start the server
		
		self.verifying = False
		self.flooded = False
		self.runServer()

	def VerifyAll(self, sock, links):
		self.verifying = True
		print "starting network handshake"
		for link in links:
			print "sending to",link.port
			SendObj(sock, Verification(link.dist), ("localhost", link.port ))
	def StopVerification(self):
		self.verifying = False
		print 'in stopVerify'
		for link in links:
			print link.toString()
		for link in links:
			if not link.conf:
				print "Node (Port {0}) can not reach Node (Port {1})".format(me[1],
					 link.port)
				print "Link failure occured. Program terminated."
				self.close()
		print	"Network Verification complete"
		self.startflood()
		
	def startflood(self, sender = None):
		if self.flooded == False:
			print "Message flooding started."
			self.t = Timer(5, self.StopFlood)
			self.t.start()
			# send each link to each link
			for sendingtolink in self.links:
				if sendingtolink.port != sender:
					print "flooding to link", sendingtolink.port
					for linktosend in self.links:
						#convert link to packet
						packet = Packet(set([self.me[1],linktosend.port]),linktosend.dist)
						#send out the packet
						SendObj(self.sock, packet, ("localhost", sendingtolink.port ))
			self.flooded = True
		else:
			print "already flooded"
		
	def StopFlood(self):
		print "messageflooding stoped"
		for packet in self.packets:
			print packet.ports, packet.dist

	"""
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
	#
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
		if self.t != None:
			self.t.cancel()
			self.t = None
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
			#self.startflood()
			self.t = Timer(1, self.StopVerification)
			self.t.start()
			self.VerifyAll(self.sock, self.links)
		print "listening ..."
		try:
			while True:
				obj, rcvdAddr = ReceiveObj(self.sock, None)
				if isinstance(obj, Packet):
					#SendACK(self.sock, rcvdAddr)
					#if len(self.packets) == 0:
					if not self.flooded:
						self.startflood()
					#check for previously received packets"
					packet = findPacket(self.packets, obj.ports)
					if packet == None:
						print "link not found, appending",obj.ports
						self.packets.append(obj)
						for link in self.links:
							SendObj(self.sock, obj, ("localhost", link.port ))
				
				# Verify the netork links
				elif isinstance(obj, Verification):
					link = findLink(self.links, rcvdAddr[1])
					if link != None and obj.dist == link.dist:
						print rcvdAddr,'confirmed'
						link.conf = True
						if  not self.verifying:
							self.VerifyAll(self.sock, self.links)
					else: 
						print "Link cost from Node (Port {0} to Node (Port {1}) is {2}".format(rcvdAddr[1],
						 		me[1], obj.dist)
						print "Link cost from Node (Port {0} to Node (Port {1}) is {2}".format(me[1],
								rcvdAddr[1], link.dist )
						print "Link cost does not match. Program terminated."
						self.close()
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
		links.append( Link(args.neighbors[i], args.neighbors[i+1]) )
		i = i+2

	for link in links:
		print link.port, link.dist

	server = MyLinkStateHandler(links, me, args.last)


	
