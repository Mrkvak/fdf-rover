fdf-rower
==========
This is a python implementation of communication protocol used for First Degree Fitness indoor water rowers. It should work for both Linux and Windows, however Windows are currently untested. Feel free to report bugs.

Supported devices
---------------
* Pacific plus (untested heart rate reporting)
* All other FDF roving machines with USB interface should work, but are untested

Dependencies
---------------
* python 3
* pyserial

Installation and usage
---------------
1. install dependencies
2. checkout the directory
3. connect the rower
4. find the device port of the roving machine (likely `/dev/ttyUSB0`, `COM3` on Windows)
5. check if you have appropriate read/write permissions for the serial port
6. run `rower.py -d serial_port_from_step_4`
7. it will output data in CSV format to standard out. To redirect to file, use: `rower.py -d serial_port_from_step_4 > file.csv`

Example and data processing
---------------


License
---------------
GPLv3. See LICENSE.md

