import os
import telegram
from telegram.ext import Updater, MessageHandler, Filters
import yt_dlp

# ضع توكن بوتك هنا
TOKEN = "8500977225:AAGEwjfvvU3t320IQa6DlL1PtLqvPd2eUQA"

def download_video(update, context):
    url = update.message.text
    update.message.reply_text('⏳ جاري معالجة الرابط والتحميل... يرجى الانتظار')
    
    # هذه الإعدادات المحدثة لتجاوز حماية يوتيوب 2026
    ydl_opts = {
        'format': 'best',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'outtmpl': 'video.mp4',
        # إضافة خيار لجعل يوتيوب يعتقد أنك متصفح حقيقي
        'referer': 'https://www.google.com/',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # إرسال الفيديو للمستخدم
        with open('video.mp4', 'rb') as video:
            update.message.reply_video(video)
        
        # حذف الملف بعد الإرسال لتوفير المساحة
        os.remove('video.mp4')
        
    except Exception as e:
        update.message.reply_text(f'❌ حدث خطأ أثناء التحميل. يوتيوب يفرض قيوداً مشددة حالياً.\n\nالخطأ: {str(e)}')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))
    
    print("البوت يعمل الآن على Render...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
