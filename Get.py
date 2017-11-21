#!/usr/bin/evn python

import urllib3

class HttpTimeout(urllib3.Timeout):

	def __init__(self, read_time_out, changeval=None):
		self.connect_time_out = 10

		if changeval is not None:
			setattr(self, 'connect_time_out', changeval)

		super(HttpTimeout, self).__init__(connect=getattr(self, 'connect_time_out'), read=read_time_out)

class Request(object):

	def __init__(self, url, changetimeout=None, readtimeout=10, **kwargs):
		self._default_timeout = HttpTimeout(readtimeout, changeval=changetimeout)
		self.url = url
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(35)
		self.sock.setblocking(False)
		self.port = 80

		if kwargs['ssl']:
			setattr(self, 'port', 443)
			try:
				import ssl
			except ImportError():
				raise StandardError("Import Error Trying to import SSL\
					Please Make sure you are using a modern version of Python (2.7+)\n")
			self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
			setattr(getattr(self, 'context'), 'verify_mode', 1)
			setattr(getattr(self, 'context'), 'check_hostname', True)
			self.context.load_default_certs()
			self.ssl_socket = self.contxt.wrap_socket(self.sock, hostname=self.url)
			self.ssl_socket.connect((self.url, self.port))
			self.instance = self.ssl_socket
		else:
			self.sock.connect((self.url, self.port))
			self.instance = self.sock

	def Get(self, page='/', **kwargs):

		if not hasattr(self, 'instance'):
			raise AttributeError("Your Socket Instance has Expired")

		request = "GET %s HTTP/1.0\r\n\r\n" % page

		request_headers = {
			'Content-Type': 'text/html; encoding=utf8',
			'Content-Length': '214',
			'Connection': 'Keep-Alive',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
				AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
		}

		raw_request_headers  = ''.join('%s: %s\n' % (header_type, header_value) \
			for header_type, header_value in request_headers.iteritems())

		# Insert the GET request to the beginning of SEND() data
		request_packet = [request] + raw_request_headers
		self.instance.send(request_packet)

		data_blocks = []
		while True:
			data = self.instance.recv(1024)
			if data:
				data_blocks.append(data)
			else:
				self.instance.close()
		return "".join(data_blocks)

if __name__ == "__main__":
	http = Request('en.wikipedia.org', changetimeout=30, readtimeout=10, ssl=True)
	webpage = http.Get(page='/wiki/basketball')
	print webpage
