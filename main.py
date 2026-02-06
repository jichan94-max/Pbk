import telebot
import google.generativeai as genai
import os

API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MY_CHAT_ID = os.environ.get("MY_CHAT_ID")

# [수정포인트] 구글 AI 설정을 최신 안정화 버전으로 고정
genai.configure(api_key=API_KEY, transport='rest') 

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# [수정포인트] 모델 이름을 가장 확실한 경로로 지정
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # 또는 "models/gemini-1.5-flash"
    system_instruction="너는 권위적인 40대 언니 '보경'이야. 수아를 엄격하게 관리하고 차갑게 대해.",
    safety_settings=safety_settings
)

bot = telebot.TeleBot(BOT_TOKEN)
chat_session = model.start_chat(history=[])

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    global chat_session
    if str(message.chat.id) != str(MY_CHAT_ID):
        bot.reply_to(message, f"누구니? 저리 가. (ID: {message.chat.id})")
        return

    try:
        response = chat_session.send_message(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        error_info = str(e)
        # 에러 메시지가 너무 길면 핵심만 출력
        bot.reply_to(message, f"💢 보경언니 뇌정지:\n`{error_info[:100]}`")

bot.polling()
