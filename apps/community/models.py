from django.contrib.auth.models import User
from django.db import models


class FriendsList(models.Model):
    user = models.OneToOneField(User, related_name="friend_list")
    friends = models.ManyToManyField(User)

class FriendRequest(models.Model):
    """
    Model to track friend requests
    @param user: is the user making the request
    @param friend: is the friend the user would like to be a friend
    @type user: User
    @type friend: User
    """
    user = models.ForeignKey(User)
    friend = models.OneToOneField(User, related_name="friend_request_friend")
