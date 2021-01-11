# beowebmote
Beo web remote - web server for controlling network link attached B&amp;O devices

## Usage
Launch the web server using the following command:
```
  python beowebmote.py
```

On startup the script starts to listen for beolink services on the local network and for requests on port 5000.

## Supported Commands

### Heartbeat/Status
Get the status of the web server.
```
  http://<beowebmote_host>:5000/
```

### List Available Devices
List all devices available on the local network.
```
  http://<beowebmote_host>:5000/devices
```

### Basic Playback Handling
#### Play
Start playback of selected source.
```
  http://<beowebmote_host>:5000/<device_name>/play
```

#### Pause
Pause playback of selected source.
```
  http://<beowebmote_host>:5000/<device_name>/pause
```

#### Stop
Stop playback of selected source.
```
  http://<beowebmote_host>:5000/<device_name>/stop
```

#### Next
Skip to next track or channel for the selected source.
```
  http://<beowebmote_host>:5000/<device_name>/next
```

#### Previous 
Select previous track or channel for the selected source.
```
  http://<beowebmote_host>:5000/<device_name>/prev
```

### Power Management
#### Single Device Standby
Put a specific device into standby.
```
  http://<beowebmote_host>:5000/<device_name>/standby
```

#### All Devices Standby
Put all devices into standby.
```
  http://<beowebmote_host>:5000/<device_name>/allstandby
```

#### Snooze Single Device
Put a specific device into standby after a delay specified in minutes. Minutes should be an integer value. 
```
  http://<beowebmote_host>:5000/<device_name>/snooze/<delay_in_minutes>
```

#### Snooze All Devices
Put all devices into standby after a delay specified in minutes. Minutes should be an integer value.
```
  http://<beowebmote_host>:5000/<device_name>/allsnooze/<delay_in_minutes>
```

### Volume Handling
#### Get Device Volume
Get the current volume set for a device.
```
  http://<beowebmote_host>:5000/<device_name>/volume
```

#### Set Device Volume
Set the volume to a certain level for a specific device. Range is 1-100, but is also limited by device settings.
```
  http://<beowebmote_host>:5000/<device_name>/volume/<level>
```

#### Increase Device Volume
Increase the volume by one for a specific device.
```
  http://<beowebmote_host>:5000/<device_name>/volume/up
```

#### Decrease Device Volume
Decrease the volume by one for a specific device.
```
  http://<beowebmote_host>:5000/<device_name>/volume/down
```

#### Get Device Mute Status
Get the mute status for a select device.
```
  http://<beowebmote_host>:5000/<device_name>/volume/ismuted
```

#### Mute Device
Mutes a select device.
```
  http://<beowebmote_host>:5000/<device_name>/volume/mute
```

#### Unmute Device
Unmutes a select device.
```
  http://<beowebmote_host>:5000/<device_name>/volume/unmute
```

### Source Handling
#### List Available Sources for Device
```
  http://<beowebmote_host>:5000/<device_name>/sources
```

#### Join an On-going Session
```
  http://<beowebmote_host>:5000/<device_name>/join
```



