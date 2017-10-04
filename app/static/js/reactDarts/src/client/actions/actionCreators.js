export function throwOne(player_id) {
	return {
		type: 'THROW_ONE',
		player_id
	}
}

export function throwDart(score, targetId) {
	return {
		type: 'THROW_DART',
		score,
		targetId
	}
}

export function resetState(response) {
	console.log('resetting state action')
	// todo wire to dispatch
	return {
		type: 'RESET_STATE',
		response
	}
}
