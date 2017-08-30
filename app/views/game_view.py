import json

import flask
from flask.ext.login import login_required

from app import app, db
from app.libs.remove_game_lib import remove_game
from app.models import User, Game
from app.views.handlers.game_handler import add_game
from config import slack_token


@app.route('/games/add', methods=['POST'])
@login_required
def add_game_post():
    session = db.session

    data = flask.request.json

    winner_id = data['winner_id']
    winner = session.query(User).get(winner_id)
    if not winner:
        raise Exception('no player with id {}'.format(winner_id))

    loser_id = data['loser_id']
    loser = session.query(User).get(loser_id)
    if not loser:
        raise Exception('no player with id {}'.format(loser_id))

    game = add_game(session, winner, loser, submitted_by_id=flask.g.user.id)

    session.commit()
    return flask.Response(json.dumps({
        'id': game.id,
        'success': True
    }), mimetype=u'application/json')


@app.route('/games/slack-game', methods=['POST'])
def add_slack_game_post():
    session = db.session

    data = flask.request.form

    token = data['token']
    if token != slack_token:
        return "You're not who you say you are. Wrong token {}".format(token)

    winner_email, loser_email = data['text'].split(' beat ')
    winner = session.query(User).filter(
        User.email == winner_email,
    ).first()
    loser = session.query(User).filter(
        User.email == loser_email
    ).first()
    if not winner:
        return 'no player with email {}'.format(winner_email)
    if not loser:
        return 'no player with email {}'.format(loser_email)

    add_game(session, winner, loser, slack_user_submitted_by=data['user_name'])

    session.commit()
    return "{} beat {}! {}'s score is now {} and {}'s score is now {}".format(winner.name, loser.name, winner.name,
                                                                              round(winner.elo, 3), loser.name,
                                                                              round(loser.elo, 3))


@app.route('/games/start/', methods=['POST'])
@login_required
def start_game_post():
    session = db.session
    game = Game(
        in_progress_player_1_id=flask.g.user.id,
        in_progress_player_2_id=int(flask.request.json['player_2_id']),
        score_to_0=int(flask.request.json['score_to_0']),
        double_out=flask.request.json['double_out'] == 'on',
        rebuttal=flask.request.json['rebuttal'] == 'on',
        best_of=int(flask.request.json['best_of'])
    )
    session.add(game)
    session.commit()
    return flask.Response(json.dumps({
        'game_id': game.id,
    }), mimetype=u'application/json')


@app.route('/games/play/<string:game_id>')
@login_required
def play_game(game_id):
    """ game id can be 'start' """

    session = db.session
    if game_id == 'start':
        active_users = session.query(User.id, User.name).filter(
            User.active.is_(True)
        ).all()
        return flask.render_template('play_game.html',
                                     title='Cratejoy Darts',
                                     active_users=active_users)
    else:
        game = session.query(Game).get(game_id)
        return flask.render_template('play_game.html',
                                     title='Cratejoy Darts',
                                     game=game)


@app.route('/games/remove/<int:game_id>', methods=['DELETE'])
@login_required
def remove_game_get(game_id):
    session = db.session

    current_user = flask.g.user
    if not current_user.admin:
        return flask.Response(json.dumps({
            'success': False,
            'message': 'Access Denied',
            'affected_player_ids': [],
            'updated_game_ids': []
        }), mimetype=u'application/json')

    game = session.query(Game).get(game_id)
    if not game:
        return flask.Response(json.dumps({
            'success': False,
            'message': 'No Such Game',
            'affected_player_ids': [],
            'updated_game_ids': []
        }), mimetype=u'application/json')

    affected_player_ids, updated_game_ids = remove_game(session, game)

    return flask.Response(json.dumps({
        'affected_player_ids': list(affected_player_ids),
        'updated_game_ids': list(updated_game_ids)
    }), mimetype=u'application/json')
