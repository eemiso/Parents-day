from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.letter import router as letter_router
from app.api.video import router as video_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Thanks To - AI Parents' Day Service")

# 업로드 폴더 생성
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# 정적 파일 서버 설정
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 라우터 등록
app.include_router(letter_router, prefix="/api/v1/letter", tags=["Letter"])
app.include_router(video_router, prefix="/api/v1/video", tags=["Video"])

# CORS 설정 (프론트엔드 통신 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Thanks To AI API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
