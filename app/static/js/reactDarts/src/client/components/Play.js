import React from 'react';

import ThrowOneModal from './ThrowOneModal';
import Scoreboard from './Scoreboard';
import Dartboard from './Dartboard';

const Play = React.createClass({
	throwOneOrPlayRender() {
		if (this.props.game.winner_id) {
			<h1>Game over</h1>
		}
		if (this.props.game.game_rounds.length === 0 || !this.props.game.game_rounds[this.props.game.game_rounds.length - 1].first_throw_player_id || this.props.game.game_rounds[this.props.game.game_rounds.length - 1].round_winner_id) {
			return (
				<ThrowOneModal {...this.props} />
			)
		} else {
			return (
				<div style={{
					display: 'flex'
				}}>
					<Scoreboard {...this.props} />
					<Dartboard {...this.props} />
				</div>
			)
		}
	},

	render() {
		return (
			<div className="game-container">
				{this.throwOneOrPlayRender()}
			</div>
		)
	}
});

export default Play;
