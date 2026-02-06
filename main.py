import telebot
import google.generativeai as genai
import os
from google.generativeai.types import RequestOptions

# 1. 설정값 로드
API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MY_CHAT_ID = os.environ.get("MY_CHAT_ID")

# 2. 구글 AI 설정 (v1 정식 버전 주소로 강제 고정)
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="너는 40대 권위적인 언니 '보경'이야. 수아를 엄격하게 관리해."
)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    if str(message.chat.id) != str(MY_CHAT_ID):
        return
    try:
        # [핵심 수정] 구글 서버에 보낼 때 정식 버전(v1)을 사용하도록 강제 지정
        response = model.generate_content(
            message.text,
            request_options=RequestOptions(api_version='v1')
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        # 에러 메시지가 바뀌는지 확인하기 위한 문구 추가
        bot.reply_to(message, f"❌ 최종 점검 에러:\n{str(e)[:100]}")

bot.polling()
