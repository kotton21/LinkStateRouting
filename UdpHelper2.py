import pickle
import socket
buflen = 1024

class Link:
	def __init__(self, portA, portB, dist):
		self.ports = set([portA, portB])
		self.dist = dist

class ACK:
	def __init__(self):
		pass

class Err:
	def __init__(self, errmsg):
		self.err = errmsg
"""
class Verification:
	def __init__(self,neighbor, sender):
		self.neighbor = neighbor
		#self.sender = sender

class Neighbor:
	def __init__(self, port, dist):
		self.port = port
		self.dist = dist
		self.verified = False
	def toString(self):
		print "({0}, {1}) {2}".format(self.port, self.dist, self.verified)

class VerificationACK:
	def __init__(self, neighbor):
		self.neighbor = neighbor

def printable(s):
	if s is not None:
		print s
	print ">>> ",
	sys.stdout.flush()
"""
# tries 5 times to send/receive the object. 
# returns False if no ACK received
def SendObj(sock, obj, address, timeout = .5):
	data = pickle.dumps(obj)
	for i in range(5):
		sock.sendto(data, address)
		print "Message sent from Node (Port {0}) to Node (Port {1})".format(sock.getsockname()[1], address[1])
		'''
		obj = None
		while not isinstance(obj, ACK) or rcvdAddr[1] != address[1]:
			try:
				received, rcvdAddr = sock.recvfrom(buflen)
				obj = UnpackData(received.strip())
			except socket.timeout:
				pass
		'''
		obj, rcvdAddr = ReceiveObj(sock, timeout)
		#check that the ACK is received from the same sender..
		if isinstance(obj, ACK) and rcvdAddr[1] == address[1]:
			return True
		
	return False

#waits the length of timeout to receive an object
def ReceiveObj(sock, timeout):
	sock.settimeout(timeout)
	obj = None
	rcvdAddr = None
	try:
		received, rcvdAddr = sock.recvfrom(buflen)
		obj = UnpackData(received.strip())
		print "Message received at Node (Port {0}) from Node (Port {1})".format(sock.getsockname()[1], rcvdAddr[1])
		if isinstance(obj,ACK):
			print "ACK"
		elif isinstance(obj,Link):
			print "link"
	except socket.timeout:
		pass
	return obj, rcvdAddr

def SendACK(sock, address):
	data = pickle.dumps(ACK())
	sock.sendto(data, address)
	#print "sent ACK"

def UnpackData(data):
	object = pickle.loads(data)
	return object

def findLink(localLinks, link):
	for l in localLinks:
		print l.ports, link.ports
		if l.ports.intersection(link.ports) == l.ports:
			return l
	return None
"""
def find(neighbors, port):
	print "finding port",port
	for neighbor in neighbors:
		print neighbor.port, port
		if int(neighbor.port) == int(port):
			return neighbor
	return None
"""
