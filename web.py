from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.internet import reactor

import json
import motor

PAGE_TEMPLATE = '''
<!DOCTYPE html>
<head>
<script type="text/javascript" src="scripts/motor.js"></script>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Robotic Arm Controller</title>
</head>
<html>
<body>
<h1>Robotic Arm Controller</h1>
<br>
<button onclick="myFunction()">Click To Advance State</button>
<br>
<br>
Current Robot State:
<p id="robot_state"></p>
</body>
</html>
'''

START = 'Initial'
STOPPED = 'Stopped'
CW = 'Running clockwise'
CCW = 'Running counter-clockwise'


class HelloResource(Resource):

    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)
    
    def render_GET(self, request):
        request.setHeader("content-type", "text/html")
        return PAGE_TEMPLATE


class MotorResource(Resource):
    isLeaf = True
    robot_state = START

    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)
    
    def advance_robot(self):
  	if self.robot_state == START:
            motor.setup()
            self.robot_state = STOPPED

        elif self.robot_state == STOPPED:
            motor.cw()
            self.robot_state = CW

        elif self.robot_state == CW:
            motor.ccw()
            self.robot_state = CCW

        elif self.robot_state == CCW:
            motor.stop()
            self.robot_state = STOPPED

    def render_GET(self, request):
        return json.dumps({"state": self.robot_state})

    def render_POST(self, request):
        self.advance_robot()
        request.setHeader("content-type", "application/json")
        return json.dumps({"state": self.robot_state})


root = HelloResource()
root.putChild('motor', MotorResource())
root.putChild('scripts', File('./scripts'))
factory = Site(root)
reactor.listenTCP(8181, factory)
reactor.addSystemEventTrigger("before", "shutdown", motor.cleanup)
reactor.run()
