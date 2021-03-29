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

from debug_print import Debug

class Generic_Packet:
    packet_types = {}
    
    @staticmethod
    def from_string(string):
        char = string[0]
        Debug.print("control char: "+str(char))
        if char not in Generic_Packet.packet_types:
            raise RuntimeError("Invalid packet identifier: "+str(char))

        return Generic_Packet.packet_types[char].from_string(string)


class Connect_Packet(Generic_Packet):
    @staticmethod
    def get_packet_header():
        return 'C'
    
    @staticmethod
    def from_string(string):
        if string[0] is not Connect_Packet.get_packet_header():
            raise RuntimeError("Invalid string for packet Connect_Packet!")
        return Connect_Packet()

    def to_string(self):
        return Connect_Packet.get_packet_header()



class Disconnect_Packet(Generic_Packet):
    @staticmethod
    def get_packet_header():
        return 'D'
    
    @staticmethod
    def from_string(string):
        if string[0] is not Disconnect_Packet.get_packet_header():
            raise RuntimeError("Invalid string for packet Disconnect_Packet!")
        return Disconnect_Packet()

    def to_string(self):
        return Disconnect_Packet.get_packet_header()



class Version_Packet(Generic_Packet):
    @staticmethod
    def get_packet_header():
        return 'V'
    
    @staticmethod
    def from_string(string):
        if string[0] is not Version_Packet.get_packet_header():
            raise RuntimeError("Invalid string for packet Version_Packet!")
        version_string = string[1]+"."+string[2]+"."+string[3]+"("+string[4]+string[5]+"/20"+string[6]+string[7]+")"
        return Version_Packet(version_string)

    def __init__(self, version_string):
        self.version_string = version_string

    def to_string(self):
        return Version_Packet.get_packet_header()

    def get_version_string(self):
        return self.version_string

class Keepalive_Request_Packet(Generic_Packet):
    @staticmethod
    def get_packet_header():
        return 'W'
    
    @staticmethod
    def from_string(string):
        if string[0] is not Keepalive_Request_Packet.get_packet_header():
            raise RuntimeError("Invalid string for packet Keepalive_Request_Packet!")
        return Keepalive_Request_Packet()

    def to_string(self):
        return Keepalive_Request_Packet.get_packet_header()

class Keepalive_Response_Packet(Generic_Packet):
    @staticmethod
    def get_packet_header():
        return 'K'
    
    @staticmethod
    def from_string(string):
        if string[0] is not Keepalive_Response_Packet.get_packet_header():
            raise RuntimeError("Invalid string for packet Keepalive_Response_Packet!")
        return Keepalive_Response_Packet()

    def to_string(self):
        return Keepalive_Response_Packet.get_packet_header()

class Level_Packet(Generic_Packet):
    @staticmethod
    def get_packet_header():
        return 'L'
    
    @staticmethod
    def from_string(string):
        if string[0] is not Level_Packet.get_packet_header():
            raise RuntimeError("Invalid string for packet Level_Packet!")
        if len(string) > 1:
            return Level_Packet(string[1])
        else:
            return Level_Packet()

    def __init__(self, level = None):
        self.level = level

    def to_string(self):
        if self.level is None:
            return Level_Packet.get_packet_header()
        else:
            return Level_Packet.get_packet_header() + str(self.level)

class Reset_Packet(Generic_Packet):
    @staticmethod
    def get_packet_header():
        return 'R'
    
    @staticmethod
    def from_string(string):
        if string[0] is not Reset_Packet.get_packet_header():
            raise RuntimeError("Invalid string for packet Reset_Packet!")
        return Reset_Packet()

    def to_string(self):
        return Reset_Packet.get_packet_header()

class Test_Packet(Generic_Packet):
    @staticmethod
    def get_packet_header():
        return 'T'
    
    @staticmethod
    def from_string(string):
        if string[0] is not Test_Packet.get_packet_header():
            raise RuntimeError("Invalid string for packet Test_Packet!")
        return Test_Packet()

    def to_string(self):
        return Test_Packet.get_packet_header()

class Heartrate_Packet(Generic_Packet):
    @staticmethod
    def get_packet_header():
        return 'H'
    
    @staticmethod
    def from_string(string):
        if string[0] is not Heartrate_Packet.get_packet_header():
            raise RuntimeError("Invalid string for packet Heartrate_Packet!")
        if len(string) > 1:
            return Heartrate_Packet(int(string[1:]))
        else:
            return Heartrate_Packet()

    def __init__(self, rate = None):
        self.rate = rate

    def to_string(self):
        if self.rate is None:
            return Heartrate_Packet.get_packet_header()
        else:
            return Heartrate_Packet.get_packet_header() + str(self.rate)
    
class Stroke_Packet(Generic_Packet):
    @staticmethod
    def get_packet_header():
        return 'A'
    
    @staticmethod
    def from_string(string):
        if string[0] is not Stroke_Packet.get_packet_header():
            raise RuntimeError("Invalid string for packet Heartrate_Packet!")
        if len(string) > 26:
            time = int(string[2]) * 3600
            time += int(string[3:5]) * 60
            time += int(string[5:7])

            distance = int(string[7:12])

            speed = int(string[13:15]) * 60 + int(string[15:17])

            spm = int(string[17:20])

            power = int(string[20:23])

            cals = int(string[23:27])
            return Stroke_Packet(time, distance, speed, spm, power, cals)
        else:
            raise RuntimeError("Stroke packet too short!")

    def __init__(self, time, distance, speed, spm, power, cals):
        self.time = time
        self.distance = distance
        self.speed = speed
        self.spm = spm
        self.power = power
        self.cals = cals

    def to_string(self):
        return Stroke_Packet.get_packet_header()
 

Generic_Packet.packet_types = {
        Connect_Packet.get_packet_header(): Connect_Packet,
        Disconnect_Packet.get_packet_header(): Disconnect_Packet,
        Version_Packet.get_packet_header(): Version_Packet,
        Keepalive_Request_Packet.get_packet_header(): Keepalive_Request_Packet,
        Keepalive_Response_Packet.get_packet_header(): Keepalive_Response_Packet,
        Reset_Packet.get_packet_header(): Reset_Packet,
        Level_Packet.get_packet_header(): Level_Packet,
        Heartrate_Packet.get_packet_header(): Heartrate_Packet,
        Stroke_Packet.get_packet_header(): Stroke_Packet
}



