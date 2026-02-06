import telebot
import google.generativeai as genai
import os

# 환경 변수 가져오기
API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MY_CHAT_ID = os.environ.get("MY_CHAT_ID")

# 구글 AI 설정 (주소를 v1 정식 버전으로 강제 고정)
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # 'models/'를 빼고 적어보세요
    system_instruction="너는 40대 권위적인 언니 '보경'이야. 수아를 엄격하게 관리해."
)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    if str(message.chat.id) != str(MY_CHAT_ID):
        return
    try:
        # 이 부분이 핵심입니다: 주소를 직접 호출하는 방식 대신 기본 전송 사용
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"💢 아직도 꼬였네:\n`{str(e)[:100]}`")

bot.polling()
