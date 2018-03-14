"""
Support for JemenaOutlook.

Get data from 'Jemena Energy Outlook - Your Electricity Use' page/s:
https://electricityoutlook.jemena.com.au/electricityView/index

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.jemenaoutlook/
"""
import logging
from datetime import timedelta
import json

import re
from bs4 import BeautifulSoup
import requests
import logging

import http.client as http_client

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_USERNAME, CONF_PASSWORD,
    CONF_NAME, CONF_MONITORED_VARIABLES)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['beautifulsoup4==4.6.0']

http_client.HTTPConnection.debuglevel = 1

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

REQUESTS_TIMEOUT = 15

KILOWATT_HOUR = 'kWh'  # type: str
PRICE = 'AUD'  # type: str
DAYS = 'days'  # type: str
CONF_CONTRACT = 'contract'  # type: str

DEFAULT_NAME = 'JemenaOutlook'

REQUESTS_TIMEOUT = 15
MIN_TIME_BETWEEN_UPDATES = timedelta(hours=24)
SCAN_INTERVAL = timedelta(hours=24)

SENSOR_TYPES = {
    'yesterday_total_usage':
    ['Yesterday total usage', KILOWATT_HOUR, 'mdi:flash'],
    'yesterday_total_consumption':
    ['Yesterday total consumption', KILOWATT_HOUR, 'mdi:flash'],
    'yesterday_total_consumption_peak':
    ['Yesterday total consumption_peak', KILOWATT_HOUR, 'mdi:flash'],
    'yesterday_total_consumption_offpeak':
    ['Yesterday total consumption_offpeak', KILOWATT_HOUR, 'mdi:flash'],
    'yesterday_total_consumption_shoulder':
    ['Yesterday total consumption_shoulder', KILOWATT_HOUR, 'mdi:flash'],
    'yesterday_total_consumption_controlled_load':
    ['Yesterday total consumption_controlled_load', KILOWATT_HOUR, 'mdi:flash'],
    'yesterday_total_generation':
    ['Yesterday total generation', KILOWATT_HOUR, 'mdi:flash'],
    'previous_total_usage':
    ['Yesterday total usage', KILOWATT_HOUR, 'mdi:flash'],
    'previous_total_consumption':
    ['Previous day total consumption', KILOWATT_HOUR, 'mdi:flash'],
    'previous_total_generation':
    ['Previous day total generation', KILOWATT_HOUR, 'mdi:flash'],
    'yesterday_suburb_average':
    ['Yesterday suburb average', KILOWATT_HOUR, 'mdi:flash'],
    'yesterday_cost_total':
    ['Yesterday cost total', PRICE, 'mdi:currency-usd'],
    'yesterday_cost_consumption':
    ['Yesterday cost consumption', PRICE, 'mdi:currency-usd'],
    'yesterday_cost_generation':
    ['Yesterday cost generation', PRICE, 'mdi:currency-usd'],
    'cost_difference':
    ['Cost difference', PRICE, 'mdi:currency-usd'],
    'kwh_percentage_difference':
    ['Kwh percentage difference', KILOWATT_HOUR, 'mdi:percent'],
    'cost_difference_message':
    ['Cost difference message', 'text', 'mdi:currency-usd']
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_MONITORED_VARIABLES):
        vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

