# This file is part of the fdf-rover package (https://github.com/Mrkvak/fdf-rover).
# Copyright (c) 2021 Radek Pilar.
# 
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#


import serial
import rover_packet
import threading
import time

from rover_packet import Connect_Packet,Generic_Packet

from debug_print import Debug

class Rover_IO:
    def __init__(self, port_name):
        self.port = serial.Serial(port_name, 9600, parity = serial.PARITY_NONE, stopbits = 1, timeout = 5)
        self.reader = Port_Reader(self.port)
        self.received_packet = None
        Debug.print("Opened port: "+port_name)

    def start(self):
        self.reader.start()
        self.write_packet_async(Connect_Packet())
        Debug.print("IO started")

    def close(self):
        self.reader.stop()
        self.port = None

    def write_packet_async(self, packet):
        if self.port is None:
            raise RuntimeError("Serial port is not initialized!")
        self.port.write(str.encode(packet.to_string()))
        self.port.write(b'\r\n')

    def write_packet_sync(self, packet, timeout = 5):
        self.reader.add_listener(self)
        self.write_packet_async(packet)
        waiting_step = 0.1
        while self.received_packet is not None and timeout > 0:
            time.sleep(waiting_step)
            timeout -= waiting_step

        self.reader.remove_listener(self)

        return self.received_packet

    def incoming_packet(self, packet):
        self.received_packet = packet


class Port_Reader(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.stop = False
        self.listeners = []
    
    def stop(self):
        self.stop = True

    def add_listener(self, listener):
        self.listeners.append(listener)

    def remove_listener(self, listener):
        self.listeners.remove(listener)

    def notify_listeners(self, packet):
        for listener in self.listeners:
            listener.incoming_packet(packet)

    def run(self):
        while self.stop is not True:
            string = self.port.readline()
            if len(string) > 0:
                string = string.decode()
                Debug.print("Incoming data: "+string)
                self.notify_listeners(Generic_Packet.from_string(string))
                # process packet
            else:
                time.sleep(0.1)


