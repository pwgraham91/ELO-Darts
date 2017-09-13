import React from 'react';
import ThrowOneModal from './ThrowOneModal';

const Play = React.createClass({
	throwOneOrPlayRender() {
		if (this.props.game.game_rounds.length === 0 || !this.props.game.game_rounds[this.props.game.game_rounds.length - 1].first_throw_player_id) {
			return (
				<ThrowOneModal {...this.props} />
			)
		} else {
			return (
				// todo make these their own classes
				<div className="wrapper">
					<div className="scoreboard">Scoreboard</div>
					<div className="dartboard">Dartboard</div>
				</div>
			)
		}
	},

	render() {
		return (
			<div className="game-container" style={
				{
					display: 'flex'
				}
			}>
				{this.throwOneOrPlayRender()}
			</div>
		)
	}
});

export default Play;
