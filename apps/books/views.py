from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from core.utils import json_response
from books.models import Book, Entry
from books.forms import NewBookForm, NewEntryForm, EntryEditForm
from django.core.urlresolvers import reverse


@login_required
def add_book(request):
    """ Create a blank book with a one new blank entry """
    if request.method == "POST":
        form = NewBookForm(request.POST)
        if form.is_valid():

            book = Book(title=form.cleaned_data['title'], author=request.user)
            book.save()
            
            entry = Entry(book=book, title=form.cleaned_data['first_entry'])
            entry.save()
            
            return HttpResponseRedirect(entry.get_absolute_url())
    else:
        form = NewBookForm()

    return render(request, 'books/add_book.html', {'form': form})

@login_required
def edit_model_title(request, entry_id=None):
    """ Edit the name of an book or entry, depending which one is passed in"""
    if not request.is_ajax():
        return HttpResponseForbidden()

    #if request.method != 'POST':
     #   return json_response({'success': False, 'error': 'Should be a POST but is not'})

    #Get new title
    #new_title = request.POST.get('new_title', None)

    # If we are editing the book title
    #if book_id:

     #   try:
      #      book = Book.objects.get(id=(int(book_id)))

       #     if book.author != request.user:
       #         return HttpResponseForbidden()
       # except Book.DoesNotExist:
       #     return json_response({'success': False, 'error': 'Book not found'})

       # book.setTitle(new_title)

    #Otherwise we are editing the model title
    #else:
    try:
        entry = Entry.objects.get(id=int(entry_id))

        if entry.book.author != request.user:
            return HttpResponseForbidden()

    except Entry.DoesNotExist:
       return json_response({'success': False, 'error': 'Entry not found'})
            
    # Set new title to current entry title
    entry.setTitle(new_title)

    return json_response({'success': True})


@login_required
def add_entry(request):
    """ Add a new blank entry to the book """
    #Return HttpResponseForbidden here as cleaner code? and elsewhere...
    if not request.is_ajax():
       return HttpResponseForbidden()

    if request.method != 'POST':
        return json_response({'success': False, 'error': 'wrong method'})

    form = NewEntryForm(request.POST)
    if form.is_valid():
        book = Book.objects.get(id=int(request.POST['book_id']))
        entry = Entry(title=form.cleaned_data['title'], book=book)
        entry.save()
        url = entry.get_absolute_url()

        return json_response({'success': True, 'url': url})
    else:
        return json_response({'success': False, 'error': 'missing argument'})


@login_required
def edit_entry(request, book_id=None, entry_id=None, slug=None):
    user = request.user
    
    if entry_id:
        entry = get_object_or_404(Entry, id=entry_id)
        book = entry.book    
    elif book_id:
        entry = None
        book = get_object_or_404(Book, id=book_id)
    else:
        raise Http404

    """ You are not authorized to edit this entry """
    if book.author != user:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = EntryEditForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
    else:
        form = EntryEditForm(instance=entry)

    new_entry_form = NewEntryForm()
    latest_entries = Entry.objects.filter(book__author=user).order_by('-last_update_date')

    """ Update last_update_date for the entry and the associated book, but DateField.auto_now already
        does this for us. Make book's last_update_date time as the most recently modified entry's time """

    # form.save() does automatically update entry's most recent time, or do I need to do entry.save() ?
    entry.book.last_update_date = entry.last_update_date

    return render(request, 'books/edit_entry.html',
                  {'entry': entry,
                   'book': book,
                   'form': form,
                   'new_entry_form': new_entry_form,
                   'latest_entries': latest_entries})


@login_required
def view_entry(request, book_id=None, entry_id=None, slug=None):

    """ If the entry id is nothing, get only the book instead """
    if entry_id:
        entry = get_object_or_404(Entry, id=entry_id)
        book = entry.book
    elif book_id:
        entry = None
        book = get_object_or_404(Book, id=book_id)
    else:
        raise Http404

    #If this entry is not yours (and it has not been shared with you), forbid access
    if entry:
        shared_entries = book.shared_entries(request.user)
        if len(shared_entries) == 0 or not entry in shared_entries:
            return HttpResponseForbidden()
    else:
        shared_entries = None

    return render(request, 'books/view_entry.html',
                  {'entry': entry,
                   'book': book,
                   'shared_entries': shared_entries})


@login_required
def delete(request):
    if not request.is_ajax():
        return HttpResponseForbidden()

    if request.method != 'POST':
        return json_response({'success': False, 'error': 'wrong method'})

    entry = request.POST.get('entry', None)
    if not entry:
        return json_response({'success': False, 'error': 'missing argument'})

    try:
        delete_entry = Entry.objects.get(id=int(entry))
    except Entry.DoesNotExist:
        return json_response({'success': False, 'error': 'entry not found'})
    
    book = delete_entry.book

    # This is not your entry
    if delete_entry.book.author != request.user:
        return HttpResponseForbidden()

    delete_entry.delete()
    url = book.get_absolute_url()

    """ Delete the entry and return to the book, checking if it is empy or not """
    return json_response({'success': True, 'empty_book': book.empty_book(), 'url': url})

@login_required
def delete_book(request):
    if not request.is_ajax():
        return HttpResponseForbidden()

    if request.method != 'POST':
        return json_response({'success': False, 'error': 'wrong method'})

    book = request.POST.get('book', None)
    if not book:
        return json_response({'success': False, 'error': 'missing argument'})

    try:
        delete_book = Book.objects.get(id=int(book))
    except Book.DoesNotExist:
        return json_response({'success': False, 'error': 'book not found'})

    if delete_book.author != request.user:
        return HttpResponseForbidden()

    """ Does it delete every entry also with the book itself? Do we have to do that or 
        Django take care of that for us? """
    delete_book.delete()

    return json_response({'success': True, 'url': reverse('core_home')})
