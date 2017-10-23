#!/usr/bin/env python


import os, re, sys
import socket
import struct

class proc():
    def __init__(self):
        uname = os.uname ()
        if uname[0] == "Linux":
            self.proc = '/proc'
        else:
            raise("Unsupported OS!\n")

    def paths(self, *args):
        return  os.path.join(self.proc, *(str(pth) for pth in args))

    def file_opener(self, tfile):
        lines = []
        with open(tfile, 'r') as ftopener:
            for line in ftopener.readlines():
                line = line.strip()
                lines.append(line)
            ftopener.close()

        return lines


def getprocess_sockets():

    def socketHandler(sourcesock, destsock):
        print "\tBuilding Socket Profile..."
        source_address = socket.inet_ntoa(struct.pack('<L', int(sourcesock.split(":")[0], 16)))
        source_port = int(sourcesock.split(":")[1], 16)
        dest_address = socket.inet_ntoa(struct.pack('<L', int(destsock.split(":")[0], 16)))
        dest_port = int(destsock.split(":")[1], 16)
        return (source_address, source_port, dest_address, dest_port)

    process = proc()

    for fd in os.listdir(process.proc):
        if not fd.isdigit():
            continue
        process_name = open(process.paths(fd, 'comm'), 'r')
        print "Analyzing Process: %s(%s)" % (process_name.read(), fd)
        process_name.close()
        descriptor_path = process.paths(fd, 'fd')
        symlinks_inodes = [os.path.realpath(process.paths(descriptor_path, sym)).split("[") for sym in os.listdir(descriptor_path) if 'socket' in os.path.realpath(process.paths(descriptor_path, sym))]
        inode_list = []
        for inode in symlinks_inodes:
            try:
                inode_list.append(re.sub(r']', "", inode[1]))
            except:
                pass
        for proc_inode in inode_list:
            with open(process.paths(fd, 'net', 'tcp'), 'r') as fsocket:
                for line in fsocket.readlines():
                    if proc_inode in line:
                        source = line.split()[1]
                        destination = line.split()[2]
                        (sourceaddr, sourceport, destaddr, destport) = socketHandler(source, destination)
                        print "\tSockets Found"
                        print "\t\tSource[socket] %s:%s" % (sourceaddr, sourceport)
                        print "\t\tDestination[socket]: %s:%s" % (destaddr, destport)
                    else:
                        continue
                fsocket.close()
if __name__ == "__main__":
    getprocess_sockets()