from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import model
from constants import PALINDROME_DB_URI


@contextmanager
def connection():
    '''
        Connection provides a scope for performing
        operations on the application's database.
    '''
    engine = create_engine(PALINDROME_DB_URI)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_messages(session):
    messages = session.query(model.Messages)
    if messages:
        messages = messages.order_by(model.Messages.created_on)
    return messages.all()


def get_message(session, message_id):
    return session.query(model.Messages).filter(
        model.Messages.id == message_id
    ).first()


def add_message(session, msg, username, is_palindrome):
    message = model.Messages(
        message=msg,
        username=username,
        is_palindrome=is_palindrome
    )
    session.add(message)
    session.flush()

    return message


def delete_message(session, message_id):
    message = session.query(model.Messages).filter(
        model.Messages.id == message_id
    ).first()
    if message:
        session.delete(message)
        session.flush()
    return message
