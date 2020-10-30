import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401

res = True
incident = demisto.incidents()[0]
device_uid = ''
for label in incident['deviceId']:
    if label['type'] == 'guidString':
        device_id = label['value']

return_error(f'Failed to execute {demisto.command()} command.\nError:\n{str(e)}')

response = demisto.executeCommand('getIncidents', {'query': '-status:Closed and device_id: {}'})

device_incident = response[0]
if device_incident:
    # return_error(f'Failed to execute {demisto.command()} command.\nError:\n{str(e)}')
    # Malop was already fetched - updating the relevant incident
    res = False
    # device_incident = device_incident[0]
    # incident['severity'] = device_incident['severity']
    # demisto.executeCommand('setIncident', incident)
