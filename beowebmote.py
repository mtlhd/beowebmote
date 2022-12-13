from flask import Flask, jsonify, make_response
from beoremotelistener import BeoremoteListener
from threading import Timer
import requests
import json
import sys

device_port = "8080"
app = Flask(__name__)
beolistener = BeoremoteListener()

def build_command_url(server, port, command_url):
    return "http://" + server + ":" + port + command_url

def post_command(device, command):
    beodevices = beolistener.get_devices()
    if device in beodevices:
        device_address = beodevices[device]
        r = requests.post(build_command_url(device_address, device_port, command))
    else:
        return make_response(jsonify(message = "Device not found"), 404) 

    if r.status_code != 200:
        return make_response(jsonify(message = "Command failed"), r.status_code) 

    return make_response(jsonify(message = "OK"), 200)

def post_command_with_release(device, command):
    beodevices = beolistener.get_devices()
    if device in beodevices:
        device_address = beodevices[device]
        r = requests.post(build_command_url(device_address, device_port, command))
        if r.status_code == 200:
            r = requests.post(build_command_url(device_address, device_port, command + "/Release"))
    else:
        return make_response(jsonify(message = "Device not found"), 404) 

    if r.status_code != 200:
        return make_response(jsonify(message = "Command failed"), r.status_code) 

    return make_response(jsonify(message = "OK"), 200)

def put_command(device, command, json_string):
    beodevices = beolistener.get_devices()
    if device in beodevices:
        device_address = beodevices[device]
        r = requests.put(build_command_url(device_address, device_port, command), json_string, headers={"Content-Type":"application/json"})
    else:
        return make_response(jsonify(message = "Device not found"), 404) 

    if r.status_code != 200:
        return make_response(jsonify(message = "Command failed"), r.status_code) 

    return make_response(jsonify(message = "OK"), 200)

def get_command(device, command):
    beodevices = beolistener.get_devices()
    if device in beodevices:
        device_address = beodevices[device]
        r = requests.get(build_command_url(device_address, device_port, command))
    else:
        return make_response(jsonify(message = "Device not found"), 404) 

    if r.status_code != 200:
        return make_response(jsonify(message = "Command failed"), r.status_code) 

    return make_response(r.text, 200)

def adjust_volume_command(device, delta):
    beodevices = beolistener.get_devices()
    if device in beodevices:
        device_address = beodevices[device]
        r = requests.get(build_command_url(device_address, device_port, "/BeoZone/Zone/Sound/Volume/Speaker"))
        if r.status_code == 200:
            data = r.json()
            key_speaker = "speaker"

            if key_speaker in data:
                speaker_data =  data[key_speaker]

                # Check for available volume range, if not found assume device will handle out of range requests
                key_range = "range"
                volume_min = 0
                volume_max = 90

                if key_range in speaker_data:
                    range_data = speaker_data[key_range]
                    key_minimum = "minimum"
                    key_maximum = "maximum"

                    if (key_minimum in range_data) and (key_maximum in range_data):
                        volume_min = range_data[key_minimum]
                        volume_max = range_data[key_maximum]

                # Get current volume level
                key_level = "level"
                if key_level in speaker_data:
                    current_level = speaker_data[key_level]
                    target_level = current_level + delta

                    if target_level > volume_max:
                        target_level = volume_max
                    if target_level < volume_min:
                        target_level = volume_min

                    return command_volume_set_level(device, str(target_level))

            # Fallback, return missing volume information
            return make_response(jsonify(message = "Volume information missing"), 404) 
                
    else:
        return make_response(jsonify(message = "Device not found"), 404) 

    if r.status_code != 200:
        return make_response(jsonify(message = "Command failed"), r.status_code) 

    return make_response(jsonify(message = "OK"), 200)

def snooze(device):
    with app.app_context():
        command_standby(device)

def allsnooze(device):
    with app.app_context():
        command_allstandby(device)

def queue_deezer_content_with_id(device, contenttype, contentid, flush):
    if flush:
        return post_command(device, "/BeoZone/Zone/PlayQueue?instantplay", "{\"playQueueItem\":{\"behaviour\":\"planned\",\"" + contenttype + "\":{\"deezer\":{\"id\":"+ contentid +"},\"image\":[]}}}")
    return post_command(device, "/BeoZone/Zone/PlayQueue", "{\"playQueueItem\":{\"behaviour\":\"planned\",\"" + contenttype + "\":{\"deezer\":{\"id\":"+ contentid +"},\"image\":[]}}}")
    
def queue_dlna_content_with_id(device, contenttype, contentUrl, flush):
    if flush:
        return post_command(device, "/BeoZone/Zone/PlayQueue?instantplay", "{\"playQueueItem\":{\"behaviour\":\"planned\",\"" + contenttype + "\":{\"dlna\":{\"url\":\""+ contentUrl +"\"}}}}")
    return post_command(device, "/BeoZone/Zone/PlayQueue", "{\"playQueueItem\":{\"behaviour\":\"planned\",\"" + contenttype + "\":{\"dlna\":{\"url\":\""+ contentUrl +"\"}}}}")
    
    
