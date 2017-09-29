import os
import glob
import time
import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

buffsize = 0


base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def timeStamp():
	return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H.%M.%S')

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def loop(file):
	while True:
		deg_c, deg_f = read_temp()
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

