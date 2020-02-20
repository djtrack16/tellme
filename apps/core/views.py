from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login, authenticate

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.shortcuts import render
from books.models import Book, Entry
from books.forms import NewBookForm
from core.forms import BootstrapUserCreationForm, BootstrapAuthenticationForm

def home(request):
    user = request.user
    if user.is_authenticated():
        books = Book.objects.filter(author=user)
        latest_entries = Entry.objects.filter(book__author=user).order_by('-last_update_date')
        form = NewBookForm()
        return render(request, 'core/home.html', {'books': books, 'latest_entries': latest_entries, 'new_book_form': form})
    else:
        return render(request, 'core/index.html')

def signup(request):
    if request.method == 'POST':
        form = BootstrapUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            # Currently disabled because need a IMAP server to send mail when running locally
            # Works fine on production
            #body = "Write More. Share more. Be more."   
            # Send confirmation email to new user   
            #try:
            #    send_mail('Thanks for signing up!', body, 'djtrack16@gmail.com', [mailto], fail_silently=False)
            #except Exception, error:
            #    logging.exception("Not able to send confirmation email")
            login(request, user)
            return HttpResponseRedirect(reverse('core_home'))
    else:
        form = BootstrapUserCreationForm()
    return render(request, 'core/signup.html', { 'form': form })

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('core_home'))
