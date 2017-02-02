from app.models import User


def get_active_users(session):
    user_objects = session.query(User).filter(
        User.active.is_(True)
    ).order_by(User.name).all()
    return [user.dict for user in user_objects]
