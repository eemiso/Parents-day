import os
from moviepy import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip
from app.core.config import settings

class VideoService:
    @staticmethod
    def create_memory_video(image_paths: list, captions: list, output_filename: str):
        clips = []
        duration_per_image = 3  # 각 사진당 3초
        
        for img_path, caption in zip(image_paths, captions):
            # 이미지 클립 생성
            img_clip = ImageClip(img_path).set_duration(duration_per_image)
            
            # 자막 추가 (간단한 구현을 위해 하단 중앙 배치)
            # 주의: ImageMagick이 설치되어 있어야 TextClip 사용 가능
            try:
                txt_clip = TextClip(
                    caption, 
                    fontsize=50, 
                    color='white', 
                    font='Arial', 
                    method='caption', 
                    size=(img_clip.w*0.8, None)
                ).set_duration(duration_per_image).set_position(('center', 'bottom'))
                
                video_clip = CompositeVideoClip([img_clip, txt_clip])
            except:
                # TextClip 실패 시 이미지로만 구성
                video_clip = img_clip
                
            clips.append(video_clip)
        
        final_video = concatenate_videoclips(clips, method="compose")
        output_path = os.path.join(settings.UPLOAD_DIR, output_filename)
        
        # 실제 영상 파일 저장
        final_video.write_videofile(output_path, fps=24, codec="libx264")
        return output_path
