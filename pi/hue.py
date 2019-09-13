import time
from phue import Bridge

BRIDGE_IP = '192.168.2.43'

# 1, 2 Bedroom standing, 3 Study, 4 bedroom lamp
LIGHTS = [4, ]


def main():
    bridge = Bridge(BRIDGE_IP)
    bridge.connect()
    # Get the bridge state (This returns the full dictionary that you can explore)
    bridge.get_api()
    lights = bridge.get_light_objects('id')

    is_on = True
    while True:
        for light_id in LIGHTS:
            print('turning {} {}'.format(light_id, is_on))
            lights[light_id].on = is_on
        is_on = not is_on
        time.sleep(2)


if __name__ == '__main__':
    main()
