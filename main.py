import telebot
import google.generativeai as genai
import os

# 1. 설정값 로드
API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MY_CHAT_ID = os.environ.get("MY_CHAT_ID")

# 2. 보경 언니 뇌(AI) 세팅
genai.configure(api_key=API_KEY)
# 구글 검열을 최대한 피하기 위한 안전 설정
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="너는 권위적인 40대 언니 '보경'이야. 수아를 엄격하게 관리하고 차갑게 대해.",
    safety_settings=safety_settings
)
bot = telebot.TeleBot(BOT_TOKEN)
chat_session = model.start_chat(history=[])

# 3. 메시지 처리 (오류 진단 포함)
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    global chat_session
    
    # ID가 다르면 입구컷
    if str(message.chat.id) != str(MY_CHAT_ID):
        bot.reply_to(message, f"누구니? 저리 가. (ID: {message.chat.id})")
        return

    try:
        response = chat_session.send_message(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # 에러 발생 시 수아님께 직접 원인 설명
        error_info = str(e)
        if "safety" in error_info.lower():
            bot.reply_to(message, "💢 구글이 내 말이 너무 세다고 검열해서 막아버렸어. 좀 더 얌전하게 말해봐.")
        elif "api_key" in error_info.lower():
            bot.reply_to(message, "💢 API 키가 안 된대. 다시 확인해봐.")
        else:
            bot.reply_to(message, f"💢 뇌정지 왔어. 이거 복사해서 보여줘:\n`{error_info[:150]}`")

print("진단 모드 보경언니 가동...")
bot.polling()
