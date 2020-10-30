import json
from typing import Any, Dict, List

import urllib3

from CommonServerPython import *

# Disable insecure warnings
urllib3.disable_warnings()

'''Constants'''

STANDARD_DEVICE_FIELDS = 'common.uuid,common.compliant,common.id,common.imei,common.imsi,common.last_connected_at,common.manufacturer,common.model,common.noncompliance_reasons,common.owner,common.platform,common.quarantined,common.quarantined_reasons,common.registration_date,common.status,user.display_name,user.email_address,user.user_id,common.security_state'
FETCH_INCIDENTS_DEVICE_QUERY = 'common.status = \"ACTIVE\" AND (common.quarantined = true OR common.compliant = ' \
                               'false OR common.security_state != \"Ok\") '

# Incident Severity Constants

SEVERITY_LOW = 1
SEVERITY_MEDIUM = 2
SEVERITY_HIGH = 3
SEVERITY_CRITICAL = 4

# This is just for tracking, not actually shown to the user
DEFAULT_ACTION_NOTE = 'Message sent through XSOAR-Integration'

CORE_DEVICE_TO_INCIDENT_MAPPING = {
    'common.uuid': 'deviceId',
    'common.id': 'Id',
    'common.os_version': 'OS Version',
    'common.manufacturer': 'manufacturer',
    'common.model': 'DeviceModel',
    'common.status': 'Registration Status',
    'common.imei': 'IMEI',
    'common.imsi': 'IMSI',
    'common.platform': 'Platform',
    'common.security_state': 'Security State',
    'user.display_name': 'User Display Name',
    'user.email_address': 'User Email address',
    'user.user_id': 'User ID',
    'common.last_connected_at': 'Last check in Timestamp',
    'common.registration_date': 'Device registration timestamp',
    'common.owner': 'Device Owner',
    'common.quarantined': 'IsDeviceQuarantined',
    'common.compliant': 'IsDeviceCompliant'
}


class MobileIronCoreClient(BaseClient):
    """Client class to interact with the MobileIron Core API"""

    def __get_device_data_page(self, current_page: int = 0, per_page: int = 50, query: str = None,
                               fields: str = None, admin_space_id: str = None) -> List[Any]:
        response = self._http_request(
            method='GET',
            url_suffix='/api/v2/devices',
            params={
                'adminDeviceSpaceId': admin_space_id,
                'query': query,
                'fields': fields,
                'limit': per_page,
                'offset': current_page
            })
        results: List = response['results']
        if len(results) < per_page:
            return results
        else:
            return results + self.__get_device_data_page(current_page + 1, per_page, query, fields, admin_space_id)

    def get_devices_data(self, admin_space_id: str, query: str = None, fields: str = None) -> List[Any]:
        """Gets the Devices Data from MobileIron Core

        :type query: ``str``
        :param query: Conditions in the Core API Call

        :type fields: ``str``
        :param fields: Attributes to be retrieved

        :type admin_space_id: ``str``
        :param admin_space_id: Admin Space ID

        :return: list containing all device info as returned from the API
        :rtype: ``List``
        """

        if not admin_space_id:
            raise ValueError('admin_space_id not specified')

        return self.__get_device_data_page(query=query, fields=fields, admin_space_id=admin_space_id)

    def execute_device_action(self, device_id: str, admin_space_id: str, command_action: str) -> Dict[str, Any]:
        """Execute device action.

        :type command_action: ``str``
        :param command_action: Action String based on the action to be performed over MobileIron Core.

        :type device_id: ``str``
        :param device_id: DeviceID on which the actions should be performed..

        :type admin_space_id: ``str``
        :param admin_space_id: Admin Space ID

        :return: dict containing the scan results as returned from the API
        :rtype: ``Dict[str, Any]``

        """

        if not device_id:
            raise ValueError('device_id not specified')

        if not admin_space_id:
            raise ValueError('admin_space_id not specified')

        if not command_action:
            raise ValueError('command_action not specified')

        method_type = 'PUT'
        if command_action == 'WIPE_DEVICE':
            action_url_suffix = 'wipe'
        elif command_action == 'RETIRE':
            action_url_suffix = 'retire'
        elif command_action == 'WAKE_UP':
            action_url_suffix = 'wakeup'
        else:
            action_url_suffix = 'action'
            method_type = 'POST'

        payload = {'deviceUuids': [device_id], 'note': DEFAULT_ACTION_NOTE}

        return self._http_request(
            method=method_type,
            url_suffix=f'/api/v2/devices/{action_url_suffix}',
            params={
                'adminDeviceSpaceId': admin_space_id,
                'actionType': command_action
            },
            json_data=payload
        )

    def send_message_action(self, device_id: str, admin_space_id: str, message: str, message_mode: str = 'pns',
                            message_subject: str = '') -> \
            Dict[str, Any]:
        """Execute send message action to MobileIron CORE based on the conditions.

        :type device_id: ``str``
        :param device_id: DeviceID on which the actions should be performed..

        :type admin_space_id: ``str``
        :param admin_space_id: Admin Space ID

        :type message: ``str``
        :param message: Message to send to the specified devices.

        :type message_mode: ``str``
        :param message_mode: Mode of the message:
                            • pns (push notifications)
                            • sms
                            • email (email takes the subject parameter, too)

        :type message_subject: ``str``
        :param message_subject: Provide if desired when the message mode is email.

        :return: dict containing the scan results as returned from the API
        :rtype: ``Dict[str, Any]``
        """

        if not device_id:
            raise ValueError('device_id not specified')

        if not admin_space_id:
            raise ValueError('admin_space_id not specified')

        payload = {'deviceUuids': [device_id], 'note': DEFAULT_ACTION_NOTE,
                   'additionalParameters': {'message': message, 'mode': message_mode, 'subject': message_subject}}
        return self._http_request(
            method='POST',
            url_suffix='/api/v2/devices/action',
            params={
                'adminDeviceSpaceId': admin_space_id,
                'actionType': 'SEND_MESSAGE'
            },
            json_data=payload
        )

    def ping(self):
        """Executes PING ´to check for the connection with MobileIron CORE.

        :return: Ping Response
        :rtype:
        """
        return self._http_request(
            method='GET',
            url_suffix='/api/v2/ping'
        )


