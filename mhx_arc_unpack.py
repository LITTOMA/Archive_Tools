import os,sys,zlib
from struct import unpack as bin_unpack

class c_file(object):
	def __init__(self,data):
		self.filename = readstring(data)
		self.offset = bin_unpack('<I', data[0x4C:])[0]
		self.size = bin_unpack('<I', data[0x44:0x48])[0]
		self.data = ''

def mkdir(path):
        isExists=os.path.exists(path)
        if not isExists:
                os.makedirs(path)
                return True
        else:
                return False

def readstring(data):
	s = ''
	for c in data:
		if not c == '\x00':
			s += c
		else:
			return s

def unpack(filename):
	with open(filename,'rb')as arc:
		arc.seek(6,0)
		filecount = bin_unpack('H', arc.read(2))[0]
		arc.seek(4, 1)

		c_entries = []

		for i in range(filecount):
			c_entry = c_file(arc.read(0x50))
			c_entries.append(c_entry)
		for i in range(filecount):
			arc.seek(c_entries[i].offset, 0)
			try:
				c_entries[i].data = zlib.decompress(arc.read(c_entries[i].size))
			except:
				c_entries[i].data = arc.read(c_entries[i].size)
				print 'Decompress Failed.'

		for e in c_entries:
			path = os.path.splitext(filename)[0] + '_' + os.path.splitext(filename)[1][1:] + '\\'
			path = path + e.filename
			mkdir(os.path.split(path)[0])
			with open(path, 'wb')as outfile:
				print 'Save:', path
				outfile.write(e.data)


for filename in sys.argv[1:]:
	unpack(filename)
