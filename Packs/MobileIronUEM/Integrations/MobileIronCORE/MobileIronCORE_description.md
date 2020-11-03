MobileIron CORE Integration
This integration was integrated and tested with version xx of MobileIronCORE
## Configure MobileIronCORE on Cortex XSOAR

1. Navigate to **Settings** > **Integrations** > **Servers & Services**.
2. Search for MobileIronCORE.
3. Click **Add instance** to create and configure a new integration instance.

| **Parameter** | **Description** | **Required** |
| --- | --- | --- |
| url | Server URL \(e.g. https://core.mobileiron.com\) | True |
| admin_space_id | Admin Space ID \(e.g. 1 for the global space id\) | True |
| credentials | API User Credentials | True |
| max_fetch | Maximum number of incidents per fetch | False |
| first_fetch | First fetch time | False |
| incidentType | Incident type | False |
| insecure | Trust any certificate \(not secure\) | False |
| proxy | Use system proxy settings | False |
| fetch_interval | Fetch Interval \(in minutes\) | True |
| isFetch | Fetch incidents | False |

4. Click **Test** to validate the URLs, token, and connection.
## Commands
You can execute these commands from the Demisto CLI, as part of an automation, or in a playbook.
After you successfully execute a command, a DBot message appears in the War Room with the command details.
### mobileiron-send-message
***
This command is used to send a message to the particular device based on device id


#### Base Command

`mobileiron-send-message`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| device_id | This argument fetch the device id for mobileiron send message command | Optional | 
| subject | Provide Subject for email | Required | 
| message | Provide message for email | Required | 
| push_message | Push Message Mode | Required | 


#### Context Output

There is no context output for this command.

#### Command Example
``` ```

#### Human Readable Output



### mobileiron-update-os
***
This command is used to update OS to the particular device based on device id


#### Base Command

`mobileiron-update-os`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| device_id | This argument fetch the device id for mobileiron update os command | Optional | 


#### Context Output

There is no context output for this command.

#### Command Example
``` ```

#### Human Readable Output



### mobileiron-unlock-device-only
***
This command is used to unlock device to the particular device based on device id


#### Base Command

`mobileiron-unlock-device-only`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| device_id | This argument fetch the device id for mobileiron unlock device only command | Optional | 


#### Context Output

There is no context output for this command.

#### Command Example
``` ```

#### Human Readable Output



### mobileiron-enable-voice-roaming
***
This command is used to enable voice roaming to the particular device based on device id


#### Base Command

`mobileiron-enable-voice-roaming`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| device_id | This argument fetch the device id for mobileiron enable voice roaming command | Optional | 


#### Context Output

There is no context output for this command.

#### Command Example
``` ```

#### Human Readable Output



### mobileiron-disable-voice-roaming
***
This command is used to disable voice roaming to the particular device based on device id


#### Base Command

`mobileiron-disable-voice-roaming`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| device_id | This argument fetch the device id for mobileiron disable voice roaming command | Optional | 


#### Context Output

There is no context output for this command.

#### Command Example
``` ```

#### Human Readable Output



### mobileiron-enable-data-roaming
***
This command is used to enable data roaming to the particular device based on device id


#### Base Command

`mobileiron-enable-data-roaming`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| device_id | This argument fetch the device id for mobileiron enable data roaming command | Optional | 


#### Context Output

There is no context output for this command.

#### Command Example
``` ```

#### Human Readable Output



### mobileiron-disable-data-roaming
***
This command is used to disable data roaming to the particular device based on device id


#### Base Command

`mobileiron-disable-data-roaming`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| device_id | This argument fetch the device id for mobileiron disable data roaming command | Optional | 


#### Context Output

There is no context output for this command.

#### Command Example
``` ```

#### Human Readable Output



### mobileiron-enable-personal-hotspot
***
This command is used to enable personal hotspot to the particular device based on device id


#### Base Command

`mobileiron-enable-personal-hotspot`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| device_id | This argument fetch the device id for mobileiron enable personal hotspot command | Optional | 


#### Context Output

There is no context output for this command.

#### Command Example
``` ```

#### Human Readable Output



### mobileiron-disable-personal-hotspot
***
This command is used to disable personal hotspot to the particular device based on device id


#### Base Command

`mobileiron-disable-personal-hotspot`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| device_id | This argument fetch the device id for mobileiron disable personal hotspot command | Optional | 


#### Context Output

There is no context output for this command.

#### Command Example
``` ```

#### Human Readable Output



### mobileiron-unlock-app-connect-container
***
This command is used to unlock app connect container to the particular device based on device id


#### Base Command

`mobileiron-unlock-app-connect-container`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| device_id | This argument fetch the device id for mobileiron unlock app connect container command | Optional | 


#### Context Output

There is no context output for this command.

#### Command Example
``` ```

#### Human Readable Output



### mobileiron-retire-device
***
This command is used to retire device to the particular device based on device id


#### Base Command

`mobileiron-retire-device`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| device_id | This argument fetch the device id for mobileiron retire device command | Optional | 


#### Context Output

There is no context output for this command.

#### Command Example
``` ```

#### Human Readable Output



### mobileiron-wipe-device
***
This command is used to wipe device to the particular device based on device id


#### Base Command

`mobileiron-wipe-device`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| device_id | device id pointing to the device to execute the command on | Optional | 


#### Context Output

There is no context output for this command.

#### Command Example
``` ```

#### Human Readable Output



### mobileiron-force-checkin
***
This command is used to force checkin to the particular device based on device id


#### Base Command

`mobileiron-force-checkin`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| device_id | This argument fetch the device id for mobileiron force checkin command | Optional | 


#### Context Output

There is no context output for this command.

#### Command Example
``` ```

#### Human Readable Output



### mobileiron-get-devices-data
***
This command is used to get devices data to the particular device based on device id


#### Base Command

`mobileiron-get-devices-data`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| query | The query which to execute to filter down the list of devices | Optional | 
| additional_fields | comma separated list of fields to query from the API | Optional | 


#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| MobileIron.DevicesInfo | Unknown | Fetches the data from devices | 


#### Command Example
``` ```

#### Human Readable Output



### mobileiron-get-device-by-id
***
This command is used to get a single devic based on the device id


#### Base Command

`mobileiron-get-device-by-id`
#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| device_id | device id pointing to the device to execute the command on | Optional | 
| additional_fields | comma separated list of fields to query from the API | Optional | 


#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| MobileIron.DeviceInfo | Unknown | Contains the response with the device data | 


#### Command Example
``` ```

#### Human Readable Output


