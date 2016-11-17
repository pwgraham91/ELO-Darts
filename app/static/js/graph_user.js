var categories = _.map(window.userGames, function(game) {
	return moment.utc(game.created_at, "MMM DD YYYY HH:mm A").tz(moment.tz.guess() || 'America/Chicago').format("MM/D/YYYY hh:mm A");
});
var userID = window.userID;
var scores = _.map(window.userGames, function (game) {
	if (game.winner_id == userID) {
		return parseFloat(game.winner_elo_score.toFixed(3));
	} else {
		return parseFloat(game.loser_elo_score.toFixed(3));
	}
});

Highcharts.chart('container', {
	chart: {
		type: 'line'
	},
	title: {
		text: 'User Score'
	},
	xAxis: {
		categories: categories
	},
	yAxis: {
		title: {
			text: 'Elo Score'
		}
	},
	plotOptions: {
		line: {
			dataLabels: {
				enabled: true
			}
		}
	},
	series: [{
		name: 'Date of Play',
		data: scores
	}]
});