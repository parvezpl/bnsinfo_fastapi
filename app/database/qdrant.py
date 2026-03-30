import logging
import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient

logger = logging.getLogger(__name__)
load_dotenv()

_qdrant_client: QdrantClient | None = None


def get_or_create_qdrant_client() -> QdrantClient | None:
    global _qdrant_client

    if _qdrant_client is not None:
        return _qdrant_client

    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not (qdrant_url and qdrant_api_key):
        return None

    _qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    logger.info("Qdrant client initialized.")
    return _qdrant_client


def initialize_qdrant() -> bool:
    if get_or_create_qdrant_client() is None:
        logger.warning(
            "Qdrant credentials are not set. Configure QDRANT_URL and QDRANT_API_KEY."
        )
        return False

    return True
