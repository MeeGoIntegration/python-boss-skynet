#!/usr/bin/python3
class WorkItemCtrl(object):
    """
    Message object for workitems
    Explicitly supports start(), stop() and die()

    A ConfigParser is available in the config attribute of start()
    messages

    """
    def __init__(self, msg):
        self.message = msg

    def start(self):
        return self.message == "start"

    def stop(self):
        return self.message == "stop"

    def die(self):
        return self.message == "die"

    def __repr__(self):
        return f"ctrl: {self.message}"


class ParticipantCtrl:
    """
    Message object for participant control (startup, shutdown)
    """
    pass
