from time import sleep
import serial


device = serial.Serial('/dev/ttyACM0')
sleep(0.2)

values = [0, 1000, 2000, 2500, 3000, 3500, 4000]
currents = []

for value in values:
    output = 'OUT:CH0:{}\n'.format(value)
    device.write(output.encode('ascii'))
    sleep(0.5)
    device.write(b'IN:CH0\n')
    current = device.readline()
    currents.append(current)

device.close()

print(currents)