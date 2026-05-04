import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import yt_dlp

# ضع توكن بوتك هنا بين علامتي الاقتباس
TOKEN = "8500977225:AAGEwjfvvU3t320IQa6DlL1PtLqvPd2eUQA"

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    # التأكد من أن الرسالة رابط
    if not url.startswith('http'):
        return

    await update.message.reply_text('⏳ جاري استخدام "الكوكيز" لتجاوز الحماية والتحميل... يرجى الانتظار')
    
    ydl_opts = {
        'format': 'best',
        'cookiefile': 'cookies.txt',  # استخدام الملف الذي رفعته لـ GitHub
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'outtmpl': 'video.mp4',
    }

    try:
        # تشغيل عملية التحميل
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
        
        # إرسال الفيديو للمستخدم
        with open('video.mp4', 'rb') as video:
            await update.message.reply_video(video, caption="✅ تم التحميل بنجاح بواسطة بوتك!")
        
        # حذف الفيديو من السيرفر بعد الإرسال لتوفير المساحة
        os.remove('video.mp4')
        
    except Exception as e:
        await update.message.reply_text(f'❌ فشل التحميل. يوتيوب لا يزال يرفض السيرفر أو الرابط غير مدعوم.\nالخطأ: {str(e)}')

def main():
    # بناء تطبيق التلجرام (الإصدار الحديث)
    application = Application.builder().token(TOKEN).build()
    
    # إعداد معالج الرسائل (يستقبل النصوص فقط)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    print("البوت يعمل الآن باستخدام ملف الكوكيز المحدث...")
    application.run_polling()

if __name__ == '__main__':
    main()
