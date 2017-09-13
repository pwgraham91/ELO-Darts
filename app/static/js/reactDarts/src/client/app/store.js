import { createStore } from 'redux';
import { syncHistoryWithStore } from 'react-router-redux';
import { browserHistory } from 'react-router';

// import the root reducer
import rootReducer from '../reducers/index';

// create an object for the default data
const defaultState = {
	game: window.game || null
};

const store = createStore(rootReducer, defaultState);

export const history = syncHistoryWithStore(browserHistory, store);

if(module.hot) {
	console.log('module hot')
	module.hot.accept('/reducers/',() => {
		const nextRootReducer = require('/reducers/index').default;
		store.replaceReducer(nextRootReducer);
	});
}

export default store;
