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
			debugger
			// figure out who threw the dart and log it and post it
			var clonedState = Object.assign({}, state);



		default:
			return state;
	}
}

export default game;
