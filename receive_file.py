import serial
import time
import Image

####################################################
# this was the first experiment I made to build the 
# scanning electron microscope interface 
####################################################

#FIRMWARE COMMANDS
#a - send file
#b - nothing
#c - send byte stream
#d - advance next byte
#e - exit bytestrem mode
####################################################
"""

To ascii int.
ord('a')
gives 97

And back to a string:
str(unichr(97))
gives 'a'


"""
####################################################

SERIAL_DEVICE = '/dev/ttyUSB1' #'/dev/tty.usbserial'
SERIAL_PORT   = serial.Serial(SERIAL_DEVICE, 9600)
  
BUFFERSIZE    = 0
RX_BUFFER     = []
directoryPath = '/received_file.binary'
#############

#get file size in (int) num bytes
SERIAL_PORT.write("b") 
BUFFERSIZE= ord( SERIAL_PORT.read(1))

#now transfer file 
SERIAL_PORT.write("c") #hey send me the file!
for i in range(BUFFERSIZE):
   SERIAL_PORT.write("d") #next byte please
   #print hex(ord(SERIAL_PORT.read(1) ))
   RX_BUFFER.append( ord(SERIAL_PORT.read(1) ) )

print "\ndone receiving!\n"

print RX_BUFFER

#write it to a binary
newFile = open (directoryPath, "wb")
newFileByteArray = bytearray(RX_BUFFER)
newFile.write(newFileByteArray)


print "\ndone writing file!\n"

####################################################
"""
class uart_sdcard:
 
    def __init__(self):
       self.device = '/dev/ttyUSB1' 
       self.port   = serial.Serial(self.device, 9600)
       self.buffer_size = 256
       self.rx_buffer = []
       self.delaytime = .001 # pause between bytes sent

    ######
    def read_bmp(self):
	self.port.write("c") #c
	while(1):
	  time.sleep(self.delaytime)
	  self.port.write("d") #0x44) #c
	  print self.port.read(1)
    ###### 


    ######


talker = uart_sdcard()
talker.read_bmp()
"""
####################################################

















####################################################
"""

"""

