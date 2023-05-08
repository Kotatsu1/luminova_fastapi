from fastapi import APIRouter
from funcs.get_images import interactive_search
from schemas.search_schemas import Search

router = APIRouter(prefix='/api/images', tags=['search'])

@router.post("/search")
def search(q: Search):
    return {'search': interactive_search(q.query)}
