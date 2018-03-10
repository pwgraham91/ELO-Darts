import React from 'react';

import funcs from '../handlers';

const PlayerScore = React.createClass({
	renderGroupedThrows() {
		const currentRound = this.props.game.game_rounds[this.props.game.game_rounds.length - 1];
		const throws = this.props.player1 ? currentRound.player_1_throws : currentRound.player_2_throws;
		if (throws.length > 0) {
			const lastThrowGroup = throws[throws.length - 1];
			return lastThrowGroup.map(function (_throw, i) {
				return <div key={ _throw.hit_score + ' ' + i }>{ _throw.hit_score }</div>
			});
		} else {
			return <p>no throws yet</p>
		}
	},

	render() {
		return (
			<div className="player-score" style={{
				display: 'flex',
				justifyContent: 'space-between'
			}}>
				<p>{this.props.player1 ? this.props.game.in_progress_player_1.name : this.props.game.in_progress_player_2.name }</p>
				{ this.renderGroupedThrows() }
				<p>{funcs.getPlayerScore(this.props.game, this.props.player1)}</p>
			</div>
		)
	}
});

export default PlayerScore;
