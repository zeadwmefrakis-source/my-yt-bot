import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        msg = await update.message.reply_text("⏳ جاري التحميل... يرجى الانتظار")
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video.mp4',
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            await update.message.reply_video(video=open('video.mp4', 'rb'), caption="تم التحميل بنجاح ✅")
            os.remove('video.mp4')
            await msg.delete()
        except Exception as e:
            await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")
    else:
        await update.message.reply_text("⚠️ أرسل رابط يوتيوب صحيح")

if __name__ == '__main__':
    # ضع التوكن الخاص بك هنا بين علامتي الاقتباس
    TOKEN = "8500977225:AAGEwjfvvU3t320IQa6DlL1PtLqvPd2eUQA"
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("البوت يعمل...")
    app.run_polling()
