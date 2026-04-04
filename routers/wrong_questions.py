"""错题本 - 收集错题、AI分析、复习追踪"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models

router = APIRouter(prefix="/api/wrong", tags=["错题本"])


class WrongCreate(BaseModel):
    subject: str
    chapter: str = ""
    question_text: str = ""
    question_image: str = ""
    my_answer: str = ""
    correct_answer: str = ""
    ai_analysis: str = ""
    difficulty: int = 3


class WrongUpdate(BaseModel):
    mastered: Optional[bool] = None
    my_answer: Optional[str] = None
    correct_answer: Optional[str] = None
    ai_analysis: Optional[str] = None
    review_count: Optional[int] = None


@router.get("/")
def list_wrong(subject: str = "", mastered: str = "", db: Session = Depends(get_db)):
    q = db.query(models.WrongQuestion)
    if subject:
        q = q.filter(models.WrongQuestion.subject == subject)
    if mastered == "true":
        q = q.filter(models.WrongQuestion.mastered == True)
    elif mastered == "false":
        q = q.filter(models.WrongQuestion.mastered == False)
    items = q.order_by(models.WrongQuestion.created_at.desc()).all()
    return [{
        "id": w.id, "subject": w.subject, "chapter": w.chapter,
        "question_text": w.question_text,
        "question_image": w.question_image[:100] + "..." if len(w.question_image) > 100 else w.question_image,
        "has_image": bool(w.question_image),
        "my_answer": w.my_answer, "correct_answer": w.correct_answer,
        "ai_analysis": w.ai_analysis, "difficulty": w.difficulty,
        "mastered": w.mastered, "review_count": w.review_count,
        "created_at": str(w.created_at),
    } for w in items]


@router.get("/{item_id}")
def get_wrong(item_id: int, db: Session = Depends(get_db)):
    w = db.query(models.WrongQuestion).filter(models.WrongQuestion.id == item_id).first()
    if not w:
        raise HTTPException(404, "错题不存在")
    return {
        "id": w.id, "subject": w.subject, "chapter": w.chapter,
        "question_text": w.question_text, "question_image": w.question_image,
        "my_answer": w.my_answer, "correct_answer": w.correct_answer,
        "ai_analysis": w.ai_analysis, "difficulty": w.difficulty,
        "mastered": w.mastered, "review_count": w.review_count,
    }


@router.post("/")
def create_wrong(item: WrongCreate, db: Session = Depends(get_db)):
    w = models.WrongQuestion(**item.dict())
    db.add(w)
    db.commit()
    db.refresh(w)
    return {"id": w.id}


@router.put("/{item_id}")
def update_wrong(item_id: int, data: WrongUpdate, db: Session = Depends(get_db)):
    w = db.query(models.WrongQuestion).filter(models.WrongQuestion.id == item_id).first()
    if not w:
        raise HTTPException(404)
    for k, v in data.dict(exclude_none=True).items():
        setattr(w, k, v)
    db.commit()
    return {"ok": True}


@router.delete("/{item_id}")
def delete_wrong(item_id: int, db: Session = Depends(get_db)):
    w = db.query(models.WrongQuestion).filter(models.WrongQuestion.id == item_id).first()
    if w:
        db.delete(w)
        db.commit()
    return {"ok": True}


@router.get("/stats/summary")
def wrong_stats(db: Session = Depends(get_db)):
    """各科错题统计"""
    from sqlalchemy import func
    results = db.query(
        models.WrongQuestion.subject,
        func.count(models.WrongQuestion.id).label("total"),
        func.sum(models.WrongQuestion.mastered.cast(Integer) if hasattr(models.WrongQuestion.mastered, 'cast') else 0).label("mastered_count"),
    ).group_by(models.WrongQuestion.subject).all()
    return [{
        "subject": r[0],
        "total": r[1],
        "mastered": r[2] or 0,
        "unmastered": r[1] - (r[2] or 0),
    } for r in results]