def __resolve_device_incident_severity(device_info: Dict[str, Any]) -> int:
    """
    Gets the severity based on following conditions

    :type device_info: ``json``
    :param device_info: Dictionary containing the device information

    return : 'int'
    return param: returns severity to be set on the incident
    """

    if device_info['common.security_state'] != 'Ok':
        return SEVERITY_CRITICAL
    elif not device_info['common.complaint']:
        return SEVERITY_HIGH
    elif device_info['common.quarantined']:
        return SEVERITY_LOW


def __rename_keys(event_input: Dict[str, Any], keys: Dict[str, Any]) -> Dict[str, Any]:
    """ Function to rename/translate keys from the API Response

        :type event_input: ``str``
        :param event_input: Each device information retrieved from CORE.
        :type keys: ``str``
        :param keys: Translated keys set as definied in the headers.

        :return: dict containing the scan results as returned from the API
        :rtype: ``Dict[str, Any]``
        """

    return dict([(keys.get(k, k), v) for k, v in event_input.items()])


def __datetime_to_posix_without_milliseconds(datetime_object):
    """ Function to convert UTC time to string. """
    timestamp_in_unix_millisecond = date_to_timestamp(datetime_object, 'datetime.datetime')
    posix_with_ms = timestamp_in_unix_millisecond
    posix_without_ms = str(posix_with_ms).split(',')[0]
    return posix_without_ms


def __validate_action_response(response) -> str:
    validation = response["successful"]
    if validation:
        return 'Command has been executed successfully'
    else:
        raise DemistoException(
            'API indicated that the request was not successful. Make sure the device id provided is valid')


