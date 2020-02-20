from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from core.utils import json_response
from books.models import Book, Entry
from share.models import Shared
import logging


@login_required
def share_book(request):

    if not request.is_ajax():
        return HttpResponseForbidden()

    if request.method != 'POST':
        return json_response({'success': False, 'error': 'wrong method'})
    # Have the hook default value as 'none' if value not found
    # is there a difference between this code and request.user?
    user = request.POST.get('user', None)
    #if not user:
    #    return json_response({'success': False, 'error': 'missing argument'})
    
    book = request.POST.get('book', None)
    entry = request.POST.get('entry', None)
    # I do not believe you can share an entry without sharing the corresponding book
    if not book and not entry and not user:
        return json_response({'success': False, 'error': 'missing argument'})
    
    """ Ask the user for an email or username. If user does not exist, validate email anyway
        and return 404. """
    try:
        shared_user = User.objects.get(Q(username=user)|Q(email=user))
    except User.DoesNotExist:
        try:
            validate_email(user)
        except:
            is_email = False
        else:
            is_email = True

        params = {
            'success': False,
            'error': 'user not found',
            'code': 404,
            'is_email': is_email
        }
        return json_response(params)
    
    if book:
        try:
            shared_book = Book.objects.get(id=int(book))
        except Book.DoesNotExist:
            return json_response({'success': False, 'error': 'book not found'})
        else:
            shared_entry = None
    else:
        try:
            shared_entry = Entry.objects.get(id=int(entry))
        except Entry.DoesNotExist:
            return json_response({'success': False, 'error': 'entry not found'})
        else:
            shared_book = None

    if request.user == shared_user:
        return json_response({'success': False, 'error': "You can't share with yourself!"})
    # If user did not want to share a book, it must have been an entry. 
    #    https://docs.djangoproject.com/en/dev/ref/models/querysets/#get-or-create
    if book:
        shared, created = Shared.objects.get_or_create(from_user=request.user, to_user=shared_user, book=shared_book)
    else:
        shared, created = Shared.objects.get_or_create(from_user=request.user, to_user=shared_user, entry=shared_entry)
    #If the object didn't have to be created, then user is already sharing either (book/entry) with that person.
    if not created:
        return json_response({'success': False, 'error': 'The book/entry is already shared with %s' % shared_user.profile.get_full_name()})

    shared.save()

    result = render_to_string('share/share_list_block.html', {'share': shared})
    data = {'success': True, 'result': result}
    
    return json_response(data)


@login_required
def unshare(request):
    if not request.is_ajax():
        return HttpResponseForbidden()

    if request.method != 'POST':
        return json_response({'success': False, 'error': 'wrong method'})

    shared = request.POST.get('shared', None)
    if not shared:
        return json_response({'success': False, 'error': 'missing argument'})

    try:
        shared_elem = Shared.objects.get(id=int(shared))
    except Shared.DoesNotExist:
        return json_response({'success': False, 'error': 'shared not found'})
    # Does this make sense? If they are both not you, then return a forbidden access?
    # Will only change if it does NOT work
    if shared_elem.from_user != request.user and shared_elem.to_user != request.user:
        return HttpResponseForbidden()

    shared_elem.delete()
    return json_response({'success': True})


@login_required
def send_invitation(request):
    """ If user shares book or entry with someone by email (who is not already using the application),
        they will be invited to use the application. """
    if not request.is_ajax():
        return HttpResponseForbidden()

    if request.method != 'POST':
        return json_response({'success': False, 'error': 'wrong method'})

    mail_to = request.POST.get('mail_to', None)
    user_from = request.POST.get('user_from', None)

    if not mail_to or not user_from:
        return json_response({'success': False, 'error': 'missing argument'}, error=True)

    message = render_to_string('share/share_invitation.html', {'user_from': user_from})
    try:
        send_mail('You are invited to use Nenjah', message, settings.EMAIL_FROM, [mail_to], fail_silently=True)
    except Exception, error:
        logging.exception("not able to send invitation")
        return json_response({'success': False, 'error': error}, error=True)

    return json_response({'success': True})


@login_required
def sharing(request):
    shared_by_me = Shared.objects.filter(from_user=request.user).order_by('book', 'entry') 
    shared_with_me = Shared.objects.filter(to_user=request.user)

    return render(request, 'share/sharing.html', {'shared_by_me': shared_by_me, 'shared_with_me': shared_with_me})
