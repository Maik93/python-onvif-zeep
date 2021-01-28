from onvif import ONVIFCamera

if __name__ == '__main__':
    my_cam = ONVIFCamera('192.168.1.10', 8899, 'admin', 'admin')  # , no_cache=True)
    event_service = my_cam.create_events_service()
    print(event_service.GetEventProperties())

    pull_point = my_cam.create_pullpoint_service()
    req = pull_point.create_type('PullMessages')
    req.MessageLimit = 100
    print(pull_point.PullMessages(req))
