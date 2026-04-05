"""留言板"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
import models

router = APIRouter(prefix="/api/messages", tags=["留言板"])


class MessageCreate(BaseModel):
    author: str
    content: str


@router.get("/")
def get_messages(db: Session = Depends(get_db)):
    msgs = db.query(models.Message).order_by(models.Message.created_at.desc()).limit(100).all()
    return [{
        "id": m.id,
        "author": m.author,
        "content": m.content,
        "created_at": str(m.created_at),
    } for m in msgs]


@router.post("/")
def create_message(req: MessageCreate, db: Session = Depends(get_db)):
    msg = models.Message(author=req.author, content=req.content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return {"id": msg.id, "author": msg.author, "content": msg.content, "created_at": str(msg.created_at)}


@router.delete("/{msg_id}")
def delete_message(msg_id: int, db: Session = Depends(get_db)):
    msg = db.query(models.Message).filter(models.Message.id == msg_id).first()
    if msg:
        db.delete(msg)
        db.commit()
    return {"ok": True}
