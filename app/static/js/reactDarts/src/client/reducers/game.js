import funcs from '../handlers';

function game(state = [], action) {

	switch(action.type) {
		case 'THROW_ONE':
			var clonedState = Object.assign({}, state);
			clonedState.game_rounds.push({
				game_id: state.id,
				first_throw_player_id: action.player_id,
				player_1_throws: [],
				player_2_throws: []
			});

			fetch('/games/throw_one/',
				{
					method: 'POST',
					body: JSON.stringify(state),
					credentials: 'include',
					headers: {
						'Content-Type': 'application/json',
						'Accept': 'application/json'
					}
				}
			);

			return clonedState;
		case 'THROW_DART':
			// figure out who threw the dart and log it and post it
			var clonedState = Object.assign({}, state);
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
					return state;
				}
			}
			var _throw = {
				hit_score: action.score,
				hit_area: action.targetId,
				points_left_before_throw,
				player_id
			};

			if (throws.length > 0 && throws[throws.length - 1].length < 3) {
				throws[throws.length - 1].push(_throw);
			} else {
				throws.push([_throw]);
			}

			// check for winner
			var throwerDict = funcs.determineThrower(clonedState);

			if (throwerDict.winnerId) {
				// todo: pass round winner to the POST
				// todo: start new round or finish game
			}

			fetch('/games/throw_dart/',
				{
					method: 'POST',
					body: JSON.stringify({
						game_id: clonedState.id,
						..._throw

					}),
					credentials: 'include',
					headers: {
						'Content-Type': 'application/json',
						'Accept': 'application/json'
					}
				}
			);

			return clonedState;

		case 'UNDO_THROW_DART':
			// todo undo state and send request to undo last dart from this game
			return state;

		default:
			return state;
	}
}

export default game;
