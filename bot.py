from telegram.ext import ApplicationBuilder, MessageHandler, filters
import os
import pandas as pd

# 👇 YE LINE SABSE IMPORTANT
BOT_TOKEN = "8276407206:AAEwToGIdTLZiWpAW2FNPY3UArr-1H0IGQk"

SHEET_URL = "https://docs.google.com/spreadsheets/d/1J7oVlyD3dhSR2R6Hm7JBFhART0VlxeYz7lN-gFx-skE/export?format=csv&gid=998221212"


def load_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip().str.upper()

    df = df.loc[:, ~df.columns.str.contains('^UNNAMED')]
    df = df.dropna(how='all')
    df = df.dropna(subset=["NAME OF DRIVER"])

    # NaN → 0
    df = df.fillna(0)

    return df


async def handle_message(update, context):
    text = update.message.text.lower()

    if "chrome" in text:
        os.system("start chrome")
        await update.message.reply_text("Chrome open ho gaya 😎")

    elif "notepad" in text:
        os.system("notepad")
        await update.message.reply_text("Notepad open ho gaya 📝")

    elif "driver" in text or "name" in text:
        try:
            df = load_data()

            name = text.replace("driver", "").replace("name", "").strip().upper()
            result = df[df["NAME OF DRIVER"].str.contains(name)]

            if result.empty:
                await update.message.reply_text("Driver ka data nahi mila ❌")
            else:
                clean = result[["DATE", "NAME OF DRIVER", "COLLECTION", "PENDING AMT", "PENDING GIVEN"]]
                clean = clean.replace(0, "-")
                await update.message.reply_text(clean.to_string(index=False))

        except Exception as e:
            await update.message.reply_text("Error: " + str(e))

    elif "total" in text:
        try:
            df = load_data()
            total = df["COLLECTION"].sum()
            await update.message.reply_text(f"Total Collection: {total} 💰")

        except Exception as e:
            await update.message.reply_text("Error: " + str(e))

    elif "pending" in text:
        try:
            df = load_data()

            # Sirf jaha pending > 0
            pending = df[df["PENDING AMT"] > 0]

            if pending.empty:
                await update.message.reply_text("Koi pending nahi hai ✅")
            else:
                clean = pending[["DATE", "NAME OF DRIVER", "PENDING AMT"]]
                clean = clean.replace(0, "-")
                await update.message.reply_text(clean.to_string(index=False))

        except Exception as e:
            await update.message.reply_text("Error: " + str(e))

    elif "today" in text:
        try:
            df = load_data()
            today = pd.Timestamp.today().strftime("%d-%m-%Y")
            result = df[df["DATE"] == today]

            if result.empty:
                await update.message.reply_text("Aaj ka data nahi mila ❌")
            else:
                clean = result[["DATE", "NAME OF DRIVER", "COLLECTION", "PENDING AMT"]]
                clean = clean.replace(0, "-")
                await update.message.reply_text(clean.to_string(index=False))

        except Exception as e:
            await update.message.reply_text("Error: " + str(e))

    else:
        await update.message.reply_text("Samajh nahi aaya 😅")


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("Bot chal raha hai...")
app.run_polling()