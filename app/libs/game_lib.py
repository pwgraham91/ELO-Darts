import datetime
import sqlalchemy as sqla
from sqlalchemy import orm

import config
from app.models import User, Game, Round, Throw


def decay_users():
    """ reduce non-playing users elo scores by 10% every 2 weeks
        redistribute elo scores to users who play
    """
    engine = sqla.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
    Session = orm.sessionmaker(bind=engine)
    session = Session()

    print 'starting user decay'

    tax_rate = 10.0
    elo_tax_fund = 0

    playing_users = session.query(User).join(
        Game,
        sqla.or_(
            User.id == Game.winner_id,
            User.id == Game.loser_id
        )
    ).filter(
        Game.deleted_at.is_(False),
        Game.created_at >= datetime.datetime.utcnow() - datetime.timedelta(days=14)
    )

    non_playing_users = session.query(User).filter(
        User.id.notin_([user_.id for user_ in playing_users])
    )

    for user in non_playing_users:
        current_user_elo = user.elo
        taxed_elo = current_user_elo * (1 / tax_rate)
        user.elo = current_user_elo - taxed_elo
        session.add(user)

        elo_tax_fund += taxed_elo

    num_playing_users = playing_users.count()
    elo_distribution = elo_tax_fund /num_playing_users

    for user in playing_users:
        current_user_elo = user.elo
        user.elo = current_user_elo + elo_distribution
        session.add(user)

    session.commit()

    print 'ending user decay'


def calc_user_current_average(session, user_id, game_id, add_score=None):
    if game_id:
        user_current_winning_game_elo_scores = session.query(sqla.func.array_agg(Game.winner_elo_score)).filter(
            Game.id <= game_id,
            Game.winner_id == user_id
        ).all()
        user_current_loser_game_elo_scores = session.query(sqla.func.array_agg(Game.loser_elo_score)).filter(
            Game.id <= game_id,
            Game.loser_id == user_id
        ).all()

        # [0][0] to access the nested array of values. if no scores, it will return None so instead set to empty list
        winner_score_values = user_current_winning_game_elo_scores[0][0] or []
        loser_score_values = user_current_loser_game_elo_scores[0][0] or []
    else:
        winner_score_values = []
        loser_score_values = []

    combined_scores = winner_score_values + loser_score_values
    if add_score:
        combined_scores += add_score
    return sum(combined_scores) / len(combined_scores)


def get_user_most_recent_game(session, user_id):
    game_id_result = session.query(Game.id).filter(
        sqla.or_(
            Game.winner_id == user_id,
            Game.loser_id == user_id
        )
    ).order_by(Game.id.desc()).first()

    if game_id_result:
        return game_id_result[0]


def group_throws(throws):
    throws_group = []
    throw_round = []

    for counter, throw in enumerate(throws):
        if ((counter + 1) % 3 == 0) and counter != 0:
            throw_round.append(throw.hit_score)
            throws_group.append(throw_round)
            throw_round = []
        else:
            throw_round.append(throw.hit_score)

    if len(throw_round) > 0:
        throws_group.append(throw_round)

    return throws_group


def game_dict(session, game):
    g_dict = {
        'id': game.id,
        'created_at': game.created_at.strftime('%b %d %Y %I:%M%p') if game.created_at else None,
        'deleted_at': game.deleted_at.strftime('%b %d %Y %I:%M%p') if game.deleted_at else None,
        'score_to_0': game.score_to_0,
        'double_out': game.double_out,
        'rebuttal': game.rebuttal,
        'best_of': game.best_of,
        'winner_id': game.winner_id,
        'winner_elo_score': game.winner_elo_score,
        'winner_average_score': game.winner_average_score,
        'loser_id': game.loser_id,
        'loser_elo_score': game.loser_elo_score,
        'loser_average_score': game.loser_average_score,
        'submitted_by_id': game.submitted_by_id,
        'in_progress_player_1': game.in_progress_player_1.dict,
        'in_progress_player_2': game.in_progress_player_2.dict,
    }

    round_objects = session.query(Round).filter(
        Round.game_id == game.id
    ).all()

    rounds = []
    for _round in round_objects:

        round_dict = {
            'id': _round.id,
            'game_id': _round.game_id,
            'first_throw_player_id': _round.first_throw_player_id,
            'in_progress_player_1_id': game.in_progress_player_1_id,
            'in_progress_player_2_id': game.in_progress_player_2_id,
            'round_winner': _round.round_winner
        }

        # get throws and add to round_dict
        player_1_throws = session.query(Throw).filter(
            Throw.round_id == _round.id,
            Throw.player_id == game.in_progress_player_1_id
        ).all()

        round_dict['player_1_throws'] = group_throws(player_1_throws)

        player_2_throws = session.query(Throw).filter(
            Throw.round_id == _round.id,
            Throw.player_id == game.in_progress_player_2_id
        ).all()

        round_dict['player_2_throws'] = group_throws(player_2_throws)

        rounds.append(round_dict)

    g_dict['game_rounds'] = rounds
    return g_dict
