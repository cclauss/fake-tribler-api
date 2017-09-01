import json

import time
from twisted.web import resource


class DebugEndpoint(resource.Resource):

    def __init__(self):
        resource.Resource.__init__(self)
        self.putChild("open_files", DebugOpenFilesEndpoint())
        self.putChild("open_sockets", DebugOpenSocketsEndpoint())
        self.putChild("threads", DebugThreadsEndpoint())
        self.putChild("cpu_history", DebugCPUHistoryEndpoint())
        self.putChild("memory_history", DebugMemoryHistoryEndpoint())


class DebugOpenFilesEndpoint(resource.Resource):

    def render_GET(self, request):
        return json.dumps({"open_files": [{"path": "a/b/c.log", "fd": 3}, {"path": "d/e/f.txt", "fd": 4}]})


class DebugOpenSocketsEndpoint(resource.Resource):

    def render_GET(self, request):
        return json.dumps({"open_sockets": [
            {"family": 2, "status": "ESTABLISHED", "laddr": "0.0.0.0:0", "raddr": "0.0.0.0:0", "type": 30},
            {"family": 2, "status": "OPEN", "laddr": "127.0.0.1:1234", "raddr": "134.233.89.7:3849", "type": 30}
        ]})


class DebugThreadsEndpoint(resource.Resource):

    def render_GET(self, request):
        return json.dumps({"threads": [
            {"thread_id": 12345, "thread_name": "fancy_thread", "frames": ['line 1', 'line 2']},
            {"thread_id": 5653, "thread_name": "another_thread", "frames": ['line 1']},
            {"thread_id": 8784, "thread_name": "twisted", "frames": ['line 1', 'line 2']}]})


class DebugCPUHistoryEndpoint(resource.Resource):

    def render_GET(self, request):
        now = time.time()
        return json.dumps({"cpu_history": [
            {"time": now, "cpu": 5.3},
            {"time": now + 5, "cpu": 10.5},
            {"time": now + 10, "cpu": 50},
            {"time": now + 15, "cpu": 57},
            {"time": now + 20, "cpu": 40},
            {"time": now + 25, "cpu": 30},
            {"time": now + 30, "cpu": 34}]})


class DebugMemoryHistoryEndpoint(resource.Resource):

    def render_GET(self, request):
        now = time.time()
        return json.dumps({"memory_history": [
            {"time": now, "mem": 5000},
            {"time": now + 5, "mem": 5100},
            {"time": now + 10, "mem": 5150},
            {"time": now + 15, "mem": 5125},
            {"time": now + 20, "mem": 5175},
            {"time": now + 25, "mem": 5100},
            {"time": now + 30, "mem": 5150}]})