@app.route('/')
def home():
    return "Beowebmote is active with {:d} device(s) conneceted.".format(len(beolistener.get_devices().keys()))

@app.route("/devices")
def command_list_devices():
    devices = beolistener.get_devices()
    return make_response(jsonify(devices = devices), 200)

@app.route("/<device>/play")
def command_play(device):
    return post_command_with_release(device, "/BeoZone/Zone/Stream/Play")

@app.route("/<device>/stop")
def command_stop(device):
    return post_command_with_release(device, "/BeoZone/Zone/Stream/Stop")

@app.route("/<device>/pause")
def command_pause(device):
    return post_command_with_release(device, "/BeoZone/Zone/Stream/Stop")

@app.route("/<device>/next")
def command_next(device):
    return post_command_with_release(device, "/BeoZone/Zone/Stream/Forward")

@app.route("/<device>/prev")
def command_prev(device):
    return post_command_with_release(device, "/BeoZone/Zone/Stream/Backward")

@app.route("/<device>/join")
def command_join(device):
    return post_command(device, "/BeoZone/Zone/Device/OneWayJoin")

@app.route("/<device>/standby")
def command_standby(device):
    return put_command(device, "/BeoDevice/powerManagement/standby", "{\"standby\": {\"powerState\":\"standby\"}}")

@app.route("/<device>/allstandby")
def command_allstandby(device):
    return put_command(device, "/BeoDevice/powerManagement/standby", "{\"standby\": {\"powerState\":\"allStandby\"}}")

@app.route("/<device>/snooze/<delay_in_minutes>")
def command_snooze(device, delay_in_minutes):
    # duration is in seconds
    duration = int(delay_in_minutes) * 60
    t = Timer(duration, snooze, args=[device])
    t.start()
    return make_response(jsonify(message = "OK"), 200)

@app.route("/<device>/allsnooze/<delay_in_minutes>")
def command_allsnooze(device, delay_in_minutes):
    # duration is in seconds
    duration = int(delay_in_minutes) * 60
    t = Timer(duration, allsnooze, args=[device])
    t.start()
    return make_response(jsonify(message = "OK"), 200)

@app.route("/<device>/volume")
def command_volume_get_level(device):
    return get_command(device, "/BeoZone/Zone/Sound/Volume")

@app.route("/<device>/volume/<level>")
def command_volume_set_level(device, level):
    return put_command(device, "/BeoZone/Zone/Sound/Volume/Speaker/Level", "{\"level\":" + level + "}")

@app.route("/<device>/volume/up")
def command_volume_up(device):
    return adjust_volume_command(device, 1)

@app.route("/<device>/volume/down")
def command_volume_down(device):
    return adjust_volume_command(device, -1)

@app.route("/<device>/volume/ismuted")
def command_volume_ismuted(device):
    return get_command(device, "/BeoZone/Zone/Sound/Volume/Speaker/Muted")

@app.route("/<device>/volume/mute")
def command_volume_mute(device):
    return put_command(device, "/BeoZone/Zone/Sound/Volume/Speaker/Muted", "{\"muted\":true}")

@app.route("/<device>/volume/unmute")
def command_volume_unmute(device):
    return put_command(device, "/BeoZone/Zone/Sound/Volume/Speaker/Muted", "{\"muted\":false}")

@app.route("/<device>/sources")
def command_get_sources(device):
    return get_command(device, "/BeoZone/Zone/Sources")

@app.route("/<device>/queue/tunein/<stationId>")
def queue_content_with_id(device, contentType, stationId):
    return post_command(device, "/BeoZone/Zone/PlayQueue?instantplay", "{\"playQueueItem\":{\"behaviour\":\"planed\",\"station\":{\"tuneIn\":{\"stationId\":\""+ stationId +"\"},\"image\":[]}}}")

@app.route("/<device>/queue/deezer/<contentType>/<contentId>")
def queue_deezer_with_id(device, contentType, contentId):
    return queue_deezer_content_with_id(device, contentType, contentId, true)

@app.route("/<device>/play/deezer/<contentType>/<contentId>")
def play_deezer_with_id(device, contentType, contentId):
    return def queue_deezer_content_with_id(device, contentType, contentId, false)

@app.route("/<device>/queue/dlna/<contentType>/<contentUrl>")
def queue_dlna_with_id(device, contentType, contentUrl):
    return queue_dlna_content_with_id(device, contentType, contentUrl, true)

@app.route("/<device>/play/dlna/<contentType>/<contentUrl>")
def play_dlna_with_id(device, contentType, contentUrl):
    return def queue_dlna_content_with_id(device, contentType, contentUrl, false)

if __name__ == '__main__':
    app.run()
    beolistener.stop()
