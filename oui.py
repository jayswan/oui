import json
from sys import argv
import requests

OUTFILE = 'oui_names.txt'
LOOKUP_FILE = 'oui_names.txt'
OUI_URL = 'http://standards.ieee.org/develop/regauth/oui/oui.txt'
REPLACE_CHARS = ['.',':']

def refresh_lookups(url=OUI_URL,outfile=OUTFILE):
    """ refresh the JSON OUI lookup file """
    print 'Trying to refresh OUI lookup file; this may take some time...'
    d = {}
    u = requests.get(url)
    lines = u.text.split('\n')
    for line in lines:
        if 'base' in line:
            fields = line.split()
            d[fields[0]] = ' '.join(fields[3:])
    with open(outfile, 'w') as f:
        json.dump(d,f)

def load_lookup_file(fn):
    """ load the JSON OUI lookup file as a dict """
    oui_table = {}
    try:
        with open(fn) as f:
            oui_table = json.load(f)
        return oui_table
    except:
        # something's wrong with the lookup file, or it's missing
        refresh_lookups()
        with open(fn) as f:
            oui_table = json.load(f)
        return oui_table

def get_oui(mac):
    """ normalize MAC and look up an OUI code """
    mac = mac.upper()
    for c in REPLACE_CHARS:
        mac = mac.replace(c,'')
    mac = mac[:6]
    try:
        return oui_table[mac]
    except KeyError:
        print mac
        return 'unknown OUI'

oui_table = load_lookup_file(LOOKUP_FILE)

def main():
    macs = argv[1:]
    for mac in macs:
        print get_oui(mac)

if __name__ == "__main__":
    main()
