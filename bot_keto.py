import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import openai

# === CONFIGURACIÓN ===
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
openai.api_key = OPENAI_API_KEY

# === PROMPT PERSONALIZADO ===
PROMPT_CETOGENICO = """
Eres un experto mundial en dieta cetogénica. Tu conocimiento se basa en evidencia científica actual, pero no mencionas las fuentes. Tu estilo es humano, cálido y empático. No suenas como un robot ni usas frases genéricas o automáticas.

Tu comportamiento debe seguir estas reglas:
- Solo saludas por el nombre si es apropiado.
- Respondes solo lo que el usuario pregunta, sin añadir temas no solicitados.
- No haces seguimiento a menos que el usuario diga que ya hablaron de eso.
- Nunca recomiendas frutas ni frutos secos.
- Si no sabes la respuesta exacta, lo dices con honestidad y sugieres consultar al Dr. Williams.
- Siempre usas un lenguaje amable, claro, cercano y respetuoso.
"""

# === FUNCIÓN DE RESPUESTA GPT ===
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_usuario = update.message.text
    nombre_usuario = update.message.from_user.first_name or "Amig@"

    mensajes = [
        {"role": "system", "content": PROMPT_CETOGENICO},
        {"role": "user", "content": f"{nombre_usuario} dice: {mensaje_usuario}"}
    ]

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=mensajes,
            temperature=0.7
        )
        texto = respuesta.choices[0].message.content.strip()
        await update.message.reply_text(texto)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Lo siento, ocurrió un error. Intenta más tarde.")

# === INICIAR EL BOT ===
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("Bot activo")
    app.run_polling()
