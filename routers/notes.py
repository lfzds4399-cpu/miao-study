"""笔记系统 - 按科目/章节组织笔记"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import models

router = APIRouter(prefix="/api/notes", tags=["笔记"])


class NoteCreate(BaseModel):
    subject: str
    chapter: str = ""
    title: str
    content: str = ""
    tags: str = ""


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    chapter: Optional[str] = None
    tags: Optional[str] = None
    is_pinned: Optional[bool] = None


@router.get("/")
def list_notes(subject: str = "", chapter: str = "", search: str = "", db: Session = Depends(get_db)):
    q = db.query(models.Note)
    if subject:
        q = q.filter(models.Note.subject == subject)
    if chapter:
        q = q.filter(models.Note.chapter == chapter)
    if search:
        q = q.filter(
            (models.Note.title.contains(search)) |
            (models.Note.content.contains(search)) |
            (models.Note.tags.contains(search))
        )
    notes = q.order_by(models.Note.is_pinned.desc(), models.Note.updated_at.desc()).all()
    return [{
        "id": n.id, "subject": n.subject, "chapter": n.chapter,
        "title": n.title, "content": n.content, "tags": n.tags,
        "is_pinned": n.is_pinned,
        "created_at": str(n.created_at), "updated_at": str(n.updated_at),
    } for n in notes]


@router.post("/")
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    n = models.Note(**note.dict())
    db.add(n)
    db.commit()
    db.refresh(n)
    return {"id": n.id, "title": n.title}


@router.put("/{note_id}")
def update_note(note_id: int, data: NoteUpdate, db: Session = Depends(get_db)):
    n = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not n:
        raise HTTPException(404, "笔记不存在")
    for k, v in data.dict(exclude_none=True).items():
        setattr(n, k, v)
    db.commit()
    return {"ok": True}


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    n = db.query(models.Note).filter(models.Note.id == note_id).first()
    if n:
        db.delete(n)
        db.commit()
    return {"ok": True}
