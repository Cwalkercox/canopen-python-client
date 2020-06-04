import canopen
import os
import can
import time
import signal
import logging
from random import randint

logging.basicConfig(level=logging.DEBUG)
logger=logging.getLogger(__name__)


#os.system('sudo ip link set can0 up type can bitrate 1000000   dbitrate 8000000 restart-ms 1000 berr-reporting on fd on')
os.system('sudo ip link set can0 up type can bitrate 1000000')
#os.system('sudo ifconfig can0 txqueuelen 65536')
os.system('sudo ifconfig can0 txqueuelen 100000')
can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')# socketcan_native
#
print('Initialized can0')
network = canopen.Network()

network.connect(channel='can0', bustype='socketcan')

local_node = canopen.LocalNode(7, '/home/pi/FOCIS/IOModule/NXP_CiA401.eds')
network.add_node(local_node)

######This tests network scanning functionality. Can use it to fire off a bunch of CAN messages for testing
# network.scanner.search()
# time.sleep(0.05)
# for node_id in network.scanner.nodes:
#     print("Found node %d!" % node_id)
###############End of network scanner



##This is how to write process info to OD
#local_node.object_dictionary[0x1008].value="AI"
local_node.object_dictionary[0x1009].value="Raspi 3" #0x1009 is device name
local_node.object_dictionary[0x1000].value="AI" #0x1000 is device type (AI,AO,DI,DO)
#local_node.object_dictionary[0x6401][1].value=4
#local_node.object_dictionary[0x1017].value=99
#local_node.object_dictionary[0x6000][1].data_type=0x0009 #Makes the data type of that entry a string
local_node.object_dictionary['Read Sensor Data']['HART Primary Value'].value=0
#local_node.object_dictionary[0x6000][1].value="HART1"
local_node.object_dictionary['HART Configuration Data']['HART Device Information'].value="bar"
#local_node.object_dictionary[0x1000].value="AO"
while True:
    try:
        #####uncomment for AI slave
        sensorvalue=randint(10,50)
        local_node.object_dictionary[0x6401][1].value=sensorvalue
        #local_node.object_dictionary['Read Sensor Data']['Analog Input'].value
        
        local_node.object_dictionary[0x6401][2].value=sensorvalue+10
        #local_node.object_dictionary['Read Sensor Data']['HART Primary Value'].value
        
        print(local_node.object_dictionary[0x6401][1].value) #Analog sensor reading
        print(local_node.object_dictionary[0x6401][2].value) #Hart sensor reading
        print(local_node.object_dictionary[0x6000][1].value) #Hart Device Info"
        ######################
        
        #####uncomment for AO slave
        #receivedval=local_node.sdo[0x6401][1].phys #receive SDO value from Master
        #print(receivedval)
        ##########
    except:
        print('Loop exited due to error')
    time.sleep(0.75) #repeat every 0.75 seconds

signal.pause()


network.disconnect()
os.system('sudo ifconfig can0 down')
print('Closed can0')
print('Network disconnected')
