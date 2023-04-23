"""DWC Network Server Emulator

    Copyright (C) 2014 polaris-
    Copyright (C) 2014 msoucy
    Copyright (C) 2015 Sepalani

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from twisted.web import server, resource
from twisted.internet import reactor
from twisted.internet.error import ReactorAlreadyRunning
from multiprocessing.managers import BaseManager
import time
import datetime
import json
import logging

import other.utils as utils
import dwc_config

logger = dwc_config.get_logger('InternalStatsServer')


class GameSpyServerDatabase(BaseManager):
    pass

GameSpyServerDatabase.register("get_server_list")


class StatsPage(resource.Resource):
    """Servers statistics webpage.

    Format attributes:
     - header
     - row
     - footer
    """
    isLeaf = True
    header = """<html>
    <table border='1'>
        <tr>
            <td>Game ID</td><td># Players</td>
        </tr>"""
    row = """
        <tr>
            <td>%s</td>
            <td><center>%d</center></td>
        </tr>"""  # % (game, len(server_list[game]))
    footer = """</table>
    <br>
    <i>Last updated: %s</i><br>
    </html>"""  # % (self.stats.get_last_update_time())

    def __init__(self, stats):
        self.stats = stats

    def render_GET(self, request):
        uri_bytes = request.uri###
        uri_str = uri_bytes.decode('utf-8')
        request = uri_str###

        #request = [item.decode() if isinstance(item, bytes) else item for item in request]
        #if request[0] == "/json":
        if request.startswith("/json"):
        #if "/".join(request.postpath) == "json":
            raw = True
            force_update = True
        else:
            raw = False
            force_update = False

        server_list = self.stats.get_server_list(force_update)
        
        print(server_list)

        decoded_list = {
            k.decode(): [
                {
                    k2.decode(): v2.decode() if isinstance(v2, bytes) else v2 if isinstance(v2, str) else v2 
                    for k2, v2 in d.items() if not isinstance(k2, str)
                } 
                for v in server_list.values() for d in v
            ]
            for k in server_list.keys()
}

        #decoded_list = {k.decode(): [{k2.decode(): v2.decode() if isinstance(v2, bytes) else v2 if isinstance(v2, str) else v2 for k2, v2 in d.items() if not isinstance(k2, str)}] for v in server_list.values() for d in v]

        #decoded_list = {k.decode(): [{k2.decode() if isinstance(k2, bytes) else k2: v2.decode() if isinstance(v2, bytes) else v2 if isinstance(v2, str) else v2 for k2, v2 in d.items() if not isinstance(k2, str)] for d in v] for k, v in server_list.items()}

        #decoded_list = {k.decode(): [{k2.decode(): v2.decode() if isinstance(v2, bytes) else v2 if isinstance(v2, str) else v2 for k2, v2 in d.items() if not isinstance(k2, str)] for d in v] for k, v in server_list.items()}

        #decoded_list = {k.decode(): [{k2.decode(): v2.decode() if isinstance(v2, bytes) else v2 if isinstance(v2, str) else v2 for k2, v2 in d.items()} for d in v] for k, v in server_list.items()}

#        decoded_list = {
#            k.decode(): [
#                {
#                    k2.decode(): v2.decode() if isinstance(v2, bytes) else v2 if isinstance(v2, str) else v2 
#                    for k2, v2 in d.items()
#                } 
#                for d in v
#            ] 
#            if isinstance(v, list) else 
#            v.decode() if isinstance(v, bytes) else v 
#            for k, v in server_list.items()
#        }

        #decoded_list = {k.decode(): [{k2.decode(): v2.decode() if isinstance(v2, bytes) else v2 if not isinstance(v2, str) else v2 for k2, v2 in d.items()} for d in v] for k, v in server_list.items()}
        #decoded_list = {k.decode(): [{k2.decode(): v2.decode() if isinstance(v2, bytes) else v2 for k2, v2 in d.items()} for d in v] for k, v in server_list.items()}
        print(decoded_list)
        #server_str = str(server_list, 'utf-8') # Convert bytes to string
        #decoded_data = {}
        #for game in json.loads(server_str):
        #    data = json.loads(game)
        #    decoded_data[data['gamename']] = {k: v.decode('utf-8') if isinstance(v, bytes) else v for k, v in data.items()}

        #server_str = {}
        #for game, data in server_list.items():
        #    decoded_data = {k.decode('utf-8'): v.decode('utf-8') if isinstance(v, bytes) else v for k, v in data.items()}
        #    server_str[game.decode('utf-8')] = str(decoded_data)
        #decoded_list = json.loads(server_list.decode('utf-8'))

        #server_str = {}
        #for game, data in decoded_list.items():
        #    decoded_data = {k: v.decode('utf-8') if isinstance(v, bytes) else v for k, v in data.items()}
        #server_str[game] = str(decoded_data)


        #server_list = self.stats.get_server_list(force_update)
        #decoded_list = {k: {k2: v2.decode('utf-8') if isinstance(v2, bytes) else v2 for k2, v2 in v.items()} for k, v in server_list.items()}
        #server_str = {k: str(v) for k, v in decoded_list.items()}


        #decoded_list = json.loads(server_list.decode('utf-8'))
        #decoded_list = {k: {k2: v2.decode('utf-8') if isinstance(v2, bytes) else v2 for k2, v2 in v.items()} for k, v in decoded_list.items()}
        #server_str = {k: str(v) for k, v in decoded_list.items()}


        #decoded_list = {k.decode('utf-8'): {k2.decode('utf-8'): v2.decode('utf-8') if isinstance(v2, bytes) else v2 for k2, v2 in v.items()} for k, v in server_list.items()}
        #server_str = {k: str(v) for k, v in decoded_list.items()}
        #decoded_list = eval(server_list.decode('utf-8'))
        #server_str = {k: str({k2.decode('utf-8'): v2.decode('utf-8') if isinstance(v2, bytes) else v2 for k2, v2 in v.items()}) for k, v in decoded_list.items()}
        #server_str = []
        #for item in server_list:
        #    if isinstance(item, dict):
        #        decoded_item = {k: v.decode('utf-8') if isinstance(v, bytes) else v for k, v in item.items()}
        #        server_str.append(str(decoded_item).replace("b'", "'"))
        #    elif isinstance(item, bytes):
        #        server_str.append(item.decode('utf-8').replace("b'", "'"))
        #    else:
        #        server_str.append(str(item))
        #server_str = [str({k: v.decode('utf-8') if isinstance(v, bytes) else v for k, v in item.items()}).replace("b'", "'") for item in server_list]
        #server_str = []
        #for item in server_list:
        #    if isinstance(item, bytes):
        #        server_str.append(item.decode().replace("b'", "'"))
        #    else:
        #        server_str.append(str({k: v.decode() if isinstance(v, bytes) else v for k, v in item.items()}).replace("b'", "'"))

        #server_str = [str({k: v.decode() if isinstance(v, bytes) else v for k, v in item.items()}).replace("b'", "'") for item in server_list]
        #server_str = [str(item) for item in server_list]
        #server_str = server_list.decode('utf-8')

        server_list = decoded_list
        if raw:
            # List of keys to be removed
            restricted = ["publicip", "__session__", "localip0", "localip1"]

            # Filter out certain fields before displaying raw data
            if server_list is not None:
                for game in server_list:
                    for server in server_list[game]:
                        for r in restricted:
                            if r in server:
                                server.pop(r, None)
            #output = json.dumps(server_list).encode('utf-8')
            output = json.dumps(server_list)

        else:
            output = self.header
            if server_list is not None:
                output += "".join(self.row % (game, len(server_list[game]))
                                  for game in server_list
                                  if server_list[game])
            output += self.footer % (self.stats.get_last_update_time())

        return output.encode('utf-8')


class InternalStatsServer(object):
    """Internal Statistics server.

    Running on port 9001 by default: http://127.0.0.1:9001/
    Can be displayed in json format: http://127.0.0.1:9001/json
    """
    def __init__(self):
        self.last_update = 0
        self.next_update = 0
        self.server_list = None
        # The number of seconds to wait before updating the server list
        self.seconds_per_update = 60

    def start(self):
        manager_address = dwc_config.get_ip_port('GameSpyManager')
        manager_password = ""
        self.server_manager = GameSpyServerDatabase(address=manager_address, 
                                                    authkey=manager_password.encode('utf-8'))

        self.server_manager.connect()

        site = server.Site(StatsPage(self))
        reactor.listenTCP(dwc_config.get_port('InternalStatsServer'), site)

        try:
            if not reactor.running:
                reactor.run(installSignalHandlers=0)
        except ReactorAlreadyRunning:
            pass

    def get_server_list(self, force_update=False):
        if force_update or self.next_update == 0 or \
           self.next_update - time.time() <= 0:
            self.last_update = time.time()
            self.next_update = time.time() + self.seconds_per_update
            self.server_list = self.server_manager.get_server_list() \
                                                  ._getvalue()

            logger.log(logging.DEBUG, "%s", self.server_list)

        return self.server_list

    def get_last_update_time(self):
        return str(datetime.datetime.fromtimestamp(self.last_update))


if __name__ == "__main__":
    stats = InternalStatsServer()
    stats.start()
