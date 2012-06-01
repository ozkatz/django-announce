# Django-Announce: an Announce.js client for Django.

Announce.js is a node.js + socket.io server used for adding real-time notifications to your existing web application.
This project adds easy Announce.js integration for Django, thus enabling you to easily
add real-time notifications to you exiting Django applications.

Before installing and using the client, make sure you setup Announce.js using [this guide](https://github.com/ozkatz/announce.js/blob/master/README.md "announce.js Installation").


## Installation

* install the client either by cloning this repo, or, if using pip, by using the following command:

    pip install django-annonuce

* add `announce` to `INSTALLED_APPS` in your settings.py file.


## Configuration

* add `'announce.middleware.AnnounceCookieMiddleware'` to your `MIDDLEWARE_CLASSES`settings. right above `SessionMiddleware`. this will take care of setting the authentication cookie.
* in your templates, add `{% load announcetags %}` at the top of the template. inside your `<head>` tag, add `{% announce_js %}`. this will include the proper `<script>` tags for you. place this tag above any js files that use the announce.js client.
* the following optional settings are availabe:
    * `ANNOUNCE_CLIENT_ADDR` - defaults to `'localhost:5500'`. *should probably be changed for production.*
    * `ANNOUNCE_API_ADDR` - defaults to `'localhost:6600'`.
    * `ANNOUNCE_HTTPS` - defaults to `False`. whether or not Announce.js is setup to use SSL.


## Usage

Now, from a view, emit a message to a user:

```python
from announce import AnnounceClient
announce_client = AnnounceClient()

# This is our pseudo view code
def comment_on_blog(request):
    post = Post.objects.get(...)
    # Process stuff, handle forms, do whatever you want.
    announce_client.emit(
        post.author.pk,
        'notifications',
        data={ 'msg' : 'You have a new comment!' }
    )
    # Some other things happening here..
    return render_to_response('blog_post.html', ctx)
```

In your HTML code, add the following JS snippet, to receive this notification on the client's side:

```js
// use .on() to add a listener. you can add as many listeners as you want.
announce.on('notifications', function(data){
    alert(data.msg);
});

// .init() will authenticate against the announce.js server, and open the WebSocket connection.
announce.init();
```

Your client should receive an alert with the notification. the channel name (`notifications`) and the data you send
are completley up to you, so be creative and use it wisely.

If you have more than one channel we want to listen on, we can also chain these calls:

```js
announce.on('notifications', function(data){
    popupNotification(data.msg);

}).on('alerts', function(data)}{
    alert(data.alert_msg);

}).on('something-else', function(data){
    $('#someDiv').html(data.htmlContent);
    
}).init();
```

## License 

(The MIT License)

Copyright (c) 2012 Oz Katz &lt;oz.katz@ripplify.com&gt;

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.