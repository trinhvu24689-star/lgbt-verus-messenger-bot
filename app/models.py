# app/models.py
from sqlalchemy import Column, String, DateTime, Text, Enum, JSON, BigInteger, Integer
from .db import Base

class FbUser(Base):
    __tablename__ = "fb_users"
    psid = Column(String(64), primary_key=True)
    first_seen_at = Column(DateTime, nullable=True)
    last_seen_at = Column(DateTime, nullable=True)
    is_active = Column(Integer, nullable=False, default=1)
    note = Column(String(255), nullable=True)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String(64), primary_key=True)
    updated_time = Column(DateTime, nullable=True)

class Message(Base):
    __tablename__ = "messages"
    id = Column(String(64), primary_key=True)
    conversation_id = Column(String(64), nullable=True)
    psid = Column(String(64), nullable=True)
    direction = Column(Enum("in", "out"), nullable=False)
    text = Column(Text, nullable=True)
    created_time = Column(DateTime, nullable=True)
    raw_json = Column(JSON, nullable=True)

class Event(Base):
    __tablename__ = "events"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    psid = Column(String(64), nullable=True)
    type = Column(String(50), nullable=False)
    detail = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)
