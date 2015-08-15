import pickle
import socket
buflen = 1024

class Link:
	def __init__(self, port, dist):
		self.port = port
		self.dist = dist
		self.conf = False
	def toString(self):
		return "{0}: {1}, conf: {2}".format(self.port, self.dist, self.conf)

# object to signal the flooding step, and allow forwarding to other links.
class Packet:
	def __init__(self, ports, dist):
		self.ports = ports
		self.dist = dist
	def toString(self):
		return "{0}: {1}".format(self.port, self.dist)

# object to signal the verification step and confirm the distance to a node
class Verification:
	def __init__(self, dist):
		self.dist = dist

class Err:
	def __init__(self, errmsg):
		self.err = errmsg

def SendObj(sock, obj, address, timeout = .5):
	data = pickle.dumps(obj)
	sock.sendto(data, address)
	print "Message sent from Node (Port {0}) to Node (Port {1})".format(sock.getsockname()[1], address[1])

"""
def SendTest(sock, address, timeout = .5):
	data = pickle.dumps(Test())
	sock.sendto(data, address)
	print "Message sent from Node (Port {0}) to Node (Port {1})".format(sock.getsockname()[1], address[1])
	obj, rcvdAddr = ReceiveObj(sock, timeout)
	#check that the ACK is received from the same sender..
	if isinstance(obj, Test) and rcvdAddr[1] == address[1]:
		return True	
	return False
"""
#waits the length of timeout to receive an object
def ReceiveObj(sock, timeout):
	sock.settimeout(timeout)
	obj = None
	rcvdAddr = None
	try:
		received, rcvdAddr = sock.recvfrom(buflen)
		obj = UnpackData(received.strip())
		print "Message received at Node (Port {0}) from Node (Port {1})".format(sock.getsockname()[1], rcvdAddr[1])
		#if isinstance(obj,ACK):
		#	print "ACK"
		#elif isinstance(obj,Link):
		#	print "link"
	except socket.timeout:
		pass
	return obj, rcvdAddr

def UnpackData(data):
	object = pickle.loads(data)
	return object

def findLink(localLinks, port):
	for l in localLinks:
		#print l.ports, link.ports
		if l.port == port:
			return l
	return None

def findPacket(packets, ports):
	for p in packets:
		if ports.issubset(p.ports):
			return p
	return None
