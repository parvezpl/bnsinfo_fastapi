from fastapi import APIRouter, HTTPException, Query

from app.database.qdrant import get_or_create_qdrant_client
from app.services.embedding import get_embedding

router = APIRouter()

@router.get("/qdrant/search")
def get_qdrant_search(
    q: str = Query(..., min_length=1, description="Search query text"),
    limit: int = Query(5, ge=1, le=50, description="Number of results to return"),
    collection: str = Query(
        "new_bns_hindi_vectors", min_length=1, description="Qdrant collection name"
    ),
) -> dict:
    client = get_or_create_qdrant_client()
    if client is None:
        raise HTTPException(
            status_code=500,
            detail="Qdrant is not configured. Set QDRANT_URL and QDRANT_API_KEY.",
        )

    try:
        query_vector = get_embedding(q)

        results = client.query_points(
            collection_name=collection,
            query=query_vector,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )

        return {"results": [r.model_dump() for r in results.points]}

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to fetch search results from Qdrant: {exc}",
        ) from exc



