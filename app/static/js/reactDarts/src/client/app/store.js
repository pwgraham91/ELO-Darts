import { browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
import { createStore, applyMiddleware } from 'redux';
import createSagaMiddleware from 'redux-saga';

import mySaga from './sagas'
import rootReducer from '../reducers/index';
import funcs from '../handlers';

// create an object for the default data
var game;
if (window.game) {
	game = window.game;
	game.current_thrower_player_1 = funcs.determineThrower(game);
} else {
	game = null;
}
const defaultState = {
	game: window.game || null
};

const sagaMiddleware = createSagaMiddleware();

const store = createStore(rootReducer, defaultState, applyMiddleware(sagaMiddleware));

sagaMiddleware.run(mySaga);

export const history = syncHistoryWithStore(browserHistory, store);

if(module.hot) {
	console.log('module hot')
	module.hot.accept('/reducers/',() => {
		const nextRootReducer = require('/reducers/index').default;
		store.replaceReducer(nextRootReducer);
	});
}

export default store;
