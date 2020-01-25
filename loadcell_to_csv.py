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

# calibration globals
# default values
zero = 1.4574611610000002e-05
bar = 2.318822778000002e-05 - zero
pounds = 9.77
lbs_per_volt = pounds / bar

# TODO
# exit cleanly on ctr-c or whatever
# callibration mode

def load_callibration(filename):
    " sets globales zero and lbs_per_volt"
    global zero, lbs_per_volt
    if not os.path.exists(filename):
        print(f'Callibration file {filename} not found!!!')
        print('[WARNING] using default values for ccalibration.')

    c = json.load(open('callibrate.json'))
    zero = c['zero']
    lbs_per_volt = c['pounds'] / (c['bar'] - zero)


def voltage_to_pounds(voltage):
    return (voltage - zero) * lbs_per_volt

times_called = 0 # incremented, used for occasional printing
def change_handler(self, voltage):
    global times_called
    times.append(time.time() - start)
    voltages.append(voltage)
    weight = voltage_to_pounds(voltage)
    weights.append(weight)

    if times_called % 100 == 0:
        #print('measured voltage: ', voltage)
        print('measured pounds: ', weight)

    if times_called % 800 == 0:
        print('[WARNING] saving intermediate csv')
        save_to_csv('intermediate')
    times_called += 1

    

def connect_to_device():
    # Connect to device. Make sure anything else reading it is closed.
    ch = VoltageRatioInput.VoltageRatioInput()
    ch.close()
    ch.setDeviceSerialNumber(533042)
    ch.setChannel(2)

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

    data = {'weigths (lbs)': weights, 'voltages': voltages}
    df = pandas.DataFrame(data, times)
    timestamp = int(time.time())
    filename = f'csv/{name}_{timestamp}.csv'
    df.to_csv(filename, index_label="time (secs)")
    


def main():
    print('saving to: ', os.getcwd())

    # load callibration data
    load_callibration('callibrate.json')

    # create ch stuff
    ch = connect_to_device()
    ch.setOnVoltageRatioChangeHandler(change_handler)



    return ch


if __name__ == '__main__':
    ch = main()

    # wait for user to end it
    input("press enter when finished")
    print("have a nice day :)")

    # cleanup
    ch.close()
    ch.setOnVoltageRatioChangeHandler(None)

    # save final csv
    # must be after tear down, otherwise might different lengths
    save_to_csv('final')
    

