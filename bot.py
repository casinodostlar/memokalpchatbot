from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from telegram.error import BadRequest

# "chat aç" komutuna göre mesaj izinlerini aç
async def open_chat(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        if check_admin(update):  # Admin kontrolü
            await context.bot.restrict_chat_member(chat_id, update.message.from_user.id, can_send_messages=True)
            await update.message.reply_text("Chat açıldı. Artık mesaj gönderebilirsiniz.")
        else:
    except BadRequest as e:
        await update.message.reply_text(f"Hata: {str(e)}")

# "chat kapat" komutuna göre mesaj izinlerini kapat
async def close_chat(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        if check_admin(update):  # Admin kontrolü
            await context.bot.restrict_chat_member(chat_id, update.message.from_user.id, can_send_messages=False)
            await update.message.reply_text("Chat kapatıldı. Artık mesaj gönderemezsiniz.")
        else:
    except BadRequest as e:
        await update.message.reply_text(f"Hata: {str(e)}")

# Admin kontrolü
def check_admin(update: Update):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    admins = update.message.chat.get_administrators()
    admin_ids = [admin.user.id for admin in admins]
    return user_id in admin_ids

# Gelen mesajları kontrol et ve "chat aç" veya "chat kapat" mesajlarına göre işlem yap
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()  # Mesajı küçük harfe çevir
    
    if "chat aç" in text:
        await open_chat(update, context)  # "chat aç" varsa chat açma fonksiyonunu çağır
    elif "chat kapat" in text:
        await close_chat(update, context)  # "chat kapat" varsa chat kapama fonksiyonunu çağır

# Botu başlatan fonksiyon
async def main():
    # API Token'ınızı buraya girin
    TOKEN = '7797578045:AAFh3YD26LkihOF_x5BBxEyZZZxIeV2-oH4'

    # Uygulama oluşturma
    application = Application.builder().token(TOKEN).build()

    # Mesajları kontrol et
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Botu başlat
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
