console.log('add game')
// this isn't hooked up to anything but it works

$(document).ready(function() {
	$('.modal-button').click(function(event) {
		event.preventDefault();
		$('.modal').addClass('is-active');
	});

	$('#modal-cancel, #modal-delete').click(function(event) {
		event.preventDefault();
		$('.modal').removeClass('is-active');
	});

	$('#add-game').click(function () {
		$.ajax({
			type: "POST",
			url: '/games/add',
			data: JSON.stringify({
				winner_id: $('select.is-success option:selected').val(),
				loser_id: $('select.is-danger option:selected').val()
			}),
			success: function (data) {
				console.log(data);
				$('.modal').removeClass('is-active');
			},
			error: function (data) {
				console.log(data);
				$('.modal').removeClass('is-active');
			},
			contentType: 'application/json'
		});
	});
});
