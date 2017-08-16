console.log('LOADED: user_view.js');

define([
	'jQuery'
], function(
	jquery
) {
	$('.remove-game').click(function (e) {
		$.ajax({
			url: '/games/remove/' + $(e.currentTarget).data('gameId'),
			type: 'DELETE',
			success: function(result) {
				console.log(result)
			}
		});
	});
});
