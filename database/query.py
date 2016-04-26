from sqlalchemy.orm import sessionmaker
from common.models_db import Message
from database.config import engine
from sqlalchemy import asc, desc

db_session = sessionmaker()
db_session.configure(bind=engine)
session = db_session()


def add_message(sender_id, receiver_id, text, timestamp, rev):
    message = Message(sender_id, receiver_id, text, timestamp, rev)
    session.add(message)
    session.commit()
    return message.id


def get_last_messages(uid, friend_id, count=10):
    return session.query(Message.id, Message.text, Message.timestamp) \
                  .filter(Message.sender.in_((uid, friend_id))) \
                  .filter(Message.receiver.in_((uid, friend_id))) \
                  .order_by(asc(Message.timestamp)) \
                  .limit(count).all()


def get_new_messages(uid, count=1):
    return session.query(Message.id, Message.text, Message.timestamp) \
                  .filter((Message.receiver == uid) & (Message.rev == 0)) \
                  .limit(count).all()


def get_last_conversations_messages(uid, count):
    # who cares about efficiency
    # DOESNT WORK

    q1 = session.query(Message.id, Message.text, Message.timestamp, Message.rev) \
                       .filter(Message.sender == uid) \
                       .order_by(desc(Message.timestamp)) \
                       .group_by(Message.receiver) \
                       .limit(count).all()


    q2 = session.query(Message.id, Message.text, Message.timestamp, Message.rev) \
                       .filter(Message.receiver == uid) \
                       .order_by(desc(Message.timestamp)) \
                       .group_by(Message.receiver) \
                       .limit(count).all()
    return sorted(q1 + q2, key=lambda v: v.timestamp)[:count]


def get_unread_messages_count(uid):
    return session.query(Message).filter((Message.receiver == uid) & (Message.rev == 0)).count()


def mark_message_as_read(mid):
    session.query(Message).filter(Message.id == mid).update({'rev': 1})
    session.commit()
