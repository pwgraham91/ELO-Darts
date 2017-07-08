import React from 'react';
import StartGameForm from './StartGameForm';

class StartGame extends React.Component {
	render() {
		return (
			<div className="start-game">
				<header>
					<h1>
						Start A New Game
					</h1>
				</header>
				<StartGameForm/>
			</div>
		)
	}
};

export default StartGame;
