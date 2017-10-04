import { call, put, takeEvery, takeLatest } from 'redux-saga/effects'

// worker Saga: will be fired on USER_FETCH_REQUESTED actions
function* fetchUser(action) {
	const _throw = action._throw;
	const fetchPost = yield fetch('/games/throw_dart/',
		{
			method: 'POST',
			body: JSON.stringify({
				game_id: action.clonedState.id,
				..._throw

			}),
			credentials: 'include',
			headers: {
				'Content-Type': 'application/json',
				'Accept': 'application/json'
			}
		}
	).then(function (response) {
		return response.json()
	});
	yield put({type: "WINNER_RESPONSE", response: fetchPost});
}

function* mySaga() {
	console.log('fetching req')

	yield takeEvery("THROW_WINNING_DART", fetchUser);

	console.log('fetching req 2')

}

export default mySaga;
