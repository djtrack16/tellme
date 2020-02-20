from django.contrib.auth.models import User
from django.db import models
from books.models import Book, Entry


class Shared(models.Model):
    from_user = models.ForeignKey(User, related_name="share_from_set")
    to_user = models.ForeignKey(User, related_name="share_to_set")
    book = models.ForeignKey(Book, null=True)
    entry = models.ForeignKey(Entry, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def get_share(self):
        # I don't understand this code. If they are sharing a book, why automatically return a shared entry?
        # Why not just return null? Maybe this code works either way, but it's poorly written
        if self.book is not None:
            return self.book
        else:
            return self.entry

    def __unicode__(self):
        # u just tells you that is is a unicode string
        return u'%s' % self.get_share().title
