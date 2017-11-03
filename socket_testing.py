#!/usr/bin/env python

import socket
import time
class httpconnect(object):

	def __init__(self, addr, port=80, is_encrypted=False):
		self.addr = addr
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.port = port
		if is_encrypted and hasattr(self, 'port'):
			setattr(self, 'port', 443)
			try:
				import ssl
				self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
				setattr(getattr(self, 'context'), 'verify_mode', 1)
				setattr(getattr(self, 'context'), 'check_hostname', True)
				self.context.load_default_certs()
			except ssl.SSLError:
				raise AttributeError("Failed To Create SSL Context\n")
			# wrap socket
			assert hasattr(self, 'context') and hasattr(self, 'sock')
			# increase timeout for ssl
			self.sock.settimeout(10)
			self.ssl_socket = self.context.wrap_socket(self.sock, server_hostname=addr)
			self.ssl_socket.connect((self.addr, self.port))
			self.instance = self.ssl_socket
		else:
			self.sock.connect((self.addr, self.port))
			self.instance = self.sock

	def Get(self, page='/'):
		# the first response will always be the HTTP Server Response code, which is all we want.
		request = "GET %s HTTP/1.0\r\n\r\n" % page
		if hasattr(self, 'instance'):
			self.instance.send(request)
			while True:
				return self.instance.recv(1024).split('\r')[0]


if __name__ == "__main__":
	test_servers = {
		'www.google.com': True, 'www.cnn.com': False, 'www.iastate.edu': True, 'www.facebook.com': True,
		'www.oreilly.com': True, 'www.wikipedia.org': False, 'www.fbi.gov': True, 'www.cia.gov': True,
		'www.harvard.edu': True, 'www.amazon.com': True, 'www.twitter.com': True,'www.instagram.com': False,
		'www.ncaa.org': True
	}

	for uri, encrytpion in test_servers.iteritems():
		start = time.time()
		print "Testing URI: %s" % uri
		try:
			if not encrytpion:
				test = httpconnect(uri)
			else:
				test = httpconnect(uri, is_encrypted=True)
		except:
			print "\t[*]Failed...."
		print "\t"+test.Get()
		print "\tElapsed Time: %s" % (time.time() - start)