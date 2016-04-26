from sqlalchemy import Column, ForeignKey, Integer, DateTime, String, PickleType, \
                       Text, BigInteger, UniqueConstraint, Boolean
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()


class Message(Base):
    __tablename__ = "messages"
    id = Column(BigInteger, primary_key=True)
    sender = Column(BigInteger)
    receiver = Column(BigInteger)
    text = Column(String(1000))
    timestamp = Column(DateTime)
    rev = Column(Boolean)

    def __init__(self, sender, receiver, text, timestamp, rev):
        self.sender = sender
        self.receiver = receiver
        self.text = text
        self.timestamp = timestamp
        self.rev = rev


    def __str__(self):
        return "{id: %s, sender: %s, receiver: %s}" % (self.id, self.sender, self.receiver)
