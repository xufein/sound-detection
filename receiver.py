#XBee
import serial
ser = serial.Serial('/dev/ttyUSB0',57600)

#IEEE754 to float
import binascii
import struct

#packet loss
#node2
idflag2 = 0
startid2 = 0
currentid2 = 0
nextid2 = 0
loss2 = 0
#node3
idflag3 = 0
startid3 = 0
currentid3 = 0
nextid3 = 0
loss3 = 0

#time
from time import strftime

#file
import csv
c = csv.writer(open("record.csv", "a"))
l = csv.writer(open("logfile.csv", "a"))

#first string
while True:
	#receiver
	receive = ser.readline()
	hex = receive.encode("hex")
	#print hex
	
	#track
	start = '7e002a81'
	check =  hex.find(start,1)
	#print check
	
	if check == 2:
		string1 = hex[0:check]
		string2 = hex[check:len(hex)]
		buffer = string2
		loss2 = 1
		loss3 = 1
		break

while True:
	#receiver
	receive = ser.readline()
	hex = receive.encode("hex")
	#print hex
	
	#track
	start = '7e002a81'
	check =  hex.find(start,1)
	#print check		
			
	if check ==2:
		string1 = hex[0:check]
		string2 = hex[check:len(hex)]
		buffer = buffer + string1
 		#print 'Received: ' + buffer
		sensor = buffer[8:12]	
		idstring = buffer[22:24] + buffer[20:22] + buffer[18:20] + buffer[16:18]
		id = int(idstring,16)
		RMS1 = struct.unpack('<f', binascii.unhexlify(buffer[24:32]))
		RMS1value = str(RMS1)[1:len(str(RMS1))-2]
		RMS2 = struct.unpack('<f', binascii.unhexlify(buffer[32:40]))
		RMS2value = str(RMS2)[1:len(str(RMS2))-2]
		RMS3 = struct.unpack('<f', binascii.unhexlify(buffer[40:48]))
		RMS3value = str(RMS3)[1:len(str(RMS3))-2]
		RMS4 = struct.unpack('<f', binascii.unhexlify(buffer[48:56]))
		RMS4value = str(RMS4)[1:len(str(RMS4))-2]
		RMS5 = struct.unpack('<f', binascii.unhexlify(buffer[56:64]))
		RMS5value = str(RMS5)[1:len(str(RMS5))-2]
		RMS6 = struct.unpack('<f', binascii.unhexlify(buffer[64:72]))
		RMS6value = str(RMS6)[1:len(str(RMS6))-2]
		RMS7 = struct.unpack('<f', binascii.unhexlify(buffer[72:80]))
		RMS7value = str(RMS7)[1:len(str(RMS7))-2]
		RMS8 = struct.unpack('<f', binascii.unhexlify(buffer[80:88]))	
		RMS8value = str(RMS8)[1:len(str(RMS8))-2]
		if RMS1value.find('.',1) == 2:
			rms1 = RMS1value[0:6]		
		if RMS1value.find('.',1) == 1:
			rms1 = RMS1value[0:5]			
		if RMS2value.find('.',1) == 2:
			rms2 = RMS2value[0:6]		
		if RMS2value.find('.',1) == 1:
			rms2 = RMS2value[0:5]		
		if RMS3value.find('.',1) == 2:
			rms3 = RMS3value[0:6]		
		if RMS3value.find('.',1) == 1:
			rms3 = RMS3value[0:5]	
		if RMS4value.find('.',1) == 2:
			rms4 = RMS4value[0:6]		
		if RMS4value.find('.',1) == 1:
			rms4 = RMS4value[0:5]	
		if RMS5value.find('.',1) == 2:
			rms5 = RMS5value[0:6]		
		if RMS5value.find('.',1) == 1:
			rms5 = RMS5value[0:5]	
		if RMS6value.find('.',1) == 2:
			rms6 = RMS6value[0:6]		
		if RMS6value.find('.',1) == 1:
			rms6 = RMS6value[0:5]	
		if RMS7value.find('.',1) == 2:
			rms7 = RMS7value[0:6]		
		if RMS7value.find('.',1) == 1:
			rms7 = RMS7value[0:5]	
		if RMS8value.find('.',1) == 2:
			rms8 = RMS8value[0:6]		
		if RMS8value.find('.',1) == 1:
			rms8 = RMS8value[0:5]		
			
		time = strftime("%Y-%m-%d %H:%M:%S")
		print 'Sensor ', sensor	
		print 'Frame ID: ', id
		print time		
		print rms1, rms2, rms3, rms4, rms5, rms6, rms7, rms8	
		if len(buffer) == 92:
			l.writerow([buffer])		
		if len(buffer) == 184:
			l.writerow([buffer[0:92]])	
			l.writerow([buffer[92:184]])	
		c.writerow([sensor, id, time, rms1, rms2, rms3, rms4, rms5, rms6, rms7, rms8])				
		buffer = string2
		
		#packet loss
		#node2
		if sensor == '2222' and idflag2 == 0:
			startid2 = int(id)
			currentid2 = int(id)
			nextid2 = int(currentid2) + 1
			idflag2 = 1
		if sensor == '2222' and idflag2 == 1:
			#print '2 start id: ', startid2
			currentid2 = int(id)
			#print '2 current id: ', currentid2
			if int(currentid2) != int(nextid2):
				loss2 = loss2 + int(currentid2) - int(nextid2)
			print 'Packet loss: ', loss2
			nextid2 = int(currentid2) + 1
			#print '2 next id: ', nextid2
			print ''
		#node3
		if sensor == '3333' and idflag3 == 0:
			startid3 = int(id)
			currentid3 = int(id)
			nextid3 = int(currentid3) + 1
			idflag3 = 1		
		if sensor == '3333' and idflag3 == 1:	
			#print '3 start id: ', startid3
			currentid3= int(id)
			#print '3 current id: ', currentid3
			if int(currentid3) != int(nextid3):
				loss3 = loss3 + int(currentid3) - int(nextid3)
			print 'Packet loss: ', loss3
			nextid3 = int(currentid3) + 1
			#print '3 next id: ', nextid3
			print ''

	if check == -1:
		string3 = hex
		buffer = buffer + string3

	if check != 2 and check != -1:
		string4 = hex[0:check]
		string5 = hex[check:len(hex)]
		buffer = buffer + string4
		#print 'Received: ' + buffer
		sensor = buffer[8:12]				
		idstring = buffer[22:24] + buffer[20:22] + buffer[18:20] + buffer[16:18]
		id = int(idstring,16)
		RMS1 = struct.unpack('<f', binascii.unhexlify(buffer[24:32]))
		RMS1value = str(RMS1)[1:len(str(RMS1))-2]
		RMS2 = struct.unpack('<f', binascii.unhexlify(buffer[32:40]))
		RMS2value = str(RMS2)[1:len(str(RMS2))-2]
		RMS3 = struct.unpack('<f', binascii.unhexlify(buffer[40:48]))
		RMS3value = str(RMS3)[1:len(str(RMS3))-2]
		RMS4 = struct.unpack('<f', binascii.unhexlify(buffer[48:56]))
		RMS4value = str(RMS4)[1:len(str(RMS4))-2]
		RMS5 = struct.unpack('<f', binascii.unhexlify(buffer[56:64]))
		RMS5value = str(RMS5)[1:len(str(RMS5))-2]
		RMS6 = struct.unpack('<f', binascii.unhexlify(buffer[64:72]))
		RMS6value = str(RMS6)[1:len(str(RMS6))-2]
		RMS7 = struct.unpack('<f', binascii.unhexlify(buffer[72:80]))
		RMS7value = str(RMS7)[1:len(str(RMS7))-2]
		RMS8 = struct.unpack('<f', binascii.unhexlify(buffer[80:88]))	
		RMS8value = str(RMS8)[1:len(str(RMS8))-2]
		if RMS1value.find('.',1) == 2:
			rms1 = RMS1value[0:6]		
		if RMS1value.find('.',1) == 1:
			rms1 = RMS1value[0:5]			
		if RMS2value.find('.',1) == 2:
			rms2 = RMS2value[0:6]		
		if RMS2value.find('.',1) == 1:
			rms2 = RMS2value[0:5]		
		if RMS3value.find('.',1) == 2:
			rms3 = RMS3value[0:6]		
		if RMS3value.find('.',1) == 1:
			rms3 = RMS3value[0:5]	
		if RMS4value.find('.',1) == 2:
			rms4 = RMS4value[0:6]		
		if RMS4value.find('.',1) == 1:
			rms4 = RMS4value[0:5]	
		if RMS5value.find('.',1) == 2:
			rms5 = RMS5value[0:6]		
		if RMS5value.find('.',1) == 1:
			rms5 = RMS5value[0:5]	
		if RMS6value.find('.',1) == 2:
			rms6 = RMS6value[0:6]		
		if RMS6value.find('.',1) == 1:
			rms6 = RMS6value[0:5]	
		if RMS7value.find('.',1) == 2:
			rms7 = RMS7value[0:6]		
		if RMS7value.find('.',1) == 1:
			rms7 = RMS7value[0:5]	
		if RMS8value.find('.',1) == 2:
			rms8 = RMS8value[0:6]		
		if RMS8value.find('.',1) == 1:
			rms8 = RMS8value[0:5]		
			
		time = strftime("%Y-%m-%d %H:%M:%S")
		print 'Sensor ', sensor	
		print 'Frame ID: ', id
		print time		
		print rms1, rms2, rms3, rms4, rms5, rms6, rms7, rms8	
		if len(buffer) == 92:
			l.writerow([buffer])		
		if len(buffer) == 184:
			l.writerow([buffer[0:92]])	
			l.writerow([buffer[92:184]])	
		c.writerow([sensor, id, time, rms1, rms2, rms3, rms4, rms5, rms6, rms7, rms8])		
		buffer = string5

		#packet loss
		#node2
		if sensor == '2222' and idflag2 == 0:
			startid2 = int(id)
			currentid2 = int(id)
			nextid2 = int(currentid2) + 1
			idflag2 = 1
		if sensor == '2222' and idflag2 == 1:
			#print '2 start id: ', startid2
			currentid2 = int(id)
			#print '2 current id: ', currentid2
			if int(currentid2) != int(nextid2):
				loss2 = loss2 + int(currentid2) - int(nextid2)
			print 'Packet loss: ', loss2
			nextid2 = int(currentid2) + 1
			#print '2 next id: ', nextid2
			print ''
		#node3
		if sensor == '3333' and idflag3 == 0:
			startid3 = int(id)
			currentid3 = int(id)
			nextid3 = int(currentid3) + 1
			idflag3 = 1		
		if sensor == '3333' and idflag3 == 1:	
			#print '3 start id: ', startid3
			currentid3= int(id)
			#print '3 current id: ', currentid3
			if int(currentid3) != int(nextid3):
				loss3 = loss3 + int(currentid3) - int(nextid3)
			print 'Packet loss: ', loss3
			nextid3 = int(currentid3) + 1
			#print '3 next id: ', nextid3
			print ''

