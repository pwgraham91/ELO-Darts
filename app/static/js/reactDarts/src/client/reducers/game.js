import funcs from '../handlers';

function game(state = [], action) {

	switch(action.type) {
		case 'THROW_ONE':
			var clonedState = Object.assign({}, state);
			clonedState.current_thrower_player_1 = action.player_id === clonedState.in_progress_player_1_id;
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

			if (clonedState.current_thrower_player_1) {
				points_left_before_throw = funcs.getPlayerScore(clonedState, true);
				throws = clonedState.game_rounds[clonedState.game_rounds.length - 1].player_1_throws;
				player_id = clonedState.in_progress_player_1.id;
			} else {
				points_left_before_throw = funcs.getPlayerScore(clonedState, false);
				throws = clonedState.game_rounds[clonedState.game_rounds.length - 1].player_2_throws;
				player_id = clonedState.in_progress_player_2.id;
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

			clonedState.current_thrower_player_1 = funcs.determineThrower(clonedState);

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
			// todo
			return state;

		default:
			return state;
	}
}

export default game;