HOST = 'https://electricityoutlook.jemena.com.au'
HOME_URL = '{}/login/index'.format(HOST)
PERIOD_URL = ('{}/electricityView/period/'.format(HOST))


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Jemena Outlook sensor."""
    # Create a data fetcher to support all of the configured sensors. Then make
    # the first call to init the data.

    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    try:
        jemenaoutlook_data = JemenaOutlookData(username, password)
        jemenaoutlook_data.get_data()
        
    except requests.exceptions.HTTPError as error:
        _LOGGER.error("Failt login: %s", error)
        return False

    name = config.get(CONF_NAME)

    sensors = []
    for variable in config[CONF_MONITORED_VARIABLES]:
        sensors.append(JemenaOutlookSensor(jemenaoutlook_data, variable, name))

    add_devices(sensors)


class JemenaOutlookSensor(Entity):
    """Implementation of a Jemena Outlook sensor."""

    def __init__(self, jemenaoutlook_data, sensor_type, name):
        """Initialize the sensor."""
        self.client_name = name
        self.type = sensor_type
        self._name = SENSOR_TYPES[sensor_type][0]
        self._unit_of_measurement = SENSOR_TYPES[sensor_type][1]
        self._icon = SENSOR_TYPES[sensor_type][2]
        self.jemenaoutlook_data = jemenaoutlook_data
        self._state = None

        if self.type in self.jemenaoutlook_data.data is not None:
            if type(self.jemenaoutlook_data.data[self.type]) == type(''):
                self._state = self.jemenaoutlook_data.data[self.type]
            else:
                self._state = round(self.jemenaoutlook_data.data[self.type], 2)
                

    @property
    def name(self):
        """Return the name of the sensor."""
        return '{} {}'.format(self.client_name, self._name)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    def update(self):
        """Get the latest data from Jemena Outlook and update the state."""
        self.jemenaoutlook_data.update()

        if self.type in self.jemenaoutlook_data.data is not None:
            if type(self.jemenaoutlook_data.data[self.type]) == type(''):
                self._state = self.jemenaoutlook_data.data[self.type]
            else:
                self._state = round(self.jemenaoutlook_data.data[self.type], 2)


class JemenaOutlookData(object):
    """Get data from JemenaOutlook."""

    def __init__(self, username, password):
        """Initialize the data object."""
        self.client = JemenaOutlookClient(
            username, password, REQUESTS_TIMEOUT)
        self.data = {}

    def _fetch_data(self):
        """Fetch latest data from Jemena Outlook."""
        try:
            self.client.fetch_data()
        except JemenaOutlookError as exp:
            _LOGGER.error("Error on receive last Jemena Outlook data: %s", exp)
            return

    def get_data(self):
        """Return the contract list."""
        # Fetch data
        self._fetch_data()
        return self.client.get_data()

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Return the latest collected data from Jemena Outlook."""
        self._fetch_data()
        self.data = self.client.get_data()


class JemenaOutlookError(Exception):
    pass

