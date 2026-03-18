from fastapi import APIRouter, HTTPException
from app.security_data import get_all_chapters, get_chapter_by_id, get_chapter_list

router = APIRouter(prefix="/api/security", tags=["security"])


@router.get("/chapters")
def list_chapters():
    """Return lightweight chapter listing (no full content)."""
    return get_chapter_list()


@router.get("/chapters/{chapter_id}")
def get_chapter(chapter_id: str):
    """Return full chapter content including sections and challenges."""
    chapter = get_chapter_by_id(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail=f"Chapter '{chapter_id}' not found")
    return chapter


@router.get("/chapters/{chapter_id}/challenges")
def get_challenges(chapter_id: str):
    """Return only the challenges for a chapter."""
    chapter = get_chapter_by_id(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail=f"Chapter '{chapter_id}' not found")
    return chapter.get("challenges", [])
