# Xbee API Mode Programming and a Sound Detection Application  

### Undergraduate  thesis in Finland, 2015  

This project is about using Xbee API mode to transmit sound detection data in a wireless sensor network. In such a sound detection wireless sensor network, we use Raspberry Pi as a sink node, and a group of Arduino Mega 2560 as sensor nodes. The wireless communication was achieved by Xbee RF modules working in API mode.  
This system has a basic function run as a sound level meter. The sensor node can measure sound level in RMS (Root Mean Square) value and turn on a LED if the RMS value is over a threshold. Then the sensor nodes will send these RMS values to a sink node. The sink node display RMS value with its sensor ID, frame ID and timestamp. All these data will be recorded to log files for further use. 

![alt tag](https://github.com/xufein/sound-detection/blob/master/System%20Structure.jpg)
