import json
from hashlib import md5
from collections import namedtuple
from lib.model.smartplugin import SmartPlugin
import datetime
import logging

class Station(SmartPlugin):
    PLUGIN_VERSION='1.5.1.1'
    _name = ""
    _num = 0
    _state = 0
    _item = None

    _run_time = 0
    _run_prog = 0
    _run_act = 0

    def __init__(self, name, num):
        self._name = name
        self._num = num

    @property
    def num(self):
        return self._num
    @property
    def name(self):
        return self._name
    @property
    def state(self):
        return self._state
    @state.setter
    def state(self,value):
        self._state=value
        if self._item is not None :
            self._item(value, 'OpenSprinkler',None, None)
    def state_txt(self):
        return ""

class System():
    _lastrun = None


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


ITEM_TAG = {'station': 'opensprinkler_station', 'lastrun' : 'opensprinkler_lastrun'}
commands = {'change_values': 'cv',
            'json_controller': 'jc',
            'delete_program': 'dp',
            'change_program': 'cp',
            'change_runonce': 'cr',
            'manual_program': 'mp',
            'moveup_program': 'up',
            'json_programs': 'jp',
            'change_options': 'co',
            'json_options': 'jo',
            'change_password': 'sp',
            'json_status': 'js',
            'change_manual': 'cm',
            'change_stations': 'cs',
            'json_stations': 'jn',
            'json_station_special': 'je',
            'json_log': 'jl',
            'delete_log': 'dl',
            'view_scripturl': 'su',
            'change_scripturl': 'cu',
            'json_all': 'ja',
            }

logger = logging.getLogger(__name__)

class OpenSprinkler(SmartPlugin):
    CORE_VERSION = '1.5'
    IMPL_VERSION= "1"
    PLUGIN_VERSION = CORE_VERSION+'.'+IMPL_VERSION
    ALLOW_MULTIINSTANCE = True

    def __init__(self, sh, host, port, username, password, cycle=15):
        self._sh = sh
        self.host = host
        self.port = port
        self.username = username

        self.logger = logging.getLogger(__name__)

        self.passwd = password
        if len(self.passwd) is not 32:
            self.passwd= self.toMD5(self.passwd)

        self.pwparam = 'pw='+self.passwd
        self.url= "http://"+self.host + ':'+str(self.port)+ '/{}?' + self.pwparam
        self._sitems=[]
        self._cycle = cycle
        self.stations = self.buildStations()

        self.system = System()


    def run(self):
        self.alive = True
        self._sh.scheduler.add(self.__class__.__name__, self.update_status, cycle=self._cycle)

    def stop(self):
        self.alive = False

    def parse_logic(self, logic):
        pass

    def update_item(self, item, caller=None, source=None, dest=None):
        if caller is not 'OpenSprinkler':
            name = self.get_iattr_value(item.conf, ITEM_TAG['station'])
            for key in self.stations:
                if self.stations[key].name == name:
                    sid=self.stations[key].num
                    if item._value == True:
                        self.setOn(sid)
                    elif item._value == False:
                        self.setOff(sid)


    def setOn(self, sid, time=60):
        self.fetchCommand(commands['change_manual'],'&sid='+ str(sid) + '&en='+str(1) + '&t='+str(time))
        #self.update_status()
    def setOff(self, sid):
        self.fetchCommand(commands['change_manual'],'&sid='+ str(sid) + '&en='+str(0))
        #self.update_status()

    def stopAll(self):
        self.fetchCommand(commands['change_values'], '&rsn=1')
        #self.update_status()

    def disableSystem(self):
        self.stopAll()
        self.fetchCommand(commands['change_values'], '&en=0')
        #self.update_status()

    def enableSystem(self):
        self.fetchCommand(commands['change_values'], '&en=1')

    def parse_item(self, item):
        # wenn das item opensprinkler_station="name" enthält, dann hänge das an die Station
        if self.has_iattr(item.conf, ITEM_TAG['station']):
            name = self.get_iattr_value(item.conf, ITEM_TAG['station'])
            for key in self.stations:
                if self.stations[key].name  == name:
                    self.stations[key]._item = item
                    item._sprinkler_station = self.stations[key]
                    return self.update_item
        elif self.has_iattr(item.conf, ITEM_TAG['lastrun']):
            self.system._lastrun = item

        return None

    def update_status(self):
        self.readStatus()
        self.readSystemStatus()
        self.printtest()

    def buildStations(self):
        stations = {}
        res = self.fetchCommand(commands['json_stations'])
        for idx, name in enumerate(res.snames):
            station = Station(num=idx,name=name)
            stations[idx]= station
        #print(res)

        return stations

    def printtest(self):
        for key  in self.stations:
            print(self.stations[key].name,self.stations[key].num, self.stations[key].state)

    def readStatus(self):
        res = self.fetchCommand(commands['json_status'])
        for idx, r in enumerate(res.sn):
            #print(idx,': ', r)
            self.stations[idx].state=r
        print(res)

    def readSystemStatus(self):
        res = self.fetchCommand(commands['json_controller'])

        #for idx, r in enumerate(res.sn):
        #    print(idx,': ', r)
            #self.stations[idx].state=r
        print(res)
        print()
        print(res.en)
        print(res.devt)
        print(res.rd)
        print(res.rs)
        print(bit(res.sbits[0],7))
        print(res.ps[7])


        if self.system._lastrun is not None:
            value = ('Station: ' + str(res.lrun[0]) + ' (' + self.stations[res.lrun[0]].name + ')' + ' Prog: ' + str(
                res.lrun[1]) + ' Dauer: ' + str(res.lrun[2]) + ' s, Zeitpunkt: ' + datetime.datetime.fromtimestamp(
                res.lrun[3]).strftime('%Y-%m-%d %H:%M:%S'))
            self.system._lastrun(value, 'OpenSprinkler',None, None)



    def readAllVars(self):
        res = self.fetchCommand(commands['json_all'])
        print(res)

    def fetchCommand(self, command, parameter = ''):
        data = self.fetch(self.url.format(command)+parameter)
        print(data)
        response = json2obj(data)
        return response

    def fetch(self, url):

        src = response = None
        try:
            import urllib.request
            # @TODO: try catch
            response = urllib.request.urlopen(url).read()
        except:
            logger.error("Cannot connect to OpenSprinkler")
        finally:
            if src:
                src.close()


        if response:
            return str(response.decode('utf8'))

    def toMD5(self, string):
        hashfunc = md5()
        hashfunc.update(string.encode())
        return "".join(format(b, "02x") for b in hashfunc.digest())

def bit(num, offset):
    return str(((num >>offset) &1))

