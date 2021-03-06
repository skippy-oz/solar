#!/usr/bin/env python3

# pvoutput.py
#
# Simple library for uploading data to PVOutput.

import urllib.request
import urllib.parse
import urllib.error
import logging
import sys

logger = logging.getLogger(__name__)

class System:
    """Provides methods for direct uploading to PVOutput for set system."""
    
    def __init__(self, api_key, system_id):
        self.api_key = api_key
        self.system_id = system_id
    
    def add_output(self, data):
        """Add end of day output information. Data should be a dictionary with
        parameters as described here:
        http://pvoutput.org/help.html#api-addoutput ."""
        url = "http://pvoutput.org/service/r2/addoutput.jsp"
        self.__make_request(url, data)
    
    def add_status(self, data):
        """Add live output data. Data should contain the parameters as described
        here: http://pvoutput.org/help.html#api-addstatus ."""
        url = "http://pvoutput.org/service/r2/addstatus.jsp"
        self.__make_request(url, data)
    
    # Could add methods like 'get_status'

    def __make_request(self, url, data):
        logger.debug('Making request: %s, %s', url, data)
        data = urllib.parse.urlencode(data).encode('ascii')
        req = urllib.request.Request(url, data)
        req.add_header('X-Pvoutput-Apikey', self.api_key)
        req.add_header('X-Pvoutput-SystemId', self.system_id)
        try:
            f = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            logger.error('Upload failed: %s', e.read().decode())
        except urllib.error.URLError as e:
            logger.error('Upload failed: %s', e)
        else:
            with f:
                logger.debug('Response: %s', f.read().decode())

    def __str__(self):
        return self.system_id.__str__()

    def __repr__(self):
        return self.system_id.__repr__()

    def __hash__(self):
        return self.system_id.__hash__()

    def __eq__(self, other):
        return self.system_id == other.system_id


# Test code
if __name__ == '__main__':
    import time
    import configparser
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    data = {
        'd': time.strftime('%Y%m%d'),
        't': time.strftime('%H:%M'),
        'v1': 0, # Energy today
        'v2': 0, # Output power
        'v5': 20.0, # Temperature
        'v6': 230.0 # Grid voltage
    }
    config = configparser.ConfigParser()
    config.read_file(open('samil_upload.ini'))
    # Assumes a default API key and system ID
    api_key = config['DEFAULT']['API key']
    system_id = config['DEFAULT']['System ID']
    pv = System(api_key, system_id)
    pv.add_status(data)
