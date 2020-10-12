import json
import requests
import traceback
from typing import Any, Dict, Tuple, List, Optional, Union, cast

translation_cloud = {'guid':'deviceId','id':'Id','platformVersion':'OS Version','manufacturer':'manufacturer','deviceModel':'DeviceModel','registrationState':'registration Status','imei':'IMEI','imsi':'IMSI','platformType':'Platform','jailbroken':'Security State','displayName':'User Display Name','emailAddress':'User Email address','uid':'User ID','clientLastCheckin':'Last check in Timestamp','lastRegistrationTime':'Device registration timestamp','ownershipType':'DeviceOwner','quarantined':'IsDeviceQuarantined','complianceState':'IsDeviceCompliant'}

params = demisto.params()
credentials = params.get('credentials')
username = credentials.get('identifier')
password = credentials.get('password')

incidents = []
translation = []

def rename_keys(event_input, keys):
    return dict([(keys.get(k, k), v) for k, v in event_input.items()])

def fetch_device_data():
    if(main.response.status_code == 200):
        data = main.response.json()
        results = data["result"]
        results = results["searchResults"]
        for eve in results:
            modified_attr = rename_keys(eve, translation_cloud)
            translation.append(modified_attr)

def create_incident():
    for event in translation:
      incident = {
          'name': event['manufacturer'],
          'severity': 1,
          'type': 'DoS',
          'rawJSON': json.dumps(event)
      }
      incidents.append(incident)
    demisto.incidents(incidents)

def mobileiron_fetchresults():
    fetch_device_data()
    create_incident()

def version_status():

    version_url = "https://eu1.mobileiron.com/api/v1/tenant/partition/device"
    response = requests.get(version_url, auth=(username, password))
    if(response.status_code == 200):
        demisto.results('ok')
    else:
        raise ValueError('Username or Password is incorrect')


def send_message(deviceid):
    payload = "{\"deviceUuids\":[deviceid],\"note\":\"Success\"}"
    voice_roaming_url = "https://core.darksevt.com/api/v2/devices/action?adminDeviceSpaceId=1&actionType=SEND_MESSAGE"
    response = requests.request("POST", voice_roaming_url, auth=(username, password), data = payload)
    if(response.status_code == 200):
        demisto.results('ok')
    else:
        demisto.results(response)

def update_os(deviceid):
    payload = "{\"deviceUuids\":[deviceid],\"note\":\"Success\"}"
    voice_roaming_url = "https://core.darksevt.com/api/v2/devices/action?adminDeviceSpaceId=1&actionType=UPDATE_OS"
    response = requests.request("POST", voice_roaming_url, auth=(username, password), data = payload)
    if(response.status_code == 200):
        demisto.results('ok')
    else:
        demisto.results(response)

def unlock_device_only(deviceid):
    payload = "{\"deviceUuids\":[deviceid],\"note\":\"Success\"}"
    voice_roaming_url = "https://core.darksevt.com/api/v2/devices/action?adminDeviceSpaceId=1&actionType=UNLOCK_DEVICE_ONLY"
    response = requests.request("POST", voice_roaming_url, auth=(username, password), data = payload)
    if(response.status_code == 200):
        demisto.results('ok')
    else:
        demisto.results(response)

def main():

    main.response = None
    main.url = demisto.params().get('url')+"dmPartitionId="+demisto.params().get('adminDeviceSpaceId')+"&fq="+demisto.params().get('query')
    main.response = requests.get(main.url,auth=(username, password))

    device_id=demisto.args().get('deviceUuids')

    if demisto.command() == 'test-module':
            # This is the call made when pressing the integration Test button.
            version_status()

    elif demisto.command() == 'fetch-incidents':
        # Set and define the fetch incidents command to run after activated via integration settings.
        mobileiron_fetchresults()

    elif demisto.command() == 'getDevicesData':
        # Set and define the fetch incidents command to run after activated via integration settings.
        #fetch_device_data()
         return_results(fetch_device_data(demisto.args()))

    elif demisto.command() == 'CreateIncidents':
        # Set and define the fetch incidents command to run after activated via integration settings.
        #create_incident()
        return_results(create_incident(demisto.args()))

    elif demisto.command() == 'SEND_MESSAGE':
        send_message(device_id)

    elif demisto.command() == 'UPDATE_OS':
        update_os(device_id)

    elif demisto.command() == 'UNLOCK_DEVICE_ONLY':
        unlock_device_only(device_id)

if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()