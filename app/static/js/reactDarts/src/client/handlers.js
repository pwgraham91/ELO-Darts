function getPlayerScore(game, player1) {
	const currentRound = game.game_rounds[game.game_rounds.length -1];

	const throws = player1 ? currentRound.player_1_throws : currentRound.player_2_throws;

	let pointsLeft = game.score_to_0;
	var throwScore;
	throws.forEach(function (group) {
		group.forEach(function (_throw) {
			throwScore = _throw.hit_score;
			if (pointsLeft >= throwScore) {
				pointsLeft -= throwScore;
			}
		})
	})
	return pointsLeft;
}

function determineThrower(game) {
	// todo determine this
	// true for player 1
	return true;
}

export default {
	getPlayerScore,
	determineThrower
}