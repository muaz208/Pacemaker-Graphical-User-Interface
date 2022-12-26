#Steven Samu, samus1, 400311525

import serial
import serial.tools.list_ports as ports
import struct

Start = b'\x16'
SYNC = b'\x22'
Fn_set = b'\x55'


#s = serial.Serial("COM7",115200) #set port and baud rate
# reset the buffers of the UART port to delete the remaining data in the buffers



# s.reset_output_buffer()
# s.reset_input_buffer()

test = Start +Fn_set + struct.pack("B",2)+ struct.pack("B",88) +struct.pack("B",88) +struct.pack("B",88) +struct.pack("B",88) +struct.pack("B",88) +struct.pack("B",88) +struct.pack("B",88) 
with serial.Serial("COM7", 115200) as pacemaker:
      pacemaker.write(test)
      pacemaker.close()

print("Sucesss")




    




       

    
