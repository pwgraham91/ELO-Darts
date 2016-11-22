console.log('LOADED: add_game.js')

$(document).ready(function() {
	$('.modal-button').click(function(event) {
		event.preventDefault();
		$('.modal').addClass('is-active');
	});

	var clearModal = function() {
		$('select.select-winner').prop('selectedIndex',0);
		$('select.select-loser').prop('selectedIndex',0);
		$('select option').removeClass('hidden');
		$('.modal').removeClass('is-active');
		$('#add-game').attr('disabled', 'disabled');
	};

	$('#modal-cancel, #modal-delete').click(function(event) {
		event.preventDefault();
		clearModal();
	});

	$('select.select-winner').change(function(event) {
		var val = $('select.select-winner option:selected').val();
		$('select.select-loser option').removeClass('hidden');
		$('select.select-loser option[value="' + val + '"]').addClass('hidden');

		if($('select.select-winner').val() && $('select.select-loser').val()) {
			$('#add-game').removeAttr('disabled', 'disabled');
		}
	});

	$('select.select-loser').change(function(event) {
		var val = $('select.select-loser option:selected').val();
		$('select.select-winner option').removeClass('hidden');
		$('select.select-winner option[value="' + val + '"]').addClass('hidden');

		if($('select.select-winner').val() && $('select.select-loser').val()) {
			$('#add-game').removeAttr('disabled', 'disabled');
		}
	});

	$('#add-game').click(function (e) {
		var $this = jQuery(this);
		$this.attr('disabled', 'disabled');

		$.ajax({
			type: "POST",
			url: '/games/add',
			data: JSON.stringify({
				winner_id: $('select.select-winner option:selected').val(),
				loser_id: $('select.select-loser option:selected').val()
			}),
			success: function (data) {
				console.log(data);

				clearModal();

				window.location.reload();
			},
			error: function (data) {
				console.log(data);

				clearModal();
			},
			contentType: 'application/json'
		});
	});
});
