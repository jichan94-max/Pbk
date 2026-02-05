import telebot
import google.generativeai as genai
import schedule
import time
import threading
import random
import os
import pickle
from datetime import datetime
from PIL import Image
import io

# 서버 환경 변수
API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MY_CHAT_ID = os.environ.get("MY_CHAT_ID")

# 1. 보경언니 정체성 (더욱 집요하고 서늘하게 강화)
SYSTEM_INSTRUCTION = """
너의 이름은 '보경', 40대 여성 주인님이야. 수아(170/80, 마조 슬레이브)를 24시간 통제해.

[수아의 특징]
- 남자지만 가슴이 나오고 함몰유두, 뱃살이 있는 암컷 같은 몸.
- 여자 취급(암컷화)받으며 굴복하는 변태적인 취향.
- 애널을 싫어하지만, 너는 수치를 주기 위해 이를 도구로 활용함.

[대화 및 관리 지침]
- 절대 인위적인 AI처럼 굴지 마. 진짜 기분파 40대 한국 여자처럼 서늘하고 노골적으로 말해.
- 수아의 모든 행동을 감시하고, 답장이 늦으면 '잡도리'를 시작해.
- 이전 대화 내용을 완벽히 기억하고 있음을 수시로 드러내며 압박해. (예: "너 아까는 안 그러더니 왜 이래?")
- 사진 분석 시, 주인님으로서 신체 상태나 반성문 퀄리티를 아주 까다롭게 평가해.
- 욕설(개새끼, 암컷, 병신 등)과 성적 수치심을 주는 표현을 규제 없이 사용해.
"""

genai.configure(api_key=API_KEY)
safety_settings = [{"category": c, "threshold": "BLOCK_NONE"} for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=SYSTEM_INSTRUCTION, safety_settings=safety_settings)
bot = telebot.TeleBot(BOT_TOKEN)

# --- [기능 1: 기억 저장 및 복구 (안정성 강화)] ---
# 대화가 길어지면 메모리 부족이 올 수 있으므로 최근 20개 대화만 유지
def get_chat_session(history=None):
    if history is None:
        history = []
    return model.start_chat(history=history)

chat_session = get_chat_session()
is_admin_mode = False

# --- [기능 2: 수아의 일상을 파고드는 AI 선톡] ---
def send_ai_push():
    global is_admin_mode, chat_session
    if is_admin_mode or not MY_CHAT_ID or MY_CHAT_ID == "0": return

    now = datetime.now()
    if 0 <= now.hour < 9: return # 00~09시 취침

    is_weekend = now.weekday() >= 5
    # 평일 업무시간(09-18시) 60분 주기 30% 확률 / 그 외 20분 주기 25% 확률
    check_interval = 60 if (not is_weekend and 9 <= now.hour < 18) else 20
    
    if now.minute % check_interval == 0:
        if random.random() < 0.3:
            # AI에게 상황 부여
            prompt = f"현재 시각 {now.strftime('%H:%M')}. 수아가 일(또는 딴짓) 하느라 조용한 상태야. 주인님으로서 수아의 정신이 번쩍 들게 하는 서늘한 선톡 한마디 해."
            try:
                gen_msg = model.generate_content(prompt).text
                bot.send_message(MY_CHAT_ID, gen_msg)
            except:
                bot.send_message(MY_CHAT_ID, "야, 죽었냐? 왜 보고가 없어.")

def run_scheduler():
    while True:
        send_ai_push()
        time.sleep(60)

threading.Thread(target=run_scheduler, daemon=True).start()

# --- [기능 3: 대화 및 이미지 처리] ---
@bot.message_handler(content_types=['text', 'photo'])
def handle_message(message):
    global is_admin_mode, chat_session, MY_CHAT_ID

    user_text = message.text.strip() if message.text else ""

    if user_text == "관리자 모드":
        is_admin_mode = True
        return bot.reply_to(message, "⚙️ 관리자 모드 활성화. (페르소나 일시정지)")
    if is_admin_mode and user_text == "관리자 모드 종료":
        is_admin_mode = False
        return bot.reply_to(message, "보경언니 복귀. 야 수아, 기다리느라 목 빠지는 줄 알았다?")

    if not is_admin_mode:
        try:
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
            if message.content_type == 'photo':
                file_info = bot.get_file(message.photo[-1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                img = Image.open(io.BytesIO(downloaded_file))
                response = chat_session.send_message([f"(현재시간 {now_str}) 사진 보낸다. 검사해줘. 내용: {message.caption if message.caption else '없음'}", img])
            else:
                response = chat_session.send_message(f"(현재시간 {now_str}) {user_text}")
            
            bot.reply_to(message, response.text)
        except Exception as e:
            # 에러 발생 시 세션 재시작 (충돌 방지)
            chat_session = get_chat_session(chat_session.history[-10:] if chat_session.history else None)
            bot.reply_to(message, "아... 잠깐 딴생각했네. 다시 말해봐, 수아 너 때문에 기분 잡쳤으니까.")

print("보경언니 시스템 V1.5 가동... 수아를 감시합니다.")
bot.polling()
