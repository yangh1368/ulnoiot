# integriot __init__
#
# This allows you to easily build an integrator for binding mqtt
# objects together.
# You can also use it to easily build mqtt-drivers or devices
#
# It was initially developed for ulnoiot (http://github.com/ulno/ulnoiot)
#
# Author: Ulrich Norbisrath (http://ulno.net)
# Created: 2017-10-05

from integriot import thingconnector

_stopped = False
_main_devices = None

def thingi(t, cb={}):
    '''

    :param t:
    :param cb:
    :return:
    '''
    global _main_devices
    return _main_devices.remote_sensor(t, cb)


# Careful: all the following have to be understood as being remotely connected
# to network nodes
def sensor(t, cb={}):
    global _main_devices
    return _main_devices.remote_sensor(t, cb)


def actor(t):
    global _main_devices
    return _main_devices.remote_actor(t)


def device_list():
    global _main_devices
    return _main_devices.device_list


def switch(t, on_command="on", off_command="off", set_topic="set",
           state_topic="", init_state=None):
    global _main_devices
    return _main_devices.remote_switch(t, on_command, off_command, set_topic,
                                       state_topic, init_state)

led = switch
relay = switch


def init(mqtt_host):
    """
    Just init one mqtt connection and its devices.
    :param mqtt_host:
    :return:
    """
    global _main_devices
    _main_devices = thingconnector.ThingConnector(mqtt_host)  # TODO: auth+tls


def prefix(p):
    global _main_devices
    _main_devices.topic_prefix = p


def stop():
    global _stopped
    _stopped = True


def process(*args):
    """
    Process one step in workign on mqtt events
    :param args: a list of Thingi-objects (if empty try to use global devices)
    :return:
    """
    global _main_devices

    if len(args) == 0:
        args = [_main_devices]

    for d in args:
        d.client.loop(0.001)


loop = process


def start(*args):
    # TODO: make sure this can work with other ThingConnectors in parallel
    """
    Run until interrupted or quit called from any of the callbacks.

    :param args: a list of Thingi-objects (if empty try to use global devices)
    :return:
    """
    global _main_devices

    if len(args) == 0:
        args = [_main_devices]

    while not _stopped:
        for d in args:
            d.client.loop(0.01)


run = start
