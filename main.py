import telebot
import google.generativeai as genai
import os

# 1. 설정값 로드
API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MY_CHAT_ID = os.environ.get("MY_CHAT_ID")

# 2. 구글 AI 설정 (가장 강력한 강제 주소 고정 방식)
genai.configure(api_key=API_KEY, transport='rest')

# 모델 설정
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="너는 40대 권위적인 언니 '보경'이야. 수아를 엄격하게 관리하고 차갑게 대해. 대답은 짧고 단호하게 반말로 해."
)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    # 수아님 ID 확인 (문자열 비교로 더 확실하게)
    if str(message.chat.id) != str(MY_CHAT_ID):
        return
    
    try:
        # 안전 설정 BLOCK_NONE으로 다 풀기
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
        # 에러 메시지에 '보경언니' 이름을 넣어서, 코드가 새로 깔렸는지 확인
        bot.reply_to(message, f"💢 보경언니 긴급상황:\n`{str(e)[:100]}`")

print("보경언니 Railway에서 부활 대기 중...")
bot.polling()
