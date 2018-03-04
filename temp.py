import os
import glob
import time
import datetime
import numpy

# OS Calls to open the temperature probe
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

buffsize = 0

# Base Directory of the temperature probe
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Function to return current time stamp UTC
def timeStamp():
	return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H.%M.%S')

# Function to read raw temperature
def read_temp_raw():
	# open the device to be read
    f = open(device_file, 'r')
    lines = f.readlines()
	# close the device
    f.close()
    return lines

# function to strip the temperature
def read_temp():
	# call raw temp function
    lines = read_temp_raw()
	# loop over the line to get the temp
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
	# convert the temperature if the temperature is valid
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

# Loop to call read temp and create a rolling average
def loop(file):
	tempArray = []
	while True:
		deg_c, deg_f = read_temp()
		tempArray.append(deg_f)
		if len(tempArray) > 60:
			tempArray.pop(0)
			rollingAvg = numpy.sum(tempArray)/len(tempArray)
			print rollingAvg, len(tempArray)
		file.write(repr(timeStamp()) + ' ')
		file.write(repr(deg_c) + ' C, ')
		file.write(repr(deg_f) + ' F\n')
		print timeStamp(), deg_f
		time.sleep(1)

def destroy():
	file.close()

if __name__ == '__main__':     # Program start from here
	try:
		file = open(timeStamp() + "TempRecord.txt", "w", buffsize)
		loop(file)
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