def execute_device_action_command(client: MobileIronCoreClient, params: Dict[str, Any], args: Dict[str, Any],
                                  action: str) -> str:
    """execute_device_action_command: Returns results for a MobileIron Device Action

    :type client: ``Client``
    :param client: MobileIron client to use

    :type action: ``str``
    :param action: Device Specific Action, one of the following actions are allowed:
        - Retire a device
        - Wipe a device - This is potentially a destructive action
        - Send a message
        - Force Checkin a device
        - ENABLE_VOICE_ROAMING (iOS)
        - DISABLE_VOICE_ROAMING (iOS)
        - ENABLE_DATA_ROAMING (iOS)
        - DISABLE_DATA_ROAMING (iOS)
        - ENABLE_PERSONAL_HOTSPOT (iOS)
        - DISABLE_PERSONAL_HOTSPOT (iOS)
        - UPDATE_OS (iOS)
        - UNLOCK_APP_CONNECT_CONTAINER (Android)
        - UNLOCK_DEVICE_ONLY (Android, iOS)

    :type params: ``Dict[str, Any]``
    :param params:
        all global parameters, usually passed from ``demisto.params()``.
        ``params['admin_space_id']`` Admin Space ID for the tenant

    :type args: ``Dict[str, Any]``
    :param args:
        all command arguments, usually passed from ``demisto.args()``.
        ``args['device_id']`` Device ID

    :return:
        Status of the request. In case of issues executing this request an exception will be raised.
    :rtype: ``str``
    """

    device_id = args.get('device_id')
    admin_space_id = params.get('admin_space_id')
    response = client.execute_device_action(device_id=device_id, admin_space_id=admin_space_id, command_action=action)
    return __validate_action_response(response)


def execute_test_module_command(client: MobileIronCoreClient):
    """ This definition is for test command - get Ping response from Core

        :return: demisto.results('ok')
        :rtype: string.
    """
    response = client.ping()
    if response and (response["results"]):
        return 'ok'


