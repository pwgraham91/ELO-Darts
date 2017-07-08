function game(state = [], action) {
	console.log('game reducer')
	return state;
	switch(action.type) {
		case 'INCREMENT_LIKES' :
			console.log("Incrementing Likes!!");
			const i = action.index;
			return [
				...state.slice(0,i), // before the one we are updating
				{...state[i], likes: state[i].likes + 1},
				...state.slice(i + 1), // after the one we are updating
			]
		default:
			return state;
	}
}

export default game;
