import cgi
import json

from twisted.web import http, resource

import FakeTriblerAPI.tribler_utils as tribler_utils


class DownloadsEndpoint(resource.Resource):

    def getChild(self, path, request):
        return DownloadEndpoint(path)

    def render_GET(self, request):
        get_peers = False
        if 'get_peers' in request.args and len(request.args['get_peers']) > 0 \
                and request.args['get_peers'][0] == "1":
            get_peers = True

        get_pieces = False
        if 'get_pieces' in request.args and len(request.args['get_pieces']) > 0 \
                and request.args['get_pieces'][0] == "1":
            get_pieces = True

        return json.dumps({"downloads": [download.get_json(get_peers=get_peers, get_pieces=get_pieces)
                                         for download in tribler_utils.tribler_data.downloads]})

    def render_PUT(self, request):
        headers = request.getAllHeaders()
        request_data = cgi.FieldStorage(fp=request.content, headers=headers,
                                        environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': headers['content-type']})

        # Just start a fake download
        tribler_utils.tribler_data.start_random_download()

        return json.dumps({"added": True})


class DownloadEndpoint(resource.Resource):

    def __init__(self, infohash):
        resource.Resource.__init__(self)
        self.infohash = infohash

        self.putChild("files", DownloadFilesEndpoint(self.infohash))

    def render_PATCH(self, request):
        download = tribler_utils.tribler_data.get_download_with_infohash(self.infohash)
        parameters = http.parse_qs(request.content.read(), 1)

        if 'selected_files[]' in parameters:
            selected_files_list = [unicode(f, 'utf-8') for f in parameters['selected_files[]']]
            download.set_selected_files(selected_files_list)

        if 'state' in parameters and len(parameters['state']) > 0:
            state = parameters['state'][0]
            if state == "resume":
                download.status = 3
            elif state == "stop":
                download.status = 5
            elif state == "recheck":
                download.status = 2
            else:
                request.setResponseCode(http.BAD_REQUEST)
                return json.dumps({"error": "unknown state parameter"})

        return json.dumps({"modified": True})


class DownloadFilesEndpoint(resource.Resource):

    def __init__(self, infohash):
        resource.Resource.__init__(self)
        self.infohash = infohash

    def render_GET(self, request):
        download = tribler_utils.tribler_data.get_download_with_infohash(self.infohash)
        return json.dumps({"files": download.files})
