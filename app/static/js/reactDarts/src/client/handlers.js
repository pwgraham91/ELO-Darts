function getPlayerScore(game, player1) {
	const currentRound = game.game_rounds[game.game_rounds.length -1];

	const throws = player1 ? currentRound.player_1_throws : currentRound.player_2_throws;

	let pointsLeft = game.score_to_0;
	for (group of throws) {
		for (_throw of group) {
			if (pointsLeft >= _throw) {
				pointsLeft -= _throw
			}
		}
	}
	return pointsLeft
}

function determineThrower(game) {
	// true for player 1
	return true
}

export default {
	getPlayerScore,
	determineThrower
}