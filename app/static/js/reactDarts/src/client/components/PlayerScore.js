import React from 'react';

import getPlayerScore from '../handlers';

const PlayerScore = React.createClass({
	render() {
		return (
			<div className="player-score" style={{
				display: 'flex',
				justifyContent: 'space-between'
			}}>
				<p>{this.props.player1 ? this.props.game.in_progress_player_1.name : this.props.game.in_progress_player_2.name }</p>
				<p>{getPlayerScore(this.props.game, this.props.player1)}</p>
			</div>
		)
	}
});

export default PlayerScore;
