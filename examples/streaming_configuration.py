import os
import sys
import yaml
from onvif import ONVIFCamera

script_path = os.path.dirname(sys.argv[0])
with open(os.path.join(script_path, "credentials.yaml")) as f:
    credentials = yaml.full_load(f)
    IP = credentials['ip']
    ONVIF_PORT = credentials['onvif_port']
    USER = credentials['user']
    PASS = credentials['password']
WSDL = os.path.join(os.path.dirname(os.path.dirname(__file__)), "wsdl")

"""
A media profile consists of configuration entities such as video/audio
source configuration, video/audio encoder configuration,
or PTZ configuration. This use case describes how to change one
configuration entity which has been already added to the media profile.
"""

# Create the media service
my_cam = ONVIFCamera(IP, ONVIF_PORT, USER, PASS)  # , WSDL)
media_service = my_cam.create_media_service()

profiles = media_service.GetProfiles()

# Use the first profile and Profiles have at least one
token = profiles[0].token

# Get all video encoder configurations
configurations_list = media_service.GetVideoEncoderConfigurations()

# Use the first profile and Profiles have at least one
video_encoder_configuration = configurations_list[0]

# Get video encoder configuration options
options = media_service.GetVideoEncoderConfigurationOptions({'ProfileToken': token})

# Setup stream configuration
video_encoder_configuration.Encoding = 'H264'

# Setup Resolution - does not change anything: 2560x1920
# video_encoder_configuration.Resolution.Width = \
#     options.H264.ResolutionsAvailable[0].Width
# video_encoder_configuration.Resolution.Height = \
#     options.H264.ResolutionsAvailable[0].Height

# Setup Quality from 0 to 1 (0 seems unfeasible too)
video_encoder_configuration.Quality = options.QualityRange.Min

# Setup FrameRate - from 30 to 1
video_encoder_configuration.RateControl.FrameRateLimit = \
    options.H264.FrameRateRange.Min

# Setup EncodingInterval - from 10 to 1
video_encoder_configuration.RateControl.EncodingInterval = \
    options.H264.EncodingIntervalRange.Min

# # Setup Bitrate - options.Extension is None
# video_encoder_configuration.RateControl.BitrateLimit = \
#     options.Extension.H264[0].BitrateRange[0].Min[0]

# Create request type instance
request = media_service.create_type('SetVideoEncoderConfiguration')
request.Configuration = video_encoder_configuration
# ForcePersistence is obsolete and should always be assumed to be True
request.ForcePersistence = True

# Set the video encoder configuration
media_service.SetVideoEncoderConfiguration(request)
