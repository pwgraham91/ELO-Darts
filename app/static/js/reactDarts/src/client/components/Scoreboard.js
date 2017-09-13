import React from 'react';

import PlayerScore from './PlayerScore';

const Scoreboard = React.createClass({
	render() {
		return (
			<div className="scoreboard" style={{
				flexGrow: 1
			}}>
				<PlayerScore {...this.props} player1={true} />
				<PlayerScore {...this.props} player1={false} />
			</div>
		)
	}
});

export default Scoreboard;
