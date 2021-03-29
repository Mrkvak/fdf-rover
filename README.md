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
You can process your data as you wish (import to openoffice, libreoffice, excel, R). I've provided a simple gnuplot script, that will generate sample images. 
Usage:
`gnuplot -e "filename='file.csv'" gencharts.plt`
It will create several .png files (starting with `file-`).

Example images (together with source .csv file) are provided:
![Example chart - speed and SPM](/example/rower-2021-03-29.csv-speed-spm.png)
![Example chart - SPM and power](/example/rower-2021-03-29.csv-spm-power.png)
![Example chart - distance and kcals](/example/rower-2021-03-29.csv-distance-cals.png)
![Example chart - spm and heartrate](/example/rower-2021-03-29.csv-spm-heartrate.png)




License
---------------
GPLv3. See LICENSE.md

