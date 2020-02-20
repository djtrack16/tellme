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

	$('.unshare-icon').each(function(){
		$(this).click(unshare);
	});
});
