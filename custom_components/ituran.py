
import homeassistant.loader as loader
from requests import get
import xmltodict
import json
import logging
import datetime
import time

import voluptuous as vol

from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.core import callback


_LOGGER = logging.getLogger(__name__)

DOMAIN = 'ituran'
ENTITY_ID_FORMAT = DOMAIN + '.{}'
ITURAN_API_FORMAT = 'https://www.ituran.com/ituranmobileservice/mobileservice.asmx/GetUserPlatforms?UserName={}&GetAddress=True&Password={}'
STATIC_MAP_FORMAT = 'https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom=13&size=500x500&maptype=roadmap&markers=color:blue%7Clabel:P%7C{},{}'
GOOGLE_MAP_FORMAT = "https://www.google.com/maps/search/?api=1&query={},{}"
GOOGLE_MAP_EMBEDDED_FORMAT = "https://maps.google.com/maps?q={},{}&ie=UTF8&t=&z=17&iwloc=B&output=embed"

REQUIREMENTS = ['xml2dict==0.2.2']

def setup(hass, config):

    component = EntityComponent(_LOGGER, DOMAIN, hass)
    
    entities = []
    
    for ent_id, conf in config[DOMAIN].items():
        if not config:
            config = {}
            
        name = conf.get('name', '')
        username = conf.get('username', '')
        password = conf.get('password', '')
        update_interval = conf.get('update_interval', 120)
        
        entities.append(Ituran(name, username, password, ent_id, update_interval))
        
    component.add_entities(entities)
    
    return True
  
 
class Ituran(Entity):
    def __init__(self, name, user, password, ent_id, update_interval):
        self.entity_id = ENTITY_ID_FORMAT.format(ent_id.replace('-', '').replace(' ', '_').replace('.', '_'))
        self._name = name
        self._user = user
        self._pass = password
        self._lat = 0
        self._lon = 0
        self._address = 'loading...'
        self._plate = '0000000'
        self._map = STATIC_MAP_FORMAT.format(self._lat, self._lon, self._lat, self._lon)
        self._milage = '0'
        self._update_interval = update_interval
        self._updated_at = 0.0

        
    @property
    def should_poll(self):
        return True

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._address
        
    def update(self):
        if self._updated_at + self._update_interval > time.mktime(time.gmtime()):
            return
        self._updated_at = time.mktime(time.gmtime())
        url = ITURAN_API_FORMAT.format(self._user, self._pass)
        response = get(url)
        dic = xmltodict.parse(response.text, process_namespaces=False)
        car = dic['ServiceListPlatformsDetails']['VehList']['Veh']

        self._lat = car['Lat']
        self._lon = car['Lon']
        self._address = car['Address']
        self._plate = car['Plate']
        self._map = STATIC_MAP_FORMAT.format(self._lat, self._lon, self._lat, self._lon)
        self._milage = car['LastMileage']
        
    @property    
    def state_attributes(self):
        return {
            "name" : self._name,
            "lat":self._lat,
            "lon":self._lon,
            "address":self._address,
            "map_still" : self._map,
            "plate": self._plate,
            "google_map" : GOOGLE_MAP_FORMAT.format(self._lat, self._lon),
            "google_embedded" : GOOGLE_MAP_EMBEDDED_FORMAT.format(self._lat, self._lon),
            "custom_ui_state_card" : "state-card-ituran",
            "milage" : self._milage,
            "update_interval" : self._update_interval
        }
        
