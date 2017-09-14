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
