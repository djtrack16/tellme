$(document).ready(function(){
	
	unshare = function(event){
		event.preventDefault();
		var sender = $(this);
		var shared = sender.find('input[name="shared"]');
		$.post(sender.attr('href'), {'shared': shared.val()}, function(data){
			if (data['success']) {
				sender.parents('.share-wrap').animate({opacity:0}, 400);
				sender.parents('.share-wrap').remove();
			}
		});
	};

	var unshare_icon = $('.unshare-icon');
	//hide in the beginning
	unshare_icon.hide();

	unshare_icon.each(function(){
		$(this).click(unshare);
	});

	$('.share-wrap, .friend-name').hover( function() {
		//mouse enter
		$(this).find('.unshare-icon').show();

	}, function() {
		//mouse leave
		$(this).find('.unshare-icon').hide();

	});
});
