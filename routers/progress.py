"""学习进度 + 番茄钟记录 + 数据统计"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models

router = APIRouter(prefix="/api/progress", tags=["学习进度"])


class ProgressUpdate(BaseModel):
    subject: str
    chapter: str
    section: str = ""
    status: str = "in_progress"
    score: float = 0


class SessionCreate(BaseModel):
    subject: str
    duration_min: int
    session_type: str = "pomodoro"


@router.get("/")
def get_progress(subject: str = "", db: Session = Depends(get_db)):
    q = db.query(models.StudyProgress)
    if subject:
        q = q.filter(models.StudyProgress.subject == subject)
    items = q.order_by(models.StudyProgress.subject, models.StudyProgress.chapter).all()
    return [{
        "id": p.id, "subject": p.subject, "chapter": p.chapter,
        "section": p.section, "status": p.status, "score": p.score,
        "updated_at": str(p.updated_at),
    } for p in items]


@router.post("/update")
def update_progress(data: ProgressUpdate, db: Session = Depends(get_db)):
    p = db.query(models.StudyProgress).filter(
        models.StudyProgress.subject == data.subject,
        models.StudyProgress.chapter == data.chapter,
        models.StudyProgress.section == data.section,
    ).first()
    if p:
        p.status = data.status
        p.score = data.score
    else:
        p = models.StudyProgress(**data.dict())
        db.add(p)
    db.commit()
    return {"ok": True}


@router.post("/session")
def record_session(data: SessionCreate, db: Session = Depends(get_db)):
    s = models.StudySession(**data.dict())
    db.add(s)
    db.commit()
    return {"id": s.id}


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """总体学习统计"""
    # 总学习时长
    total_min = db.query(func.sum(models.StudySession.duration_min)).scalar() or 0
    # 今日学习时长
    from datetime import date
    today = date.today().isoformat()
    today_min = db.query(func.sum(models.StudySession.duration_min)).filter(
        func.date(models.StudySession.created_at) == today
    ).scalar() or 0
    # 笔记数
    notes_count = db.query(func.count(models.Note.id)).scalar() or 0
    # 错题数
    wrong_total = db.query(func.count(models.WrongQuestion.id)).scalar() or 0
    wrong_mastered = db.query(func.count(models.WrongQuestion.id)).filter(
        models.WrongQuestion.mastered == True
    ).scalar() or 0
    # 各科学习时长
    subject_stats = db.query(
        models.StudySession.subject,
        func.sum(models.StudySession.duration_min),
        func.count(models.StudySession.id),
    ).group_by(models.StudySession.subject).all()

    return {
        "total_study_min": total_min,
        "today_study_min": today_min,
        "notes_count": notes_count,
        "wrong_total": wrong_total,
        "wrong_mastered": wrong_mastered,
        "subject_study": [{
            "subject": s[0], "total_min": s[1], "sessions": s[2]
        } for s in subject_stats],
    }


@router.get("/sessions")
def get_sessions(limit: int = 30, db: Session = Depends(get_db)):
    sessions = db.query(models.StudySession).order_by(
        models.StudySession.created_at.desc()
    ).limit(limit).all()
    return [{
        "id": s.id, "subject": s.subject,
        "duration_min": s.duration_min, "session_type": s.session_type,
        "created_at": str(s.created_at),
    } for s in sessions]
