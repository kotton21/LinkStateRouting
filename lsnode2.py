import SocketServer
import sys
import argparse
import socket
execfile("UdpHelper2.py")

#class MyUDPHandler(SocketServer.BaseRequestHandler):
	"""
	This class works similar to the TCP handler class, except that
	self.request consists of a pair of data and client socket, and since
	there is no connection the client address must be given explicitly
	when sending data back via sendto().
	"""
#def start(me, links):
#me = me #local address tuple (hostname, port)
sock = None
links = [] #links #local links to other nodes
packets = [] #all received packets (links)

def trysend(sock, obj, me, links)
	for link in links:
		if not SendObj(sock, obj, ("localhost", link.ports.remove(me[1]).pop() )):
			print "Node (Port {0}) can not reach Node (Port {1})".format(me[1],
				 neighbor.port)
			print "Link failure occured. Program terminated."
			#TODO try to initiate reverify
			close()


def startflood(me, links):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(me)
	#return forwardPackets(sock, me, links, packets, newpackets)
	trysend(sock, link, me, [link])

def forwardPackets(sock, me, links, packets, newpackets):
	for packet in newpackets:
		link = findLink(links, packet)
		checkLink( link, packet )
		packet = findLink(packets, packet)
		checkLink( link, packet )
		if  link == None and  packet == None:
			trysend(sock, packet, me, links)
			packets.append(packet)

def checkLink(link, packet):
	if link != None:
		if link.dist != newpacket.dist:
			print "Link cost from Node (Port {0} to Node (Port {1}) is {2}".format(rcvdAddr[1],
					 me.port, obj.neighbor.dist)
			print "Link cost from Node (Port {0} to Node (Port {1}) is {2}".format(me.port,
					rcvdAddr[1], mySender.dist )
			print "Link cost does not match. Program terminated."
			
			#TODO restart verification
			
			close()
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
	def close():
		if sock != None:
			sock.close()
			sock = None
		shutdown()
		sys.exit()
"""
server = SocketServer.UDPServer(me, MyUDPHandler)
	server.me = me
	server.links = links #) # = links
	try:
		server.serve_forever()
"""
def runServer(links, me, last):
	links = links #local links to other nodes
	packets = [] #all received packets
	if last:
		flood(me, links, [], [],
	try:
		while True:
			obj, rcvdAddr = ReceiveObj(sock, None)
			if isinstance(obj, Link):
				print "inside"
				SendACK(sock, rcvdAddr)
				forwardPackets(sock, self.me, self.links, self.packets, [obj])
			elif isinstance(obj, ACK):
				print 'unknown ack received from {0}'.format(rcvdAddr)
			elif isinstance(obj, Err):
				print 'Err received from {0}: {1}'.format(rcvdAddr, obj.errmsg)
	except KeyboardInterrupt:
		print "Program Terminated"
		server.close()



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

	runServer(links, me)
	
