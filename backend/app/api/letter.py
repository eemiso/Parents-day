from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LetterRequest(BaseModel):
    user_name: str

@router.post("/generate")
async def generate_letter(request: LetterRequest):
    # 📍 사용자(미소)가 직접 작성한 실제 편지 데이터
    personal_letters = {
        "미소": """TO. 엄마 아빠 
안녕하세요 미소입니다 편지를 굉~~장히 오랜만에 쓰는 것 같네요. 
번뜩 해보고 싶어서 무턱대로 만들었어요 (조금후회함)
어버이날을 맞이하여 그냥 넘어가기에는 아쉬우니까 특별한 이벤트입니다
어버이날을 까먹은 것은 절대 아닙니다. 오로지 원하는 선물을 드리고 싶었을 뿐... 
하지만 선물은 밑에 있는 룰렛을 돌려서 나오는 것을 드릴겁니다 선택권은 없어요 받아들이셔야합니다!!ㅋㅋㅋ 
항상 건강하게 있어주시길 바랍니다 해피 어버이날 ~~~ 😄😄 
 """,
        
        "민지": """엄마, 아빠! 어버이날 축하드려요🥳
언니가 웹페이지 만들어줘서 서프라이즈를 할 수 있게 되었어요 ㅎ
저희가 잘 자랄 수 있게 아낌없이 지원해주시고 사랑해주셔서 감사합니다
믿어주신만큼 뉴질랜드에서 잘 배우고 더 성장할게요
걱정보다는 기대가 되는 딸이 되도록 하겠습니다! 
항상 감사하고 사랑해요❤️""",

        "민준": """엄마, 아빠! 어버이날 축하드려요🥳
나가 웹페이지 만들어줘서 서프라이즈를 할 수 있게 되었어요 ㅎ
저희가 잘 자랄 수 있게 아낌없이 지원해주시고 사랑해주셔서 감사합니다
믿어주신만큼 학교에서 잘 배우고 더 성장할게요
걱정보다는 기대가 되는 아들이 되도록 하겠습니다! 
항상 감사하고 사랑해요❤️"""
    }

    # 요청받은 이름에 해당하는 편지 반환 (없으면 기본 메시지)
    letter_content = personal_letters.get(request.user_name, "사랑하는 부모님께 드립니다.")

    return {"letter": letter_content}
