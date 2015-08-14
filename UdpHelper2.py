import pickle
import socket
buflen = 1024

class Link:
	def __init__(self, portA, portB, dist):
		self.ports = set([portA, portB])
		self.dist = dist

class Test:
	def __init__(self, dist):
		self.dist = dist

class Err:
	def __init__(self, errmsg):
		self.err = errmsg

def SendObj(sock, obj, address, timeout = .5):
	data = pickle.dumps(obj)
	sock.sendto(data, address)
	print "Message sent from Node (Port {0}) to Node (Port {1})".format(sock.getsockname()[1], address[1])

def SendTest(sock, address, timeout = .5):
	data = pickle.dumps(Test())
	sock.sendto(data, address)
	print "Message sent from Node (Port {0}) to Node (Port {1})".format(sock.getsockname()[1], address[1])
	obj, rcvdAddr = ReceiveObj(sock, timeout)
	#check that the ACK is received from the same sender..
	if isinstance(obj, Test) and rcvdAddr[1] == address[1]:
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

def findLink(localLinks, link):
	for l in localLinks:
		print l.ports, link.ports
		if l.ports.intersection(link.ports) == l.ports:
			return l
	return None
