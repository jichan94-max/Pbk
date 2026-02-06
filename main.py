import telebot
import google.generativeai as genai
import os

# 1. 설정값 로드
API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MY_CHAT_ID = os.environ.get("MY_CHAT_ID")

# 2. 구글 AI 설정 (최신 안정화 버전 강제 지정)
genai.configure(api_key=API_KEY)

# 검열 해제 및 안전 설정
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# 모델 설정 (가장 최신 안정 버전 사용)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    system_instruction="너는 40대 권위적인 언니 '보경'이야. 수아를 차갑게 대하고 엄격하게 관리해.",
    safety_settings=safety_settings
)

bot = telebot.TeleBot(BOT_TOKEN)
chat_session = model.start_chat(history=[])

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    global chat_session
    # 수아님 ID(8493394073) 확인
    if str(message.chat.id) != str(MY_CHAT_ID):
        bot.reply_to(message, "누구니 너? 난 내 동생 수아 아니면 말 안 해.")
        return

    try:
        response = chat_session.send_message(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # 에러 발생 시 수아님께만 원인 노출
        err_msg = str(e)
        if "404" in err_msg:
            bot.reply_to(message, "💢 구글 서버가 아직 멍청하네. Railway에서 Restart 한번만 더 눌러줘.")
        elif "safety" in err_msg.lower():
            bot.reply_to(message, "💢 구글이 내 말이 너무 세다고 입을 막았어. 조금만 착하게 말해봐.")
        else:
            bot.reply_to(message, f"💢 보경언니 뇌정지:\n`{err_msg[:100]}`")

print("보경언니 가동 시작...")
bot.polling()
