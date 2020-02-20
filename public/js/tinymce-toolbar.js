function init_tb(){
	var tb = $('.tellmeSkin .mceToolbar');

	tb.css('margin-top', '-110px');
	tb.animate({'opacity': 1}, 250);

	tb.data('showing', true);

	// hide toolbar
	hide_tb = function(){
		tb.animate({opacity: 0}, 250, function(){ tb.hide(); });
		tb.data('showing', false);
	};

	// show toolbar
	show_tb = function(){
		tb.show();
		tb.animate({opacity: 1}, 250);
		tb.data('showing', true);
	};

	// toolbar hide-show toggle 
	toolbar_toggle = function(){
		if (tb.data('showing')) {
			hide_tb();
		} else {
			show_tb();
		}
	};
}
