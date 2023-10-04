# Multiple Connections as TCP Server here: https://www.espressif.com/sites/default/files/documentation/4b-esp8266_at_command_examples_en.pdf

import socket
import os
import sys
import time
import math
import argparse

version = 1.0

# Variables #######################################################################################

tcp_ip = '192.168.4.1' # default IP on ESP8266
tcp_port = 333 # default port on ESP8266

chunkSize = 128
currentChunk = 0
totalChunks = 0
fileSize = 0

###################################################################################################

print("NetLoader version", version)

# Arguments #######################################################################################

cmdparser = argparse.ArgumentParser(description='Send a .uze file to a Uzebox over wifi')
cmdparser.add_argument('-i', '--input', dest='filename', help="file to be sent to Uzebox", required=True)
cmdparser.add_argument('-v', '--verbose', action='store_true', help="enable verbose output while sending a file")
cmdparser.add_argument('-f', '--force', action='store_true', help="force the file to be sent, even if it isn't a valid .uze file")
args = cmdparser.parse_args()

###################################################################################################

fileName = args.filename

f = open(fileName,'rb')

# check if the file is a valid .uze file
# if the "UZEBOX" marker isn't there, then the file is either corrupted or not a valid .uze file
fileHeader = f.read(6)
if fileHeader != b'UZEBOX' and not args.force:
    print("The specified file doesn't appear to be a valid .uze file. Use --force to send it anyways.")
    f.close()
    sys.exit()

# read game name from the .uze header
f.seek(14) # set file pointer to the beginning of the game name
gameName = f.read(31)
gameName = gameName.decode()
f.seek(0) # reset back to the beginning of the file

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect((tcp_ip, tcp_port))
#s.settimeout(None)

fileSize = os.path.getsize(fileName)

totalChunks = math.ceil(fileSize/chunkSize) # round up to nearest int

print("Sending", gameName)

if args.verbose: print("File size:", fileSize, "bytes")
if args.verbose: print("Chunks:", totalChunks)

if args.verbose: print("Sending size data")
s.send(str(totalChunks).encode())

if args.verbose: print("Waiting for reply")
response = s.recv(int(math.log10(totalChunks))+1) # get number of digits in totalChunks variable
if response.decode() != str(totalChunks):
    print("Error\nData mismatch\nExpected:", totalChunks, "\nUzebox replied:", response.decode())
    s.close()
    f.close()
    sys.exit()

if args.verbose: print("") # new line

time.sleep(0.150)

###################################################################################################

while (currentChunk < totalChunks):
    if args.verbose: print("Sending chunk", currentChunk, "of", totalChunks)
    l = f.read(chunkSize)

    if args.verbose: print(l)

    s.send(l)

    if args.verbose: print("Waiting for reply")
    response = s.recv(chunkSize)
    if response != l:
        print("Error\nData mismatch\nExpected:", l, "\nUzebox replied:", response)
        s.close()
        f.close()
        sys.exit()
        
    currentChunk += 1

    if args.verbose: print("") # new line

s.send(b'DONE')
response = s.recv(4)
if response != b'DONE':
    print("Error\nUzebox didn't reply to DONE signal\nUzebox replied", response)
    s.close()
    f.close()
    sys.exit()
print("Done!")
s.close()
f.close()
sys.exit()