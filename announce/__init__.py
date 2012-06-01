import httplib
import socket
from django.conf import settings
from django.utils import simplejson as json

__version__ = '0.1.5'
VERSION = map(int, __version__.split('.'))

class AnnounceClient(object):
    """
    A really basic HTTP client to the Announce.js internal interface.
    It is intended for use with django, but could easily be adapted
    for general use (or maybe for another python web framework)
    """
    def __init__(self):
        self.base_url = getattr(settings, 'ANNOUNCE_API_ADDR', 'localhost:6600')

    def _do_request(self, method, path, *args, **kwargs):
        # A generic wrapper around httplib.
        # I initally wanted to use @kennethreitz's awesome Requests
        # (python-requests.org) but didn't want to intoduce more dependencies.
        try:
            con = httplib.HTTPConnection(self.base_url)
            con.request(method, path, *args, **kwargs)
            return con.getresponse()
        except (httplib.HTTPException, socket.error):
            return None

    def get_token(self, user_id):
        """
        For a given user ID, return a token. Keep in mind that this ID
        could be anything that uniquley describes a user in the system.
        A primary key from the users table is a good fit, but so is
        a session ID, as long as it is unique.
        """
        path = '/auth/token/%s' % (user_id)
        response = self._do_request('POST', path)
        if not response or response.status > 399:
            return None
        try:
            resp = json.loads(response.read())
        except ValueError:
            return None
        if resp:
            if 'token' in resp:
                return '%s|%s' % (user_id, resp['token'])
        return None

    def register_group(self, user_id, group_name):
        """
        Add a user ID (read about what a user ID is under get_token())
        to a given group name. Groups are created on the fly when adding
        the first user. This group could be anything you want it to be,
        no rules here. Map a set of users to a logical name.
        """
        path = '/auth/group/%s/%s' % (group_name, user_id)
        response = self._do_request('POST', path)
        response.read()

    def unregister_group(self, user_id, group_name):
        """
        Remove a user from group.
        """
        path = '/auth/group/%s/%s' % (group_name, user_id)
        response = self._do_request('DELETE', path)
        response.read()


    def emit(self, user_id, channel, data):
        """
        send a message over the given channel to the specified user.
        `data` should be a regular python dict, or any other object
        that is json.dumps'able.
        """
        path = '/emit/user/%s/%s' % (user_id, channel)
        headers = {'Content-Type' : 'application/json'}
        data = json.dumps(data)
        response = self._do_request('POST', path, data, headers)
        response.read()

    def broadcast_group(self, group_name, channel, data):
        """
        Emitts the message over the specified channel to all members
        of the group.
        """
        path = '/emit/group/%s/%s' % (group_name, channel)
        headers = {'Content-Type' : 'application/json'}
        data = json.dumps(data)
        response = self._do_request('POST', path, data, headers)
        response.read()

    def broadcast_room(self, channel, data):
        """
        Emitts the message over the specified channel to all members
        of the group.
        """
        path = '/emit/room/%s' % (channel)
        headers = {'Content-Type' : 'application/json'}
        data = json.dumps(data)
        response = self._do_request('POST', path, data, headers)
        response.read()

    def broadcast(self, channel, data):
        """
        Emit the given message to all connected users.
        """
        path = '/emit/broadcast/%s' % (channel)
        headers = {'Content-Type' : 'application/json'}
        data = json.dumps(data)
        response = self._do_request('POST', path, data, headers)
        response.read()

    def get_room_status(self, channel):
        """
        Return information about the current status of a room.
        (most importanly, members currently online in that room).
        """
        path = '/status/room/%s' % (channel)
        response = self._do_request('GET', path)
        data = response.read()
        try:
            return json.loads(data)
        except ValueError:
            return None

