from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from database import Base


class Note(Base):
    """笔记"""
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)          # 科目
    chapter = Column(String, default="")           # 章节
    title = Column(String, nullable=False)
    content = Column(Text, default="")             # Markdown内容
    tags = Column(String, default="")              # 逗号分隔标签
    is_pinned = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class WrongQuestion(Base):
    """错题本"""
    __tablename__ = "wrong_questions"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    chapter = Column(String, default="")
    question_text = Column(Text, default="")       # 题目文本
    question_image = Column(Text, default="")      # 题目图片base64
    my_answer = Column(Text, default="")           # 我的答案
    correct_answer = Column(Text, default="")      # 正确答案
    ai_analysis = Column(Text, default="")         # AI解析
    difficulty = Column(Integer, default=3)        # 难度1-5
    mastered = Column(Boolean, default=False)      # 是否已掌握
    review_count = Column(Integer, default=0)      # 复习次数
    created_at = Column(DateTime, server_default=func.now())


class StudySession(Base):
    """学习记录（番茄钟）"""
    __tablename__ = "study_sessions"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String)
    duration_min = Column(Integer)                 # 学习时长（分钟）
    session_type = Column(String, default="pomodoro")  # pomodoro/free
    created_at = Column(DateTime, server_default=func.now())


class StudyProgress(Base):
    """学习进度 - 按科目章节追踪"""
    __tablename__ = "study_progress"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    chapter = Column(String)
    section = Column(String, default="")
    status = Column(String, default="not_started")  # not_started/in_progress/completed
    score = Column(Float, default=0)                 # 掌握程度 0-100
    notes_count = Column(Integer, default=0)
    wrong_count = Column(Integer, default=0)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Message(Base):
    """留言板"""
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    author = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class ChatHistory(Base):
    """AI对话历史"""
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, default="general")
    title = Column(String, default="")
    messages = Column(Text, default="[]")          # JSON存储
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
