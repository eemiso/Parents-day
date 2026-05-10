from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
import os
import uuid
from app.core.config import settings
from app.services.video_service import VideoService
import openai

router = APIRouter()

@router.post("/create")
async def create_video(
    files: List[UploadFile] = File(...),
    message: str = Form(...)
):
    # 1. 파일 저장
    saved_paths = []
    for file in files:
        file_ext = os.path.splitext(file.filename)[1]
        file_path = os.path.join(settings.UPLOAD_DIR, f"{uuid.uuid4()}{file_ext}")
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        saved_paths.append(file_path)
    
    # 2. AI 감성 자막 생성
    captions = []
    try:
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        # 사진 개수만큼 자막 생성 요청
        prompt = f"부모님께 드리는 메시지 '{message}'를 바탕으로 사진 {len(saved_paths)}장에 들어갈 짧고 감동적인 자막 {len(saved_paths)}개를 만들어줘. 한 줄씩 출력해줘."
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        captions = response.choices[0].message.content.strip().split('\n')
        # 자막 개수 맞춤
        captions = (captions + ["언제나 사랑합니다"] * len(saved_paths))[:len(saved_paths)]
    except:
        captions = [f"사랑하는 부모님께 {i+1}" for i in range(len(saved_paths))]

    # 3. 영상 생성
    output_filename = f"memory_{uuid.uuid4()}.mp4"
    try:
        # 비동기로 처리하는 것이 좋으나, 우선 동기 방식으로 구현
        video_path = VideoService.create_memory_video(saved_paths, captions, output_filename)
        return {"video_url": f"/uploads/{output_filename}", "captions": captions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
