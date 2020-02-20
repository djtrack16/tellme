from django import forms
from django.utils.translation import ugettext_lazy as _
from messages.models import Entry

class NewMessageForm(forms.Form):
    title = forms.CharField(label=_('Book Title'), max_length=256)
    first_entry = forms.CharField(label=_('First Entry Title'), max_length=256)

class EntryEditForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('body', )

class NewEntryForm(forms.Form):
    title = forms.CharField(label=_('Entry Title'), max_length=256)