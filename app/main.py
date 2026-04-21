from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.routes.resume_routes import router as resume_router
from app.core.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "AI-powered Resume Builder backend by RS Education Solution. "
            "Uses Groq LLM via LangChain to generate ATS-optimized resumes."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # ── CORS ───────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Restrict to specific origins in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routers ────────────────────────────────────────────────────────────────
    app.include_router(resume_router)

    # ── Health Check ───────────────────────────────────────────────────────────
    @app.get("/", tags=["Health"], summary="Health check")
    async def root():
        return JSONResponse(
            content={
                "status": "ok",
                "app": settings.APP_NAME,
                "version": settings.APP_VERSION,
                "message": "RS Education Solution Resume Builder API is running.",
            }
        )

    @app.get("/health", tags=["Health"], summary="Detailed health check")
    async def health():
        return JSONResponse(
            content={
                "status": "healthy",
                "groq_model": settings.GROQ_MODEL,
                "debug": settings.DEBUG,
            }
        )

    return app


app = create_application()
