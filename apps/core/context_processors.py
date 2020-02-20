from django.contrib.auth.models import User 

def usernames(request):
    return {'USERNAMES': [ user.username for user in User.objects.all()]}
