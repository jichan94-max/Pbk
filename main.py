import telebot
import google.generativeai as genai
import os

# 1. 설정값 로드
API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MY_CHAT_ID = os.environ.get("MY_CHAT_ID")

# 2. 구글 AI 설정
genai.configure(api_key=API_KEY)

# 모델 설정 (가장 안정적인 호출 방식)
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
        # 안전 설정 및 검열 해제를 메시지 보낼 때마다 직접 적용
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
        # 에러가 나면 보경 언니 말투로 투덜거리게 설정
        bot.reply_to(message, f"하... 아직도 정신 못 차렸네. 다시 해봐.\n(사유: {str(e)[:50]})")

bot.polling()
