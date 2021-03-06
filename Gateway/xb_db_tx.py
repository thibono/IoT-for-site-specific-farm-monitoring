# Copyright 2017, Digi International Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from digi.xbee.devices import XBeeDevice
import time
import sqlite3

dbname='sensorsData.db'

def logData(nodeID, sampleID,temp, hum,rain):
    conn= sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute("INSERT INTO sensor_data VALUES(datetime('now'), (?), (?), (?), (?), (?))", (nodeID, sampleID,temp, hum,rain))
    conn.commit()
    conn.close()
    
def logStatusData(nodeID, temp, Vbat, Vsol):
    conn= sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute("INSERT INTO node_status VALUES(datetime('now'), (?), (?), (?), (?))", (nodeID, temp, Vbat,Vsol))
    conn.commit()
    conn.close()    
    
# TODO: Replace with the serial port where your local module is connected to. 
PORT = "/dev/ttyUSB0"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600


def main():
    print(" +-----------------------------------------+")
    print(" | XBee Python Library Receive Data Sample |")
    print(" +-----------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)
    device.open()
    device.send_data_broadcast("#k")
    device.send_data_broadcast("#k")
    device.send_data_broadcast("#a")
    device.send_data_broadcast("#b")
    #device.send_data_broadcast("#a")
    device.close()

    try:
        device.open()
        def data_receive_callback(xbee_message):
            print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                     xbee_message.data.decode()))
            dataMsg = xbee_message.data.decode()
            
            print("dataa %s" % dataMsg[0])
            
            payload = dataMsg.split(',')

            node = payload[0]
            
            if (payload[1] == '!'):
                 #data from status message
                intTemp = payload[2]
                Vbat = payload[3]
                Vsol = payload[4]
                logStatusData(node,intTemp,Vbat,Vsol)
                print(dataMsg)
                print(node)
                print(intTemp)
                print(Vbat)
                print(Vsol)
                
                         
            else:
                #data from message
                sampleID = payload[1]
                temp = payload[2]
                rh = payload[3]
                rf = payload[4]
                #call the function to insert data
                logData(node, sampleID,temp, rh,rf)
                
                print(dataMsg)
                print(node)
                print(temp)
                print(rh)
                print(rf)
                   
        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()