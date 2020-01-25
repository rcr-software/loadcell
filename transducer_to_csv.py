


#!/bin/python

import time
import json
import os

import pandas

from Phidget22.Devices import VoltageRatioInput

voltages = []
times = []
weights = []

start = time.time()

zero = 0.0063237287
bar = 0.006645199843 - zero
psi = 90.0
psi_per_volt = psi / bar

def load_callibration(filename):
    " sets globales zero and psi_per_volt"
    global zero, psi_per_volt
    if not os.path.exists(filename):
        print(f'Callibration file {filename} not found!!!')
        print('[WARNING] using default values for ccalibration.')

    c = json.load(open(filename))
    zero = c['zero']
    psi_per_volt = c['psi'] / (c['bar'] - zero)



def voltage_to_psi(voltage):
    return (voltage - zero) * psi_per_volt

times_called = 0 # incremented, used for occasional printing
def change_handler(self, voltage):
    global times_called
    times.append(time.time() - start)
    voltages.append(voltage)
    weight = voltage_to_psi(voltage)
    weights.append(weight)

    if times_called % 100 == 0:
        #print('measured voltage: ', voltage)
        print('measured psi: ', weight)

    if times_called % 800 == 0:
        print('[WARNING] saving intermediate csv')
        save_to_csv('ducer_intermediate')
    times_called += 1

    

def connect_to_device():
    # Connect to device. Make sure anything else reading it is closed.
    ch = VoltageRatioInput.VoltageRatioInput()
    ch.close()
    ch.setDeviceSerialNumber(533042)
    ch.setChannel(1)

    ch.open() # not sure if needed
    ch.openWaitForAttachment(800)
    time.sleep(1.5)

    print("trying to read voltage ratio:")
    print(ch.getVoltageRatio())
    print("setting data interval to 8ms")
    ch.setDataInterval(8)

    return ch

def save_to_csv(name):
    if not os.path.exists('csv/'):
        os.mkdir('csv')

    data = {'pressure (psi)': weights, 'voltages': voltages}
    df = pandas.DataFrame(data, times)
    timestamp = int(time.time())
    filename = f'csv/{name}_{timestamp}.csv'
    df.to_csv(filename, index_label="time (secs)")

def main():


    print('saving to: ', os.getcwd())

    # TODO should we callibrate??
    # yes.
    load_callibration('callibrate_pressure.json')

    # create ch stuff
    ch = connect_to_device()
    ch.setOnVoltageRatioChangeHandler(change_handler)





if __name__ == '__main__':
    main()

    # wait for user to end it
    input("press enter when finished")
    print("have a nice day :)")

    # tear down ch stuff
    ch.close()
    ch.setOnVoltageRatioChangeHandler(None)

    # save final csv
    # must be after tear down, otherwise might different lengths
    save_to_csv('ducer_final')


