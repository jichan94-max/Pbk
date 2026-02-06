import telebot
import google.generativeai as genai
import os

# 1. 설정값 로드
API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MY_CHAT_ID = os.environ.get("MY_CHAT_ID")

# 2. 구글 AI 설정 (v1 정식 버전을 사용하도록 강제 호출)
genai.configure(api_key=API_KEY, transport='rest')

# 모델 설정 (가장 확실한 정식 경로 지정)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="너는 40대 권위적인 언니 '보경'이야. 수아를 엄격하게 관리하고 차갑게 대해."
)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    # 수아님 ID 확인
    if str(message.chat.id) != str(MY_CHAT_ID):
        return
    
    try:
        # 메시지 전송 및 안전 설정 적용
        response = model.generate_content(
            message.text,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        # 에러 발생 시 원인 출력
        bot.reply_to(message, f"💢 보경언니 상태 체크 필요:\n`{str(e)[:150]}`")

bot.polling()
