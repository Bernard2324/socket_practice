#!/usr/bin/env python

import socket

def socket_fd_list(listofsockets):
	'''
	This function takes a list of created sockets, then prepares them with the necessary socket
	options set, and returns the file descriptors of readable sockets.

	This function also returns readable and writable sockets
	'''
	socket_nest = {}
	if listofsockets is None:
		raise RuntimeError("Failed To Pass A List of Sockets!")

	def setopt(tsocket):
		# manipulates sockets 'in-flight', no return

		if not tsocket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR):
			tsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		tsocket.setblocking(0)

	try:
		map(setopt, listofsockets)
	except:
		raise RuntimeError("Failed To Prepare SOCKETs for Use!")

	
	waittime = 60
	from select import select
	(read, write, exe) = select(listofsockets, listofsockets, [], waittime)

	read_fd = [sock.fileno() for sock in read]
	write_fd = [sock.fileno() for sock in write]

	socket_nest['read'] = [read_fd, read]
	socket_nest['write'] = [write_fd, write]

	return socket_nest


def test():
	sock_list = []
	for x in range(10):
		sname = str(x)
		sname = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock_list.append(sname)

	sock_handle = socket_fd_list(sock_list)
	
	write_pair = [sock_handle['write'][0][0], sock_handle['write'][1][0]]

	write_pair[1].connect_ex(("localhost", 10000))
	
	print "Connection Established[%s]" % str(write_pair[0])
	write_pair[1].send("Hello Moe\n")

test()
