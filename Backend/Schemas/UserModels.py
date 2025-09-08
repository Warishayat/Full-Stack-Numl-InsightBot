from Config.database import Base
from sqlalchemy import Column,Integer,Boolean,String, TIMESTAMP, ForeignKey, text


class AuthenticationModel(Base):

    __tablename__ = "Authentication"
    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=("now()"))



class ConversationModel(Base):
    __tablename__ = "conversation"
    id = Column(Integer,primary_key=True,nullable=False)
    user_id = Column(Integer,ForeignKey("Authentication.id",ondelete="CASCADE"),nullable=False)
    title = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=("now()"))



class MessageModel(Base):
    __tablename__ = "Message"
    id = Column(Integer,primary_key=True,nullable=False)
    conversation_id = Column(Integer,ForeignKey("conversation.id",ondelete='CASCADE'),nullable=False)
    content = Column(String)
    is_user = Column(Boolean,server_default=text("true"))
    created_at = Column(TIMESTAMP(timezone=True),server_default=text("now()"))