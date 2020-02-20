$(document).ready(function(){
	var delete_url = $('input[name="delete-url"]').val();
	var sender = null;

	delete_entry = function(sender){
		var entry  = sender.find('input[name="entry"]').val();
		$.post(delete_url, {'entry': entry} , function(data){
			if (data['success']) {
				sender.parents('.entry-title').animate({opacity:0}, 400);
				sender.parents('.entry-title').remove();
				if (window.current_entry == entry || data['empty_book']){
					window.location.replace(data['url']); 
				}
			}
		});
	};

	delete_book = function(){
		book_id = $('#book_delete_confirm_modal input[name="book"]').val();
		delete_url = $('#book_delete_confirm_modal input[name="book_delete_url"]').val(); 
		$.post(delete_url, {'book': book_id}, function(data){
			if (data['success']) {
				window.location.replace(data['url']);
			}
		});
	}
	
	$('#delete_confirm_modal #confirm-btn').click(function(){
		delete_entry(sender);
	});

	$('#book_delete_confirm_modal #confirm-btn').click(delete_book);
	
	$('.delete-icon').click(function(){
		sender = $(this);
	});
});
