from django.conf.urls.defaults import patterns, url

# /share is the base url because of the folder relative to the home folder
# that's why it doesn't show up in the first url
# name parameter may not be necessary, but it may be good design
# see "Naming URL patterns" @ https://docs.djangoproject.com/en/dev/topics/http/urls/#id2
urlpatterns = patterns('share.views',
    url(r'^$', 'sharing', name='share_sharing'),
    url(r'^share_book/$', 'share_book', name='share_book'),
    url(r'^unshare/$', 'unshare', name='share_unshare'),
    url(r'^send_invitation', 'send_invitation', name='send_invitation'),
)
