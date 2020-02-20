$(document).ready(function(){
	var items_count = $('.big-carousel-item').length;
	var carousel_wagon = $('.big-carousel-wagon');

	var visible_area_width = $('.big-carousel-content').width();
	var width_item = $('.big-carousel-item:first-child').width();

	carousel_wagon.data('position', 0);
	carousel_wagon.data('width', width_item * items_count);

	fix_width = function(){
		$('.big-carousel-item').each(function(index){
			$(this).css('width', width_item);
		});
	};

	right = function(){
		if (Math.abs(carousel_wagon.data('position')) + visible_area_width < carousel_wagon.data('width')) {
			var new_position = carousel_wagon.data('position') - width_item;
			carousel_wagon.animate({left: new_position}, 200);
			carousel_wagon.data('position', new_position);
		} else {
			carousel_wagon.animate({left: carousel_wagon.data('position') - 15}, 200);
			carousel_wagon.delay(50).animate({left: carousel_wagon.data('position')}, 200);
		}
	};

	$('.big-carousel-right').click(right);
	
	left = function(){
		if (carousel_wagon.data('position') < 0) {
			var new_position = carousel_wagon.data('position') + width_item;
			carousel_wagon.animate({left: new_position}, 200);
			carousel_wagon.data('position', new_position);
		} else {
			carousel_wagon.animate({left: 15}, 200);
			carousel_wagon.delay(50).animate({left: 0}, 200);
		};
	};

	$('.big-carousel-left').click(left);
	
	fix_width();
});
