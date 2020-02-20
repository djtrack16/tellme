$(document).ready(function(){
	var jwindow = $(window);
	var header = $("#header");
	var menu = $("#menubar");
	var content = $("#content");
	var editor = $("#editor");
	var editor_wrap = $('#editor-wrap');

	var top_panel = $("#middle-top-panel");
	var top_wrapper = $("#middle-top-panel .hideaway-wrap");
	var left_panel = $("#left-panel");
	var left_wrapper = $("#left-panel .hideaway-wrap");
	var left_wrapper_width = left_wrapper.width();
	var middle_panel = $("#middle-panel");
	var rigth_panel = $("#rigth-panel");
	var rigth_wrapper = $("#rigth-panel .hideaway-wrap");
	var bottom_panel = $('#middle-bottom-panel');
	var bottom_wrapper = $("#middle-bottom-panel .hideaway-wrap");

	resize_content = function() {
		height = jwindow.outerHeight(true) - header.outerHeight(true) - menu.outerHeight(true) - 2;
		if (height > 0) {
			content.height(height);
			left_panel.height(height);
			rigth_panel.height(height);
			middle_panel.height(height);
			editor.height(height - top_wrapper.outerHeight(true) - 60);
			editor_wrap.height(height);
			//console.log('height: ' + height);
		}
	}
	jwindow.resize(resize_content);
	resize_content();

	/* Left panel, hide/show ******************************** */
	left_panel.data('showing', true);
	
	hide_left_panel = function(){
		left_panel.animate({left: -left_wrapper_width}, 300, function(){ left_wrapper.hide(); });
		left_panel.data('showing', false);
		middle_panel.animate({'margin-left': 0}, 300);		
	};
	
	show_left_panel = function(){
		left_panel.animate({left: 0}, 500);
		left_panel.data('showing', true);
		middle_panel.animate({'margin-left': 280}, 500);
		setTimeout(function() { left_wrapper.show(); }, 200);
	};
	
	left_panel_toggle = function(){
		if (left_panel.data('showing')) {
			hide_left_panel();
		} else {
			show_left_panel();
		}
	}; 
	
	$('#left-panel .hide-panel-control').click(left_panel_toggle);

	/* Rigth panel, hide/show ******************************** */
	rigth_panel.data('showing', true);

	hide_rigth_panel = function(){
		rigth_wrapper.animate({opacity:0}, 300, function(){ rigth_wrapper.hide(); });
		rigth_panel.animate({width: 0}, 300);
		rigth_panel.data('showing', false);
		middle_panel.animate({'margin-right': 0}, 300);
	};
	
	show_rigth_panel = function(){
		rigth_panel.animate({width: 280}, 300, function(){ rigth_wrapper.show(); });
		rigth_wrapper.animate({opacity: 1}, 300);
		middle_panel.animate({'margin-right': 280}, 300);
		rigth_panel.data('showing', true);
	};

	rigth_panel_toggle = function(){
		if (rigth_panel.data('showing')) {
			hide_rigth_panel();
		} else {
			show_rigth_panel();
		}
	}; 
	
	$('#rigth-panel .hide-panel-control').click(rigth_panel_toggle);
	
	/* Top panel, hide/show toolbar ************************** */
	top_panel.data('showing', true);

	hide_top_panel = function(){
		top_wrapper.animate({height: 0}, 300, function(){ top_wrapper.hide(); });
		editor.height(editor.height() + 32);
		top_panel.data('showing', false);
	};

	show_top_panel = function(){
		top_wrapper.show();
		top_wrapper.animate({height: 32}, 300);
		editor.animate({height: editor.height() - 32}, 300);
		top_panel.data('showing', true);
	};

	top_panel_toggle = function(){
		if (top_panel.data('showing')) {
			hide_tb();
			setTimeout(hide_top_panel, 250);
		} else {
			show_top_panel();
			setTimeout(show_tb, 300);
		}
	};

	$('#middle-top-panel .hide-panel-control').click(top_panel_toggle);
	
	/* bottom panel, hide/show toolbar ************************** */	
	bottom_panel.data('showing', true);
	
	hide_bottom_panel = function(){
		bottom_wrapper.animate({height: 0}, 300);
		bottom_wrapper.hide();
		bottom_panel.data('showing', false);
	};
	
	show_bottom_panel = function(){
		bottom_wrapper.show();
		bottom_wrapper.animate({height: 220}, 300);
		bottom_panel.data('showing', true);
	};

	botton_panel_toggle = function(){
		if (bottom_panel.data('showing')) {
			hide_bottom_panel();
		} else {
			show_bottom_panel();
		}
	};
	
	$('#middle-bottom-panel .hide-panel-control').click(function(){
		botton_panel_toggle();
	});

	/* *** Default panels status *** */
	hide_rigth_panel();

	$(window).resize(function(){
		resize_content();
	});
});
