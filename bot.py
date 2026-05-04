import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import yt_dlp

# ضع توكن بوتك هنا
TOKEN = "8500977225:AAGEwjfvvU3t320IQa6DlL1PtLqvPd2eUQA"

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text('⏳ جاري التحميل... يرجى الانتظار')
    
    ydl_opts = {
        'format': 'best',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'outtmpl': 'video.mp4',
    }

    try:
        # استخدام asyncio لتشغيل yt-dlp بدون تعطيل البوت
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
        
        # إرسال الفيديو
        with open('video.mp4', 'rb') as video:
            await update.message.reply_video(video)
        
        os.remove('video.mp4')
        
    except Exception as e:
        await update.message.reply_text(f'❌ حدث خطأ: {str(e)}')

def main():
    # استخدام Application بدلاً من Updater (لإصدارات تلجرام الجديدة)
    application = Application.builder().token(TOKEN).build()
    
    # إضافة معالج الرسائل
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    print("البوت يعمل الآن بنظام v20 المحدث...")
    application.run_polling()

if __name__ == '__main__':
    main()
