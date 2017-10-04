import funcs from '../handlers';

export function throwOne(player_id) {
	return {
		type: 'THROW_ONE',
		player_id
	}
}

export function throwDart(currentState, score, targetId) {
	var clonedState = Object.assign({}, currentState);

	var points_left_before_throw, throws, player_id;

	var throwerDict = funcs.determineThrower(clonedState);
	var current_thrower_player_1 = throwerDict.player1;

	if (current_thrower_player_1 === true) {
		points_left_before_throw = funcs.getPlayerScore(clonedState, true);
		throws = clonedState.game_rounds[clonedState.game_rounds.length - 1].player_1_throws;
		player_id = clonedState.in_progress_player_1.id;
	} else if (current_thrower_player_1 === false) {
		points_left_before_throw = funcs.getPlayerScore(clonedState, false);
		throws = clonedState.game_rounds[clonedState.game_rounds.length - 1].player_2_throws;
		player_id = clonedState.in_progress_player_2.id;
	} else {
		// no one is throwing
		if (throwerDict.winnerId) {
			console.log(throwerDict.winnerId)
			console.log('should not have thrown that')
			// we should not have been throwing. this should have been handled below
			return {
				type: 'DO_NOTHING'
			}
		}
	}
	var _throw = {
		hit_score: score,
		hit_area: targetId,
		points_left_before_throw,
		player_id
	};

	if (throws.length > 0 && throws[throws.length - 1].length < 3) {
		throws[throws.length - 1].push(_throw);
	} else {
		throws.push([_throw]);
	}

	// check for winner
	throwerDict = funcs.determineThrower(clonedState);

	var loading = false;
	if (throwerDict.winnerId) {
		_throw.round_winner_id = throwerDict.winnerId;
		loading = true;
		clonedState.loading = loading;
		return {
			type: "THROW_WINNING_DART",
			clonedState,
			_throw
		}
	}
	return {
		type: 'THROW_DART',
		clonedState,
		_throw,
	}
}
