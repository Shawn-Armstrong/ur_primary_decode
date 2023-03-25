import socket
import struct
import datetime
import sys

# Establish connection to controller
HOST = socket.gethostbyname(socket.gethostname())
PORT = 30002

packageHeaderFmt = '>I'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((HOST, PORT))

while True:
    data = s.recv(4096)
    if data:
        # extract packet length and packet type from start of packet
        packlen = struct.unpack(packageHeaderFmt, data[0:4])[0]
        packtype = data[4]

        # extract subpackage length and subpackage type
        subpacklen = struct.unpack(packageHeaderFmt, data[5:9])[0]
        subpacktype = data[9]
        
        if packtype == 16 and subpacklen == 47:
            robot_mode_data_fmt = '>Q'
            robot_timestamp = struct.unpack(robot_mode_data_fmt, data[10:18])
            robot_mode_data_fmt = '>?'
            isRealRobotConnected = struct.unpack(robot_mode_data_fmt, data[18:19])
            isRealRobotEnabled = struct.unpack(robot_mode_data_fmt, data[19:20])
            isRobotPowerOn = struct.unpack(robot_mode_data_fmt, data[20:21])
            isEmergencyStopped = struct.unpack(robot_mode_data_fmt, data[21:22])
            isProtectiveStopped = struct.unpack(robot_mode_data_fmt, data[22:23])
            isProgramRunning = struct.unpack(robot_mode_data_fmt, data[23:24])
            isProgramPaused = struct.unpack(robot_mode_data_fmt, data[24:25])

            print(f"isRobotPowerOn: {isRobotPowerOn}")
        