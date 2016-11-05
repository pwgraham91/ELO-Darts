console.log('add game')
// this isn't hooked up to anything but it works

$(document).ready(function() {
	$('#add-game').click(function () {
		$.ajax({
			type: "POST",
			url: '/games/add',
			data: JSON.stringify({
				winner_id: 1,
				loser_id: 2
			}),
			success: function (data) {
				console.log(data)
			},
			error: function (data) {
				console.log(data)
			},
			contentType: 'application/json'
		});
	});
});
