from app.models import User


def get_active_users(session):
    return session.query(User).filter(
        User.active.is_(True)
    ).order_by(User.name).all()
