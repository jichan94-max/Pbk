import telebot
import google.generativeai as genai
import os

# 1. 환경 변수 설정
API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MY_CHAT_ID = os.environ.get("MY_CHAT_ID")

# 2. 구글 AI 설정 (정식 버전 경로 사용)
genai.configure(api_key=API_KEY)

# 안전 설정 (검열 해제)
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# 모델 설정 (가장 안정적인 flash 버전)
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
    # 주인님 확인 (ID: 8493394073)
    if str(message.chat.id) != str(MY_CHAT_ID):
        bot.reply_to(message, "누구니 너?")
        return

    try:
        # 메시지 전송
        response = chat_session.send_message(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # 에러 발생 시 핵심만 노출
        err_msg = str(e)
        if "404" in err_msg:
            bot.reply_to(message, "💢 구글 서버 주소가 꼬였어. Railway에서 Redeploy 눌러줘!")
        else:
            bot.reply_to(message, f"💢 보경언니 뇌정지:\n`{err_msg[:100]}`")

print("보경언니 재가동...")
bot.polling()
