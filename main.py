import telebot
import google.generativeai as genai
import os
from datetime import datetime

# 설정값 가져오기
API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MY_CHAT_ID = os.environ.get("MY_CHAT_ID")

# 시스템 설정
SYSTEM_INSTRUCTION = "너는 40대 여성 '보경'이야. 수아를 엄격하게 관리해. 냉소적이고 권위적인 말투를 써."

# AI 설정 (검열 최대한 해제)
genai.configure(api_key=API_KEY)
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION,
    safety_settings=safety_settings
)
bot = telebot.TeleBot(BOT_TOKEN)
chat_session = model.start_chat(history=[])

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    global chat_session
    # 아이디 체크 (수아님 ID: 8493394073 인지 확인)
    if str(message.chat.id) != str(MY_CHAT_ID):
        bot.reply_to(message, f"넌 누구니? 난 수아만 상대해. (ID: {message.chat.id})")
        return

    try:
        response = chat_session.send_message(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # ★ 오류 발생 시 구체적인 이유를 봇이 직접 말함
        error_msg = str(e)
        if "safety" in error_msg.lower():
            bot.reply_to(message, f"💢 구글이 검열해서 대답 안 한대. 표현을 좀 순화해봐. (사유: Safety)")
        else:
            bot.reply_to(message, f"💢 보경언니 뇌정지 옴. 이거 보여주고 고쳐달라고 해:\n`{error_msg[:100]}`")

print("보경언니 재가동...")
bot.polling()
