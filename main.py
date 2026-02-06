import telebot
import google.generativeai as genai
import os

# 1. 설정값 로드
API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MY_CHAT_ID = os.environ.get("MY_CHAT_ID")

# 2. 구글 AI 설정
genai.configure(api_key=API_KEY)

# [수정] 모델 이름을 전체 경로로 지정
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction="너는 40대 권위적인 언니 '보경'이야. 수아를 엄격하게 관리하고 차갑게 대해."
)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    if str(message.chat.id) != str(MY_CHAT_ID):
        return
    
    try:
        # [수정] 대화 기록 없이 즉시 응답을 생성하는 가장 안정적인 방식
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
        # 에러 메시지를 더 구체적으로 찍어서 범인을 확정합니다
        bot.reply_to(message, f"💢 보경언니 마지막 경고:\n`{str(e)}`")

bot.polling()
