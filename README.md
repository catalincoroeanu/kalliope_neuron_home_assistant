# Home Assistant

## Synopsis

This neuron allows to control your [Home assistant](https://www.home-assistant.io/) instance.

## Installation

```bash
kalliope install --git-url https://github.com/royto/kalliope_neuron_home_assistant.git
```

## Prerequisites

The [http component](https://www.home-assistant.io/components/http/) need to be configured with an api_password to enforce security

## CALL SERVICE

Allows to call a home assistant service

### Options

| parameter   | required | type   | default | choices    | comment                              |
|-------------|----------|--------|---------|------------|--------------------------------------|
| url         | YES      | String | None    |            | url of your home assistant instance with port     |
| password    | YES      | String | None    |   |the configured api_password |
| domain    | YES      | String | None    |   |the domain of the service |
| service    | YES      | String | None    |   |the service to call|
| service_data    | NO      | dict | None    |   |the service data|

#### Return Values

No return

| Name    | Description                                                          | Type   | sample        |
|---------|----------------------------------------------------------------------|--------|---------------|

#### Synapses example

Example without service_data : Restart home assistant

``` yml
    - name: "hass-restart"
    signals:
      - order: "Restart Home Assistant"
    neurons:
      - home_assistant:
          url: "http://192.168.0.1:8123"
          password: XXXX
          action: CALL_SERVICE
          domain: homeassistant
          service: restart
```

Example with service_data : Locate Vacuum

``` yml
  - name: "hass-locate-vacuum"
    signals:
      - order: "Where is the vacuum"
    neurons:
      - home_assistant:
          url: "http://192.168.0.1:8123"
          password: XXX
          action: CALL_SERVICE
          domain: vacuum
          service: locate
          service_data:
            entity_id: vacuum.xiaomi_vacuum_cleaner
```

## GET_STATE

Allows to get thermostat status

### Options

| parameter   | required | type   | default | choices    | comment                              |
|-------------|----------|--------|---------|------------|--------------------------------------|
| url         | YES      | String | None    |            | url of your home assistant instance with port     |
| password    | YES      | String | None    |   |the configured api_password |
| stateId    | YES      | String | None    |   |Id of the state |

#### Return Values

State value and associated attributes

| Name    | Description                                                          | Type   | sample        |
|---------|----------------------------------------------------------------------|--------|---------------|
| state | State value | depend of state | 12 |
| `attributeName` | Name of the attribute ||

#### Synapses example

``` yml
 - name: "hass-get-sun-state"
    signals:
      - order: "Sun state"
    neurons:
      - home_assistant:
          url: "http://192.168.1.1:8123"
          password: XXX
          action: GET_STATE
          stateId: sun.sun
```

Response Example

```python
{
   'elevation': -52.58,
   'next_noon': '2018-11-23T11:23:06+00:00', 'friendly_name': 'Sun',
   'next_setting': '2018-11-23T16:01:23+00:00',
   'state': 'below_horizon',
   'next_rising': '2018-11-23T06:44:49+00:00', 'next_dawn': '2018-11-23T06:12:19+00:00',
   'azimuth': 299.88,
   'next_dusk': '2018-11-23T16:33:53+00:00', 'next_midnight': '2018-11-22T23:23:15+00:00'
}
```