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
			const clonedState = action.clonedState;
			const _throw = action._throw;
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

			return action.clonedState;

		case 'WINNER_RESPONSE':
			// reset state to response from server
			return action.response;

		case 'UNDO_THROW_DART':
			// todo undo state and send request to undo last dart from this game
			return state;
		default:
			return state;
	}
}

export default game;
