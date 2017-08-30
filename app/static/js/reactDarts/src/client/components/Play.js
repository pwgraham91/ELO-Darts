import React from 'react';

class Play extends React.Component {
	render() {
		return (
			<header>
				<h1>
					Play
				</h1>
				<a href="#" onClick={this.props.increment.bind(null, 123, 456)}>Click (this is an example of hitting the state)</a>
			</header>
		)
	}
};

export default Play;
