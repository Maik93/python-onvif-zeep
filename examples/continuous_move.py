import os
import sys
import asyncio
import yaml
from onvif import ONVIFCamera


class Camera:

    def __init__(self):
        script_path = os.path.dirname(sys.argv[0])
        with open(os.path.join(script_path, "credentials.yaml")) as f:
            credentials = yaml.full_load(f)
            self.IP = credentials['ip']
            self.ONVIF_PORT = credentials['onvif_port']
            self.USER = credentials['user']
            self.PASS = credentials['password']
        self.WSDL = os.path.join(script_path, "..", "wsdl")

        self.active = False

        onvif_camera = ONVIFCamera(self.IP, self.ONVIF_PORT, self.USER, self.PASS, self.WSDL)
        self.ptz = onvif_camera.create_ptz_service()
        media = onvif_camera.create_media_service()
        media_profile = media.GetProfiles()[0]

        # Get PTZ configuration options for getting continuous move range
        request = self.ptz.create_type('GetConfigurationOptions')
        request.ConfigurationToken = media_profile.PTZConfiguration.token
        ptz_configuration_options = self.ptz.GetConfigurationOptions(request)

        # Get velocity range of pan and tilt
        self.vx_max = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max / 5
        self.vx_min = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min / 5
        self.vy_max = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max / 10
        self.vy_min = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min / 10
        self.vz_max = ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].XRange.Max / 5
        self.vz_min = ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].XRange.Min / 5

        # Construct request template
        self.base_request = self.ptz.create_type('ContinuousMove')
        self.base_request.ProfileToken = media_profile.token

    def do_move(self, request):
        # Start continuous move
        if self.active:
            self.ptz.Stop({'ProfileToken': request.ProfileToken})
        self.active = True
        self.ptz.ContinuousMove(request)

    def zoom_in(self):
        print('zoom in...')
        request = self.base_request
        self.base_request.Velocity = {'Zoom': {'x': self.vz_max}}
        self.do_move(request)

    def zoom_out(self):
        print('zoom out...')
        request = self.base_request
        self.base_request.Velocity = {'Zoom': {'x': self.vz_min}}
        self.do_move(request)

    def move_up(self):
        print('move up...')
        request = self.base_request
        self.base_request.Velocity = {'PanTilt': {'x': 0, 'y': self.vy_max}}
        self.do_move(request)

    def move_down(self):
        print('move down...')
        request = self.base_request
        self.base_request.Velocity = {'PanTilt': {'x': 0, 'y': self.vy_min}}
        self.do_move(request)

    def move_right(self):
        print('move right...')
        request = self.base_request
        self.base_request.Velocity = {'PanTilt': {'x': self.vx_max, 'y': 0}}
        self.do_move(request)

    def move_left(self):
        print('move left...')
        request = self.base_request
        self.base_request.Velocity = {'PanTilt': {'x': self.vx_min, 'y': 0}}
        self.do_move(request)

    def move_up_left(self):
        print('move up left...')
        request = self.base_request
        self.base_request.Velocity = {'PanTilt': {'x': self.vx_min, 'y': self.vy_max}}
        self.do_move(request)

    def move_up_right(self):
        print('move up left...')
        request = self.base_request
        self.base_request.Velocity = {'PanTilt': {'x': self.vx_max, 'y': self.vy_max}}
        self.do_move(request)

    def move_down_left(self):
        print('move down left...')
        request = self.base_request
        self.base_request.Velocity = {'PanTilt': {'x': self.vx_min, 'y': self.vy_min}}
        self.do_move(request)

    def move_down_right(self):
        print('move down left...')
        request = self.base_request
        self.base_request.Velocity = {'PanTilt': {'x': self.vx_max, 'y': self.vy_min}}
        self.do_move(request)

    def stop(self):
        self.ptz.Stop({'ProfileToken': self.base_request.ProfileToken})
        self.active = False


def read_loop_cycle():
    """ Reading from stdin and displaying menu """

    selection = sys.stdin.readline().strip("\n")
    lov = [x for x in selection.split(" ") if x != ""]
    if lov:
        if lov[0].lower() in ["u", "up"]:
            camera_handler.move_up()
        elif lov[0].lower() in ["d", "do", "dow", "down"]:
            camera_handler.move_down()
        elif lov[0].lower() in ["l", "le", "lef", "left"]:
            camera_handler.move_left()
        elif lov[0].lower() in ["l", "le", "lef", "left"]:
            camera_handler.move_left()
        elif lov[0].lower() in ["r", "ri", "rig", "righ", "right"]:
            camera_handler.move_right()
        elif lov[0].lower() in ["ul"]:
            camera_handler.move_up_left()
        elif lov[0].lower() in ["ur"]:
            camera_handler.move_up_right()
        elif lov[0].lower() in ["dl"]:
            camera_handler.move_down_left()
        elif lov[0].lower() in ["dr"]:
            camera_handler.move_down_right()
        elif lov[0].lower() in ["z"]:
            camera_handler.zoom_in()
        elif lov[0].lower() in ["x"]:
            camera_handler.zoom_out()
        elif lov[0].lower() in ["s", "st", "sto", "stop"]:
            camera_handler.stop()
        else:
            print("What are you asking?\tI only know, 'up','down','left','right', 'ul' (up left), \n" +
                  "'ur' (up right), 'dl' (down left), 'dr' (down right) and 'stop'")

    print("")
    print("Your command: ", end='', flush=True)


if __name__ == '__main__':
    camera_handler = Camera()
    loop = asyncio.get_event_loop()
    try:
        loop.add_reader(sys.stdin, read_loop_cycle)
        print("Use Ctrl-C to quit")
        print("Your command: ", end='', flush=True)
        loop.run_forever()
    except:
        pass
    finally:
        loop.remove_reader(sys.stdin)
        loop.close()
