import React from 'react';
import { Router, Route, IndexRoute} from 'react-router';
import { Provider } from 'react-redux';
import { render } from 'react-dom';
import App from './App';
import Play from '../components/Play';
import StartGame from '../components/StartGame';
import store, { history } from './store';
import './index.css';

const router = (
    <Provider store={store}>
        <Router history={history}>
            <Route path="/games/play/start" component={App}>
                <IndexRoute component={StartGame}></IndexRoute>
                <Route path="/games/play/:gameId" component={Play}></Route>
            </Route>
        </Router>
    </Provider>
);

render(router, document.getElementById('main'));
