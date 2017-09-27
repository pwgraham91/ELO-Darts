function getPlayerScore(game, player1) {
	if (game.game_rounds.length === 0) {
		return game.score_to_0
	}

	const currentRound = game.game_rounds[game.game_rounds.length - 1];

	const throws = player1 ? currentRound.player_1_throws : currentRound.player_2_throws;

	let pointsLeft = game.score_to_0;
	var throwScore;
	throws.forEach(function (group) {
		group.forEach(function (_throw) {
			throwScore = _throw.hit_score;
			if (pointsLeft >= throwScore) {
				pointsLeft -= throwScore;
			}
		});
	});
	return pointsLeft;
}

function determineNumThrows(game, player1) {
	if (game.game_rounds.length === 0) {
		return 0
	}
	const currentRound = game.game_rounds[game.game_rounds.length -1];

	const throws = player1 ? currentRound.player_1_throws : currentRound.player_2_throws;

	var numThrows = 0;
	throws.forEach(function (group) {
		numThrows += group.length;
	});
	return numThrows;
}

function determineThrower(game) {
	// has one player closed out?
	if (getPlayerScore(game, true) === 0) {
		if (game.rebuttal && (determineNumThrows(game, true) > determineNumThrows(game, false))) {
			return {player1: false, winnerId: null};
		} else {
			console.log('winner')
			return {player1: null, winnerId: game.in_progress_player_1.id};
		}
	} else if (getPlayerScore(game, false) === 0) {
		if (game.rebuttal && (determineNumThrows(game, true) < determineNumThrows(game, false))) {
			return {player1: true, winnerId: null};
		} else {
			console.log('winnner2')
			return {player1: null, winnerId: game.in_progress_player_2.id};
		}
	}

	const currentRound = game.game_rounds[game.game_rounds.length -1];
	if (game.game_rounds.length === 0) {
		// if the game hasn't started yet
		return {player1: null, winnerId: null};
	}
	const firstThrowPlayer1 = currentRound.first_throw_player_id === game.in_progress_player_1.id;
	if (firstThrowPlayer1) {
		if (determineNumThrows(game, true) === determineNumThrows(game, false)) {
			return {player1: true, winnerId: null};
		} else if (determineNumThrows(game, true) > determineNumThrows(game, false)) {
			if (determineNumThrows(game, true) % 3 === 0) {
				return {player1: false, winnerId: null};
			} else {
				return {player1: true, winnerId: null};
			}
		}
	} else {
		if (determineNumThrows(game, true) === determineNumThrows(game, false)) {
			return {player1: false, winnerId: null};
		} else if (determineNumThrows(game, false) > determineNumThrows(game, true)) {
			if (determineNumThrows(game, false) % 3 === 0) {
				return {player1: true, winnerId: null};
			} else {
				return {player1: false, winnerId: null};
			}
		}
	}
	// todo this return is wrong (found this state returning to the page in mid-game
	return {player1: true, winnerId: null};
}

export default {
	getPlayerScore,
	determineThrower
}