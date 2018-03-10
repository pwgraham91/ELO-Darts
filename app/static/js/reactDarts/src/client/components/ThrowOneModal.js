import React from 'react';

const ThrowOneModal = React.createClass({
	render() {
		return (
			<div className="modal is-active">
				<div className="modal-background"></div>
				<div className="modal-card">
					<header className="modal-card-head">
						<p className="modal-card-title">Who Goes First?</p>
						<button className="delete" id="modal-delete"></button>
					</header>
					<footer className="modal-card-foot">
						<a className="button is-primary is-medium" onClick={() => this.props.throwOne(this.props.game.in_progress_player_1.id)} >{this.props.game.in_progress_player_1.name}</a>
						<a className="button is-medium" onClick={() => this.props.throwOne(this.props.game.in_progress_player_2.id)} >{this.props.game.in_progress_player_2.name}</a>
					</footer>
				</div>
			</div>
		)
	}
});

export default ThrowOneModal;
