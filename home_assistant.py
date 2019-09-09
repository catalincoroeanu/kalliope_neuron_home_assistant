# -*- coding: utf-8 -*-

import logging
import requests, json

from urlparse import urljoin

from kalliope.core.NeuronModule import (NeuronModule,
                                        MissingParameterException,
                                        InvalidParameterException)

logging.basicConfig()
logger = logging.getLogger("kalliope")

class Home_assistant(NeuronModule):

    """
    Class used to interact with home assistant
    """
    def __init__(self, **kwargs):

        super(Home_assistant, self).__init__(**kwargs)

        #https://github.com/home-assistant/home-assistant/blob/0.75.0/homeassistant/remote.py

        # parameters
        self.url = kwargs.get('url', None)
        self.token = kwargs.get('token', None)
        self.action = kwargs.get('action', None) 
        self.stateId = kwargs.get('stateId', None)
        self.domain = kwargs.get('domain', None)
        self.service = kwargs.get('service', None)
        self.service_data = kwargs.get('service_data', None)     
        logger.debug("Home_assistant launch for action %s", self.action)

        # check parameters
        if self._is_parameters_ok():

            if self.action == "CALL_SERVICE":
                self.call_service(self.domain, self.service, self.service_data)
            elif self.action == "GET_STATE":
                self.get_state(self.stateId)

            # TODO 
            # Events GET POST
            # POST Template
            # History


    def get_state(self, stateId):
        #/api/states/stateId
        logger.debug("Get state %s", stateId)

        headers = {
            "Authorization": "Bearer " + self.token
        }
        url = urljoin(self.url, '/api/states/{}'.format(stateId))
        r = requests.get(url, headers=headers)
        data = r.json()
        result = dict()
        result["state"] = data["state"]
        for key, value in data["attributes"].items():
            result[key] = value

        self.say(result)       

    def call_service(self, domain, service, service_data):

        logger.debug("Calling service %s %s", domain, service)
        payload = service_data
        headers = {
            "Authorization": "Bearer " + self.token
        }
        url = urljoin(self.url, '/api/services/{}/{}'.format(domain, service))
        r = requests.post(url, headers=headers, json=payload)
        if r.status_code != 200:
            logger.error("Error calling service: %d - %s", r.status_code, r.text)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron.
        :return: True if parameters are ok, raise an exception otherwise.

        .. raises:: MissingParameterException, InvalidParameterException
        """
        if self.url is None:
            raise MissingParameterException("Home assistant needs an URL")
        if self.token is None:
            raise MissingParameterException("Home assistant needs a token")
        if self.action is None:
            raise MissingParameterException("Home assistant needs an action")    
        return True

