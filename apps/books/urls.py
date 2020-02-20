from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('books.views',

	# The book views - edit, view, delete, add
    url(r'^book/add/$', 'add_book', name='books_add_book'),
    url(r'^book/edit/(?P<book_id>[\d]+)/$', 'edit_entry', name='books_book_edit'),
    url(r'^book/view/(?P<book_id>[\d]+)/$', 'view_entry', name='books_book_view'),
    url(r'^book/delete/$', 'delete_book', name='books_book_delete'),

    # The entry view - edit, view, delete, add
    url(r'^entry/add/$', 'add_entry', name='books_add_entry'),
    url(r'^entry/edit/(?P<entry_id>[\d]+)(-[\w\d-]*)?$', 'edit_entry', name='books_edit_entry'),
    url(r'^entry/view/(?P<entry_id>[\d]+)(-[\w\d-]*)?$', 'view_entry', name='books_view_entry'),
    url(r'^entry/delete/$', 'delete', name='books_delete'),


    # edit entry name or book name
    url(r'^entry/model-title/$', 'edit_model_title', name="edit_model_title")

)
