import { combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux';

import game from './game';

const rootReducer = combineReducers({game, routing: routerReducer });

export default rootReducer;
