import React from 'react';

const StartGameForm = React.createClass({
	handleSubmit(e) {
		e.preventDefault();

		var bestOf = this.best_of.value;
		if (bestOf % 2 == 0) {
			// if it's an even number, make it odd by subtracting 1
			bestOf -= 1;
		} else if (bestOf < 1) {
			// if it's 0 or negative, make it 3
			bestOf = 3;
		}

		fetch('/games/start/',
			{
				method: 'POST',
				body: JSON.stringify({
					'score_to_0': this.refs.score_to_0.value,
					'best_of': bestOf,
					'double_out': this.refs.double_out.checked,
					'rebuttal': this.refs.rebuttal.checked,
					'player_2_id': this.refs.player_2_id.value
				}),
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json',
					'Accept': 'application/json'
				}
			}
		).then(function (response) {
			return response.json()
		}).then(function (response) {
			if (response.game_id) {
				window.location.href = '/games/play/' + response.game_id
			} else {
				console.log(response)
			}
		}).catch(function (response) {
			console.log('error!');
			console.log(response);
		});
	},

	renderOpponents(data, index) {
		const id = data[0];
		const username = data[1];
		return (
			<option key={id} value={id}>{username}</option>
		)
	},

	render() {
		return (
			<div className="start-game-form-div">
				<form ref="startGameForm" className="start-game-form" onSubmit={this.handleSubmit}>
					<div className="field">
						<label htmlFor="player_2_id" className="label">Opponent</label>
						<p className="control">
							<span className="select">
								<select ref="player_2_id" name="player_2_id" id="player_2_id">
									{window.activeUsers.map(this.renderOpponents)}
								</select>
							</span>
						</p>
					</div>
					<div className="field">
						<label htmlFor="score_to_0" className="label">
							Score
						</label>
						<input className="input" type="number" ref="score_to_0" defaultValue={201} />
					</div>
					<div className="field">
						<label htmlFor="best_of" className="label">Best Of</label>
						<input className="input" type="number" ref="best_of" defaultValue={3} />
					</div>
					<div className="field">
						<p className="control">
						<label htmlFor="double_out" className="checkbox">
							<input className="checkbox" type="checkbox" ref="double_out" defaultChecked={false}/>
							Double Out
						</label>
						</p>
					</div>
					<div className="field">
						<p className="control">
							<label htmlFor="rebuttal" className="checkbox">
								<input className="checkbox" type="checkbox" ref="rebuttal" defaultChecked={true}/>
								Rebuttal
							</label>
						</p>
					</div>
					<div className="field">
						<button className="button is-primary" type="submit">Submit</button>
					</div>
				</form>
			</div>
		)
	}
});

export default StartGameForm;
