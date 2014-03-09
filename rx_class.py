import serial
import time
import Image



####################################################
"""
 #modular communication protocol
 #defined on AVR/Arduino firmware

 #HEADER 
    4 bytes for filesize (128*128*128*remainder)
    
 
"""

class uart_protocol:
    def __init__(self):
       self.init  = '' #initialize
       self.ack   = '' #acknowledge
       self.nack  = '' #non acknowledge
       self.gfsz  = '' #get file size
       self.bft   = '' #begin file xfer
       self.gnb   = '' #get next byte
       self.gwf   = '' #get whole file
       ####
       self.simple()

    def simple(self):
       self.init  = ''  #initialize
       self.ack   = ''  #acknowledge
       self.nack  = ''  #non acknowledge
       self.gfsz  = 'b' #get file size
       self.bft   = 'c' #begin file xfer
       self.gnb   = 'd' #get next byte #"e" terminates 
       self.gwf   = 'f' #get next byte
####################################################
class uart_io_port:
 
    def __init__(self):
       self.ptcl          = uart_protocol()
       self.device        = '/dev/ttyUSB0' 
       self.baud          = 115200
       self.port          = ''
       self.buffer_size   = 0
       self.rx_buffer     = []
       self.connected = False
    ######
    def reset(self):
       self.buffer_size   = 0
       self.rx_buffer     = []

    ######
    def connect(self):
        self.port =serial.Serial(self.device, self.baud)
        self.connected = True
    ######
    def disconnect(self):
        self.connected = False
    ######
    def check_connected(self):
       if (self.connected==False):
           raise Exception('Serial port not connected.')
    ###### 
    def ask_fsize(self):
        self.check_connected()
        self.reset()
        fsize = long(0)
        self.port.write(self.ptcl.gfsz) 
        b1= ord( self.port.read(1))
        b2= ord( self.port.read(1))
        b3= ord( self.port.read(1))
        b4= ord( self.port.read(1))
        b5= ord( self.port.read(1))
        ##################
        fsize = b1*268435456
        fsize = b2*2097152
        fsize = fsize+b3*16384
        fsize = fsize+b4*128
        fsize = fsize+b5
        #print b1,b2,b3,b4,b5
        #print "SIZE IS "+ str(fsize)
        self.buffer_size = fsize

    ######
    def read_stream(self):
        self.check_connected()
        self.reset()
        self.ask_fsize()
	self.port.write(self.ptcl.bft) 
	for i in range(self.buffer_size):
	   self.port.write(self.ptcl.gnb) 
	   print( ord(self.port.read(1) ) )
    ######
    #slow because it "asks" for each byte
    def recieve_file(self):
        self.check_connected()
        self.reset()
        self.ask_fsize()
	self.port.write(self.ptcl.bft) 
	for i in range(self.buffer_size):
	   self.port.write(self.ptcl.gnb) 
	   self.rx_buffer.append( ord(self.port.read(1) ) )
    ######
    def fast_recieve(self):
        self.check_connected()
        self.reset()
        self.ask_fsize()
	self.port.write(self.ptcl.gwf) 
        tempbuf = self.port.read(self.buffer_size) 
        for x in tempbuf:
           self.rx_buffer.append( ord(x) )
          

    ######
    def show_buffer(self):
        print self.rx_buffer
    ######
    def save_binary(self, filepath):
	newFile = open ( filepath, "wb")
	newFileByteArray = bytearray(self.rx_buffer)
	newFile.write(newFileByteArray)
        print 'saved file '+filepath

####################################################

class interface:
   def __init__(self):
      self.dev =uart_io_port()

   def init(self):
      self.dev.connect()
      self.dev.ask_fsize()
      print 'file size is '+str(self.dev.buffer_size)

   def get_file(self,outpath):
        self.init()
	self.dev.fast_recieve()
	self.dev.save_binary(outpath)

   def slow_get_file(self,outpath):
        self.init()
	self.dev.recieve_file()
	#self.dev.show_buffer()
	self.dev.save_binary(outpath)


###

I = interface()
#I.init()
I.get_file('/keith/amazing.zip')

###
