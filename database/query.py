from sqlalchemy.orm import sessionmaker
from common.models_db import Message
from database.config import engine
from sqlalchemy import asc, desc, func
from sqlalchemy import and_

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
                  .order_by(asc(Message.id)) \
                  .limit(count).all()


def get_new_messages(uid, count=1):
    return session.query(Message.id, Message.text, Message.timestamp) \
                  .filter((Message.receiver == uid) & (Message.rev == 0)) \
                  .limit(count).all()


def get_last_conversations_messages(uid, count):
    # TODO rewrite this mess

    def select_sender():
        # http://stackoverflow.com/questions/1279356/sqlalchemy-grouping-items-and-iterating-over-the-sub-lists

        max_id_subtable = session.query(Message.receiver, func.max(Message.id).label('max_id')).filter(Message.sender == uid)\
                          .group_by(Message.receiver).order_by(desc(Message.id)).limit(count).subquery()

        result = session.query(Message).filter(Message.sender == uid).join((max_id_subtable,
               and_(Message.receiver == max_id_subtable.c.receiver,
                    Message.id == max_id_subtable.c.max_id)
           )).all()

        return result

    def select_receiver():
        max_id_subtable = session.query(Message.sender, func.max(Message.id).label('max_id')).filter(Message.receiver == uid)\
                          .group_by(Message.sender).order_by(desc(Message.id)).limit(count).subquery()

        result = session.query(Message).filter(Message.receiver == uid).join((max_id_subtable,
               and_(Message.sender == max_id_subtable.c.sender,
                    Message.id == max_id_subtable.c.max_id)
           )).all()

        return result


    q1 = select_sender()
    q2 = select_receiver()

    friends = set()
    result = []
    for m in sorted(q1 + q2, key=lambda v: v.timestamp, reverse=True):
        friend = m.sender if m.receiver == uid else m.receiver
        if friend not in friends:
            result.append(m)
            friends.add(friend)
            if len(result) == count:
                break
    return result


def get_unread_messages_count(uid):
    return session.query(Message).filter((Message.receiver == uid) & (Message.rev == 0)).count()


def mark_message_as_read(mid):
    session.query(Message).filter(Message.id == mid).update({'rev': 1})
    session.commit()
