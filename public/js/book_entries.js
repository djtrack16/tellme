$(document).ready(function(){
	var new_entry_form = $('#new_entry_form');
	var new_entry_title = new_entry_form.find('input[name="title"]'); 
	var error_msg = new_entry_form.find('#share-form-errors');

	submit_new_entry_form = function(){
		$.post(new_entry_form.attr('action'), new_entry_form.serialize(), function(data){
			if (data['success']){
				//Go to the url of the new entry if POST successful
				window.location.replace(data['url']);
			}
		});
	};

	//submit on ENTER key
	new_entry_title.keydown(function(event){
		if (event.which == 13) {
			event.preventDefault();
			validate_and_submit();
		}
	});

	validate_form = function() {
		return (new_entry_title.val().length > 0);
	}

	validate_and_submit = function(){
		if (validate_form()) {
			error_msg.text('');
			submit_new_entry_form();
		} else {
			error_msg.text('You need a title');
		}
	};

	edit_title = function() {
		form = $('#edit-entry-form');
		$(this).parent().find('#edit-entry-form').toggle();
		var err = $('#edit-entry-errors');
		title = $('#edit-entry-form').find('input');
		if (title.val().length() > 0) {
			// set the error message to 0
			form.find('#edit-entry-errors').text('');

			// no need to do an ajax call, just update the page

			$.post(form.attr('action'), form.serialize(), function(data) {
				if (data['success']) {

					window.location.replace(data['url']);
				}
			});


		} else {
			form.find('#edit-entry-errors').text('Did you forget a title?');
		}





	};

	$('#add_entry_modal #confirm-btn').click(validate_and_submit);
	$('.edit-icon').click(edit_title);


	

});
