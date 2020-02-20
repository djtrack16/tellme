from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

""" DateField.auto_now sets the field to now every time the object is saved.
    DateField.auto_now_add sets the field to now when the object is created. """

class Book(models.Model):
    title = models.CharField(_('title'), max_length=256)
    author = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % self.title

    def shared_entries(self, user):
        """
            Returns a list of shared entries with the user
        """
        from share.models import Shared
        try:
            Shared.objects.filter(to_user=user, book=self).get()
            return self.entry_set.all()
        except Shared.DoesNotExist:
            pass
        
        shared_entries = Shared.objects.filter(to_user=user, entry__book=self)
        
        return map(lambda s: s.entry, shared_entries)

    def get_first_entry(self):
        try:
            first_entry = Entry.objects.filter(book=self).order_by('creation_date')[0]
        except IndexError:
            return None
        else:
            return first_entry

    """ Why is get first_entry url the same as the book url? The book should come up with a listing of all 
    of your entries and should not point to any one of them? """
    def get_absolute_url(self):
        first_entry = self.get_first_entry()
        if first_entry:
            return first_entry.get_absolute_url()
        else:
            return reverse('books_book_edit', kwargs={'book_id': self.id})

    def get_absolute_view_url(self):
        first_entry = self.get_first_entry()
        if first_entry:
            return first_entry.get_absolute_view_url()
        else:
            return reverse('books_book_view', kwargs={'book_id': self.id})

    def empty_book(self):
        # Currently will never return 0 because 1 entry is created when you create a book
        return self.entry_set.count() == 0

    def is_book(self):
        return True

    """ Edit the title of a book """
    def set_title(self, newTitle):
        self.title = newTitle
        self.save()


class Entry(models.Model):
    book = models.ForeignKey(Book)
    title = models.CharField(_('title'), max_length=256)
    body = models.TextField(_('body'))
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s: %s' % (self.book.title, self.title)

    @models.permalink
    def get_absolute_url(self):
        """
           Returns the absolute url to edit the entry url
        """
        return ('books.views.edit_entry', [self.id, '-' + slugify(self.title)])

    @models.permalink
    def get_absolute_view_url(self):
        """
           Returns the absolute url to the entry in view mode
        """
        return ('books.views.view_entry', [self.id, '-' + slugify(self.title)])


    @models.permalink
    def set_title(self, newTitle):
        self.title = newTitle
        self.save()