def fetch_incidents(client: MobileIronCoreClient, params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
        This function returns incidents after analyzing the response data

        This function has to implement the logic of making sure that incidents are
        fetched based on analyzing the response data. By default it's invoked by
        XSOAR every minute. It will use last_run to save the timestamp of the last
        incident it processed.

        :type client: ``Client``
        :param client: MobileIron Core client to use

        :type params: ``Dict[str, Any]``
        :param params:
            all global parameters, usually passed from ``demisto.params()``.
            ``params['admin_space_id']`` Admin Space ID for the tenant

        :return:
            incidents are returned in the form of dict
    """

    # Initialize an empty list of incidents to return
    # Each incident is a dict with a string as a key
    incidents: List[Dict[str, Any]] = []

    """get the devices data from Core Call API response"""
    admin_space_id = params.get('admin_space_id')
    devices = client.get_devices_data(admin_space_id=admin_space_id,
                                      query=FETCH_INCIDENTS_DEVICE_QUERY, fields=STANDARD_DEVICE_FIELDS)
    for device in devices:
        # If no name is present it will throw an exception
        incident_name = device['common.model']

        # Rename keys for device attributes
        modified_device = __rename_keys(device, CORE_DEVICE_TO_INCIDENT_MAPPING)

        # get Device Severity
        severity = __resolve_device_incident_severity(device)

        # Incident type is fetched from the Instance configuration parameters.
        incident_type = demisto.params().get('incidentType')

        incident = {
            'name': incident_name,
            'rawJSON': json.dumps(modified_device),
            'type': incident_type,
            'severity': severity
        }
        incidents.append(incident)

    return incidents


def execute_get_device_by_id_command(client: MobileIronCoreClient, params: Dict[str, Any],
                                     args: Dict[str, Any]) -> CommandResults:
    """get-device-by-id command: Returns a specific device by providing the device id

        :type client: ``MobileIronCoreClient``
        :param client: MobileIron UEM API client to use

        :type params: ``Dict[str, Any]``
        :param params:
            all global parameters, usually passed from ``demisto.params()``
            ``params['admin_space_id']`` Admin Space ID for the tenant

        :type args: ``Dict[str, Any]``
        :param args:
            all command arguments, usually passed from ``demisto.args()``
            ``args['device_id']`` Device UUID of the device to query for

        :return:
            A ``CommandResults`` object that is then passed to ``return_results``,
            that contains the device data

        :rtype: ``CommandResults``
        """

    additional_fields = args.get('additional_fields')
    if additional_fields:
        fields = ','.join([STANDARD_DEVICE_FIELDS, additional_fields])
    else:
        fields = STANDARD_DEVICE_FIELDS

    admin_space_id = params.get('admin_space_id')

    device_id = args.get('device_id')
    query = f'common.uuid="{device_id}"'

    devices_data_response = client.get_devices_data(admin_space_id=admin_space_id, query=query, fields=fields)
    device = next(iter(devices_data_response), None)

    if not device:
        raise ValueError('device not found in system')

    return CommandResults(
        outputs_prefix='MobileIron.DeviceInfo',
        outputs_key_field='device_data',
        outputs=device
    )


def execute_get_devices_data_command(client: MobileIronCoreClient, params: Dict[str, Any],
                                     args: Dict[str, Any]) -> CommandResults:
    """get-devices command: Returns a list of all devices in the mobileiron system based on the query provided. This command might
    execute multiple API calls if there are a large amount of device to fetch

    :type client: ``MobileIronCoreClient``
    :param client: MobileIron UEM API client to use

    :type params: ``Dict[str, Any]``
    :param params:
        all global parameters, usually passed from ``demisto.params()``

    :type args: ``Dict[str, Any]``
    :param args:
        all command arguments, usually passed from ``demisto.args()``

    :return:
        A ``CommandResults`` object that is then passed to ``return_results``,
        that contains the device data

    :rtype: ``CommandResults``
    """

    additional_fields = args.get('additional_fields')
    if additional_fields:
        fields = ','.join([STANDARD_DEVICE_FIELDS, additional_fields])
    else:
        fields = STANDARD_DEVICE_FIELDS

    query = args.get('query')
    admin_space_id = params.get('admin_space_id')

    devices_data_response = client.get_devices_data(admin_space_id=admin_space_id, query=query, fields=fields)

    return CommandResults(
        # readable_output=readable_output,
        outputs_prefix='MobileIron.DevicesInfo',
        outputs_key_field='devices_data',
        outputs=devices_data_response
    )


def send_message_command(client: MobileIronCoreClient, params: Dict[str, Any], args: Dict[str, Any]) -> str:
    """mobileiron-update-os command: Returns results for a MobileIron Send Message Action

    :type client: ``MobileIronCoreClient``
    :param client: MobileIron client to use

    :type params: ``Dict[str, Any]``
    :param params:
        all global parameters, usually passed from ``demisto.params()``

    :type args: ``Dict[str, Any]``
    :param args:
        all command arguments, usually passed from ``demisto.args()``.
        ``args['device_id']`` Device UUID

    :return:
        A ``CommandResults`` compatible to return ``return_results()``,
        that contains an action result
        A Dict of entries also compatible to ``return_results()``

    :rtype: ``CommandResults``
    """

    device_id = args.get('device_id')
    admin_space_id = params.get('admin_space_id')
    message = args.get('message')
    subject = args.get('subject')
    message_mode = args.get('push_message')

    if not device_id:
        raise ValueError('device_id not specified')
    if not admin_space_id:
        raise ValueError('admin_space_id not specified')

    response = client.send_message_action(device_id=device_id, admin_space_id=admin_space_id, message=message,
                                          message_mode=message_mode, message_subject=subject)
    return __validate_action_response(response)


def main():
    # if your MobileIronClient class inherits from BaseClient, SSL verification is
    # handled out of the box by it, just pass ``verify_certificate`` to
    # the MobileIronClient constructor
    params = demisto.params()
    args = demisto.args()

    verify_certificate = not params.get('insecure', False)

    # if your MobileIronClient class inherits from BaseClient, system proxy is handled
    # out of the box by it, just pass ``proxy`` to the MobileIronClient constructor
    proxy = params.get('proxy', False)
    base_url = params.get('url')
    credentials = params.get('credentials')
    username = credentials.get('identifier')
    password = credentials.get('password')

    auth_header = b64_encode(f'{username}:{password}')
    headers = {
        'Authorization': f'Basic {auth_header}'
    }
    try:
        client = MobileIronCoreClient(
            base_url=base_url,
            verify=verify_certificate,
            headers=headers,
            proxy=proxy)

        if demisto.command() == 'test-module':
            # This is the call made when pressing the integration Test button.
            return_results(execute_test_module_command(client))

        elif demisto.command() == 'fetch-incidents':
            # Code For changing the pull incidents with timeline.
            now_utc = datetime.utcnow()
            current_run_time = __datetime_to_posix_without_milliseconds(now_utc)

            last_run_data = demisto.getLastRun()
            last_run_time = int(0)
            if last_run_data:
                last_run_time = last_run_data['time']

            next_run_interval = params.get('fetch_interval')
            date_time_interval_ago = now_utc - timedelta(minutes=int(next_run_interval))
            time_interval_ago = __datetime_to_posix_without_milliseconds(date_time_interval_ago)

            if last_run_time != 0 and last_run_time > time_interval_ago:
                demisto.incidents([])
                sys.exit(0)
                # End of skip based on the time interval.

            # Set and define the fetch incidents command to run after activated via integration settings.
            incidents = fetch_incidents(client=client, params=params)
            # fetch-incidents calls ``demisto.incidents()`` to provide the list
            # of incidents to crate
            demisto.incidents(incidents)
            demisto.setLastRun({'time': current_run_time})

        elif demisto.command() == 'mobileiron-get-devices-data':
            # To get the list of devices data with the given parameters.
            return_results(execute_get_devices_data_command(client, params, args))

        elif demisto.command() == 'mobileiron-get-device-by-id':
            # To get the list of devices data with the given parameters.
            return_results(execute_get_device_by_id_command(client, params, args))

        elif demisto.command() == 'mobileiron-unlock-device-only':
            # Action to unlock a Fetched device based on device id
            return_results(
                execute_device_action_command(client, params, args, "UNLOCK_DEVICE_ONLY"))

        elif demisto.command() == 'mobileiron-enable-voice-roaming':
            # Action to enable voice roaming on a Fetched device based on device id
            return_results(
                execute_device_action_command(client, params, args, "ENABLE_VOICE_ROAMING"))

        elif demisto.command() == 'mobileiron-disable-voice-roaming':
            # Action to disable voice roaming on a Fetched device based on device id
            # return_results(disable_voice_roaming_command(client, demisto.args()))DISABLE_VOICE_ROAMING
            return_results(
                execute_device_action_command(client, params, args, "DISABLE_VOICE_ROAMING"))

        elif demisto.command() == 'mobileiron-enable-data-roaming':
            # Action to enable data roaming on a Fetched device based on device id
            return_results(
                execute_device_action_command(client, params, args, "ENABLE_DATA_ROAMING"))

        elif demisto.command() == 'mobileiron-disable-data-roaming':
            # Action to disable data roaming on a Fetched device based on device id
            return_results(
                execute_device_action_command(client, params, args, "DISABLE_DATA_ROAMING"))

        elif demisto.command() == 'mobileiron-enable-personal-hotspot':
            # Action to enable personal hotspot on a Fetched device based on device id
            return_results(
                execute_device_action_command(client, params, args, "ENABLE_PERSONAL_HOTSPOT"))

        elif demisto.command() == 'mobileiron-disable-personal-hotspot':
            # Action to disable personal hotspot on a Fetched device based on device id
            return_results(
                execute_device_action_command(client, params, args, "DISABLE_PERSONAL_HOTSPOT"))

        elif demisto.command() == 'mobileiron-send-message':
            # Action to send message on a Fetched device based on device id
            return_results(send_message_command(client, params, args))

        elif demisto.command() == 'mobileiron-update-os':
            # Action to update OS on a Fetched device based on device id
            return_results(execute_device_action_command(client, params, args, "UPDATE_OS"))

        elif demisto.command() == 'mobileiron-unlock-app-connect-container':
            # Action to unlock app container on a Fetched device based on device id
            return_results(
                execute_device_action_command(client, params, args, "UNLOCK_APP_CONNECT_CONTAINER"))

        elif demisto.command() == 'mobileiron-retire-device':
            # Action to retire a device on a Fetched device based on device id
            return_results(execute_device_action_command(client, params, args, "RETIRE"))

        elif demisto.command() == 'mobileiron-wipe-device':
            # Action to wipe a device on a Fetched device based on device id
            # return_results(wipe_device_command(client, demisto.args()))
            return_results(execute_device_action_command(client, params, args, "WIPE_DEVICE"))

        elif demisto.command() == 'mobileiron-force-checkin':
            # Action to force-checkin a device on a Fetched device based on device id
            return_results(execute_device_action_command(client, params, args, "WAKE_UP"))

    # Log exceptions and return errors
    except Exception as e:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute {demisto.command()} command.\nError:\n{str(e)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
