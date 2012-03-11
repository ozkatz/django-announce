import datetime
from django.conf import settings
from announce import AnnounceClient

announce_client = AnnounceClient()
announce_cookie_name = 'announceToken'

class AnnounceCookieMiddleware(object):
    """
    call the Announce.js API interface and get a token
    for the currently logged-in user.
    set the token received from the API as a cookie.
    
    Put this before `AuthenticationMiddleware`.
    """
    def get_token(self, request):
        """
        use the HTTP client to get a token from the Announce.js server,
        for the currently logged in user.
        """
        res = announce_client.get_token(request.user.pk)
        return res

    def has_announce_cookie(self, request):
        cookie = request.COOKIES.get(announce_cookie_name)
        if cookie:
            return True
        return False

    def determine_path(self, request):
        # Use the same path as the session cookie.
        return settings.SESSION_COOKIE_PATH

    def determine_domain(self, request):
        # Use the same domain as the session cookie.
        return settings.SESSION_COOKIE_DOMAIN

    def set_announce_cookie(self, request, response):
        cookie_path = self.determine_path(request)
        cookie_domain = self.determine_domain(request)
        announce_cookie_value = self.get_token(request)
        
        # calculate expiry
        cookie_age = datetime.timedelta(seconds=settings.SESSION_COOKIE_AGE)

        utc_date = datetime.datetime.utcnow()
        cookie_date_str = '%a, %d-%b-%Y %H:%M:%S GMT'
        expires = datetime.datetime.strftime(
            utc_date + cookie_age, cookie_date_str
        )

        # Set the cookie. use the same path, domain and expiry
        # as the cookie set for the session.
        response.set_cookie(
            announce_cookie_name,
            announce_cookie_value,
            max_age=settings.SESSION_COOKIE_AGE,
            expires=expires,
            path=cookie_path,
            domain=cookie_domain
        )
        return response

    def process_response(self, request, response):
        # We only use it for authenticated users
        if not hasattr(request, 'user'):
            return response
            
        if not request.user.is_authenticated() and \
        announce_cookie_name in request.COOKIES:
            # If there is no authenticated user attached to this request,
            # but the announce.js token cookie is still present, delete it.
            # This is usually called on logout.
            path = self.determine_path(request)
            domain = self.determine_domain(request)
            response.delete_cookie(
                announce_cookie_name, path=path, domain=domain
            )
            return response
        
        # skip unauthenticated users
        if not request.user.is_authenticated():
            return response

        # Check if we have the cookie already set:
        if self.has_announce_cookie(request):
            return response

        # If not, set it.
        self.set_announce_cookie(request, response)
        return response
