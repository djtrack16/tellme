from django.conf.urls.defaults import patterns, include, url
from core.forms import BootstrapAuthenticationForm

urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='core_home'),    
    url(r'^login/$', 'django.contrib.auth.views.login', 
        {
            'template_name': 'core/login.html', 
            'authentication_form': BootstrapAuthenticationForm
        }, name='core_login'),
    url(r'^signup/$', 'core.views.signup', name='core_signup'),
    url(r'^logout/$', 'core.views.logout', name='core_logout'),
)