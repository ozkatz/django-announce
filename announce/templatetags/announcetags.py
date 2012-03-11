from django.conf import settings
from django.template import Library
register = Library()

def _determine_base_path():
    client = getattr(settings, 'ANNOUNCE_CLIENT_ADDR', 'localhost:5500')
    secure = getattr(settings, 'ANNOUNCE_HTTPS', False)
    proto = 'http'
    if secure:
        proto = 'https'

    return '%s://%s' % (proto, client)    

@register.simple_tag
def announce_socketio_path():
    return '%s/%s' %(_determine_base_path(), 'socket.io/socket.io.js')

@register.simple_tag
def announce_js_path():
    return '%s/%s' %(_determine_base_path(), 'client/announce.client.js')


@register.simple_tag
def announce_js():
    """
    returns the needed HTML tags for including announce.js and its dependency
    (socket.io) in the client's browser. make sure that `ANNOUNCE_CLIENT_ADDR`
    is in the settings.py file and is reachable from the internet, as
    it will be used as the domain name. if you are using announce.js over
    SSL, be sure to set `ANNOUNCE_HTTPS` to True.
    """
    path = _determine_base_path()
    return """
    <script type="text/javascript" src="%s/socket.io/socket.io.js"></script>
    <script type="text/javascript" src="%s/client/announce.client.js"></script>
    """ % (path, path)