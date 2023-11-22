from fastapi import APIRouter

from .auth import router as auth_router
from .user import router as user_router
from .budget import router as budget_router
from .geolocation import router as geolocation_router
from .auhor import router as author_router
from .genre import router as genre_router
from .book import router as book_router
from .swap import router as swap_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(budget_router)
router.include_router(geolocation_router)
router.include_router(author_router)
router.include_router(genre_router)
router.include_router(book_router)
router.include_router(swap_router)
