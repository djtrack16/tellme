$(document).ready(function(){
	var new_entry_form = $('#new_entry_form');
	var new_entry_title = new_entry_form.find('input[name="title"]'); 
	var error_msg = new_entry_form.find('#share-form-errors');

	submit_new_entry_form = function(){
		$.post(new_entry_form.attr('action'), new_entry_form.serialize(), function(data){
			if (data['success']){
				window.location.replace(data['url']);
			}
		});
	};

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
			error_msg.text('This field is required');
		}
	};

	$('#add_entry_modal #confirm-btn').click(validate_and_submit);
});
