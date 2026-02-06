import telebot
import google.generativeai as genai
import os

# 1. 설정값 로드
API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MY_CHAT_ID = os.environ.get("MY_CHAT_ID")

# 2. 구글 AI 설정 (v1 정식 버전 강제 지정)
genai.configure(api_key=API_KEY, transport='rest')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    if str(message.chat.id) != str(MY_CHAT_ID):
        return
    
    try:
        # 모델을 매번 새로 정의해서 최신 주소를 찾게 함
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"너는 40대 권위적인 언니 '보경'이야. 수아를 엄격하게 관리해. 짧게 반말로 답해: {message.text}",
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"💢 보경언니 최종 에러 로그:\n`{str(e)[:100]}`")

bot.polling()
