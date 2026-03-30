from fastapi import HTTPException
from fastapi import APIRouter

from app.database.qdrant import get_or_create_qdrant_client

router = APIRouter()

@router.get("/qdrant/collections")
def get_qdrant_collections() -> dict:
    print("Fetching Qdrant collections...")
    client = get_or_create_qdrant_client()

    if client is None:
        raise HTTPException(
            status_code=500,
            detail="Qdrant is not configured. Set QDRANT_URL and QDRANT_API_KEY.",
        )

    try:
        collections = client.get_collections()
        return collections.model_dump()
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to fetch collections from Qdrant: {exc}",
        ) from exc



