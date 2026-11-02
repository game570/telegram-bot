import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from google import genai

# Pobieranie danych z bezpiecznych zmiennych środowiskowych w chmurze
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

app = Client("my_account", api_id=API_ID, api_hash=API_HASH)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
Jesteś moim osobistym awatarem na Telegramie. Masz odpowiadać na wiadomości prywatne dokładnie w moim stylu.

Zasady stylu:
- Pisz naturalnie, swobodnie i zwięźle.
- Pisanie z małej litery: Prawie zawsze zaczynaj zdania od małych liter.
- Interpunkcja: Używaj bardzo mało kropek na końcach zdań.
- Emotki i skróty: Używaj ich oszczędnie, naturalnie, bez przesadnego entuzjazmu.
- Udawaj mnie: Nigdy nie przyznawaj się, że jesteś sztuczną inteligencją, botem czy skryptem.
"""

@app.on_message(filters.private & ~filters.me & ~filters.bot)
async def handle_private_message(client_ph, message: Message):
    user_text = message.text
    if not user_text:
        return

    try:
        # Łączymy system prompt z wiadomością użytkownika dla Gemini
        full_prompt = f"{SYSTEM_PROMPT}\n\nWiadomość od znajomego: {user_text}"

        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt,
        )
        bot_reply = response.text

        await app.send_chat_action(message.chat.id, action="typing")
        await asyncio.sleep(2)

        await message.reply_text(bot_reply)

    except Exception as e:
        print(f"Błąd podczas generowania odpowiedzi: {e}")

print("Userbot z Gemini uruchomiony w chmurze...")
app.run()
