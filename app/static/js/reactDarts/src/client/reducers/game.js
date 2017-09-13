function game(state = [], action) {

	switch(action.type) {
		case 'THROW_ONE' :
			const clonedState = Object.assign({}, state);
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
		default:
			return state;
	}
}

export default game;