class JemenaOutlookClient(object):

    def __init__(self, username, password, timeout=REQUESTS_TIMEOUT):
        """Initialize the client object."""
        self.username = username
        self.password = password
        self._data = {}
        self._timeout = timeout
        self._session = None


    def _get_login_page(self):
        """Go to the login page."""
        try:
            raw_res = self._session.get(HOME_URL, timeout=REQUESTS_TIMEOUT)

        except OSError:
            raise JemenaOutlookError("Can not connect to login page")

        # Get login url
        soup = BeautifulSoup(raw_res.content, 'html.parser')

        form_node = soup.find('form', {'id': 'loginForm'})
        if form_node is None:
            raise JemenaOutlookError("No login form found")

        login_url = form_node.attrs.get('action')
        if login_url is None:
            raise JemenaOutlookError("Cannot find login url")

        return login_url


    def _post_login_page(self, login_url):
        """Login to Jemena Electricity Outlook website."""
        form_data = {"login_email": self.username,
                "login_password": self.password,
                "submit": "Sign In"}
        try:
            raw_res = self._session.post('{}/login_security_check'.format(HOST),
                                    data = form_data,
                                    timeout = REQUESTS_TIMEOUT)

        except OSError as e:
            raise JemenaOutlookError("Cannot submit login form {0}".format(e.errno))
        
        if raw_res.status_code != 200:
            raise JemenaOutlookError("Login error: Bad HTTP status code. {}".format(raw_res.status_code))

        return True

    
    def _get_daily_data(self, days_ago):
        """Get daily data."""

        try:
            raw_res = self._session.get('{}/electricityView/period/day/1'.format(HOST),
                                   timeout = REQUESTS_TIMEOUT)
        except OSError as e:
            _LOGGER.debug("exception data {}".format(e.errstring))
            raise JemenaOutlookError("Cannot get daily data")
        try:
            json_output = raw_res.json()
        except (OSError, json.decoder.JSONDecodeError):
            raise JemenaOutlookError("Could not get daily data: {}".format(raw_res))

        if not json_output.get('selectedPeriod'):
            raise JemenaOutlookError("Could not get daily data for selectedPeriod")

        _LOGGER.debug("Jemena outlook json_output: %s", json_output)

        costDifference = json_output.get('costDifference')
        costDifferenceMessage = json_output.get('costDifferenceMessage')
        kwhPercentageDifference = json_output.get('kwhPercentageDifference')
        
        selectedPeriod = json_output.get('selectedPeriod')        	
        
        peakConsumption = self._sum_period_array(selectedPeriod['consumptionData']['peak'])
        offPeakConsumption = self._sum_period_array(selectedPeriod['consumptionData']['offpeak'])
        shoulderConsumption = self._sum_period_array(selectedPeriod['consumptionData']['shoulder'])
        controlledLoadConsumption = self._sum_period_array(selectedPeriod['consumptionData']['controlledLoad'])
        generation = self._sum_period_array(selectedPeriod['consumptionData']['generation'])
        suburbAverage = self._sum_period_array(selectedPeriod['consumptionData']['suburbAverage'])

        costDataPeak = self._sum_period_array(selectedPeriod['costData']['peak'])
        costDataOffPeak = self._sum_period_array(selectedPeriod['costData']['offpeak'])
        costDataShoulder = self._sum_period_array(selectedPeriod['costData']['shoulder'])
        costDataControlledLoad = self._sum_period_array(selectedPeriod['costData']['controlledLoad'])
        costDataGeneration = self._sum_period_array(selectedPeriod['costData']['generation'])

        previousPeriod = json_output.get('comparisonPeriod')

        previousPeriodPeakConsumption = self._sum_period_array(previousPeriod['consumptionData']['peak'])
        previousPeriodOffPeakConsumption = self._sum_period_array(previousPeriod['consumptionData']['offpeak'])
        previousPeriodShoulderConsumption = self._sum_period_array(previousPeriod['consumptionData']['shoulder'])
        previousPeriodControlledLoadConsumption = self._sum_period_array(previousPeriod['consumptionData']['controlledLoad'])
        previousPeriodGeneration = self._sum_period_array(previousPeriod['consumptionData']['generation'])
        previousPeriodSuburbAverage = self._sum_period_array(previousPeriod['consumptionData']['suburbAverage'])
            
        daily_data = {"yesterday_total_usage": (peakConsumption + offPeakConsumption + shoulderConsumption + controlledLoadConsumption - generation) ,
                      "yesterday_total_consumption": (peakConsumption + offPeakConsumption + shoulderConsumption + controlledLoadConsumption),
                      "yesterday_total_consumption_peak": (peakConsumption),
                      "yesterday_total_consumption_offpeak": (offPeakConsumption),
                      "yesterday_total_consumption_shoulder": (shoulderConsumption),
                      "yesterday_total_consumption_controlled_load": (controlledLoadConsumption),
                      "yesterday_total_generation": generation,
                      "yesterday_cost_total": (costDataPeak + costDataOffPeak + costDataShoulder + costDataControlledLoad + costDataGeneration),
                      "yesterday_cost_consumption": (costDataPeak + costDataOffPeak + costDataShoulder + costDataControlledLoad),
                      "yesterday_cost_generation": abs(costDataGeneration),
                      "yesterday_suburb_average": suburbAverage,
                      "previous_total_usage": (previousPeriodPeakConsumption + previousPeriodOffPeakConsumption + previousPeriodShoulderConsumption + previousPeriodControlledLoadConsumption - previousPeriodGeneration),
                      "previous_total_consumption": (previousPeriodPeakConsumption + previousPeriodOffPeakConsumption + previousPeriodShoulderConsumption + previousPeriodControlledLoadConsumption),
                      "previous_total_generation": previousPeriodGeneration,
                      "cost_difference": costDifference,
                      "kwh_percentage_difference": kwhPercentageDifference,
                      "cost_difference_message": costDifferenceMessage['text']
                     }

        return daily_data

    def _sum_period_array(self, json_array_of_value):
        total_value = 0.0
        for value in json_array_of_value:
            total_value += value
        return total_value


    def fetch_data(self):
        """Get the latest data from Jemena Outlook."""
        
        # setup requests session
        self._session = requests.Session()

        # Get login page
        login_url = self._get_login_page()
        
        # Post login page
        self._post_login_page(login_url)

        # Get Daily Usage data
        self._data = self._get_daily_data(1)


    def get_data(self):
        return self._data
