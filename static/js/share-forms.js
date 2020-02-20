$(document).ready(function(){
	reset_form = function(form){
		form.find('#share-form-errors').text('');
		form.find('#share-user').val('');
	};

	hide_form = function(form){
		form.animate({opacity: 0}, 300);
		reset_form(form);
		form.hide();
		form.data('showing', false);
	};

	show_form = function(form){
		form.show();
		form.animate({opacity: 1}, 300);
		form.data('showing', true);
	};

	form_toggle = function(){
		var form = $(this).data('form');
		if (form.data('showing')) {
			hide_form(form);
			$(this).text('Add');
		} else {
			show_form(form);
			$(this).text('Cancel');
		}
	};

	submit_form = function(form, result){
		$.post(form.attr('action'), form.serialize(), function(data){
			if (data['success']==true) {
				result.append(data['result']);
				reset_form(form);
				result.find('.unshare-icon').each(function(){
					$(this).click(unshare);
				});
			} else {
				form.find('#share-form-errors').text(data['error']);
				if (data['is_email']){
					var mail_to = form.find('#share-user').val();
					invite.find('#to_user').text(mail_to);
					invite.find('input[name="invitation_mail_to"]').val(mail_to);
					invite.modal('show');
				}
			}
		});
	};

	unshare = function(event){
		event.preventDefault();
		var sender = $(this);
		var shared = sender.find('input[name="shared"]');
		$.post(sender.attr('href'), {'shared': shared.val()}, function(data){
			if (data['success']) {
				sender.parent().remove();
			}
		});
	};

	initialize = function(sender_selector, form_selector, result_selector){
		var send = $(sender_selector);
		var form = $(form_selector);
		var result = $(result_selector);

		form.data('showing', false);
		send.data('form', form);
		send.data('result', result);

		var form_input = form.find('#share-user');
		form_input.keydown(function(event){
			if (event.which == 13) {
				event.preventDefault();
				submit_form(send.data('form'), send.data('result'));
			}
			if (event.which == 27) {
				hide_form(send.data('form'));
				send.text('Add');
			}
		});
		form_input.typeahead({'source': window.usernames});

		result.find('.unshare-icon').each(function(){
			$(this).click(unshare);
		});

		send.click(form_toggle);
	};

	initialize('#add-book-share',  '#share-book-form',  '#book-shared-friend-list');
	initialize('#add-entry-share', '#share-entry-form', '#entry-shared-friend-list');

	var invite = $('#send_invitation_modal');

	send_invitation = function() {
		post_url = invite.find('input[name="share_send_invitation_url"]').val();
		user_from = invite.find('input[name="invitation_user_from"]').val();
		mail_to = invite.find('input[name="invitation_mail_to"]').val();
		$.post(post_url, {'user_from': user_from, 'mail_to': mail_to}, function(data){});
	}

	$('#send_invitation_modal #confirm-btn').click(send_invitation);
});
