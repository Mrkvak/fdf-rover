#!/usr/bin/env python3

# This file is part of the fdf-rower package (https://github.com/Mrkvak/fdf-rower).
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



import datetime

import sys
import getopt

from rower_io import *
from rower_packet import *
from debug_print import Debug

class Keepalive_Responder:
    def __init__(self, io):
        self.io = io

    def enable(self):
        self.io.reader.add_listener(self)

    def incoming_packet(self, packet):
        if isinstance(packet, Keepalive_Request_Packet):
            io.write_packet_async(Keepalive_Response_Packet())

class CSV_Logger:
    def __init__(self, io):
        self.last_heart_rate = -1
        self.last_level = -1
        self.total_cals = 0
        self.io = io

    def enable(self):
        self.io.reader.add_listener(self)
        self.io.write_packet_sync(Level_Packet())
        self.io.write_packet_sync(Heartrate_Packet())
        print("\"time\", \"elapsed time\", \"level\", \"heartrate\", \"speed\", \"spm\", \"power\", \"distance\", \"cals\"")


    def incoming_packet(self, packet):
        if isinstance(packet, Heartrate_Packet):
            self.last_heart_rate = packet.rate
        if isinstance(packet, Level_Packet):
            self.last_level = packet.level
        if isinstance(packet, Stroke_Packet):
            if packet.spm > 0:
                self.total_cals += packet.cals / (60 * packet.spm)
            print("\"" + str(datetime.datetime.now()) + "\", "
                + str(packet.time) + ", "
                + str(self.last_level) + ", "
                + str(self.last_heart_rate) + ", "
                + str(packet.speed) + ", "
                + str(packet.spm) + ", "
                + str(packet.power) + ", "
                + str(packet.distance) + ", "
                + str(self.total_cals), flush=True)



def print_help():
    print("Usage: "+sys.argv[0]+" -s [/dev/ttyUSBn | COMx] [-d]" )
    print("\t-d print debug messages to stderr")


def main():
    argv = sys.argv[1:]
    port = None
    try:
        opts, args = getopt.getopt(argv, "s:hd")

    except:
        print("Getopt error!")

    for opt, arg in opts:
        if opt in ['-s']:
            port = arg
        if opt in ['-h']:
            print_help()
            return
        if opt in ['-d']:
            Debug.enabled = 1

    if port is None:
        print_help()
        return
    

    io = Rover_IO(port)
    io.start()

    ka = Keepalive_Responder(io)
    ka.enable()

    csv_logger = CSV_Logger(io)
    csv_logger.enable()


if __name__ == '__main__':
    main()
