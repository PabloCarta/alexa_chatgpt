from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Usa tu API key de OpenAI desde variable de entorno (mejor práctica)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["POST"])
def alexa_webhook():
    data = request.get_json()
    print(data)

    try:
        # Extrae el mensaje que dice el usuario a Alexa
        mensaje_usuario = data["request"]["intent"]["slots"]["mensaje"]["value"]

        # Llama al modelo de OpenAI
        respuesta = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente útil que responde de forma amable y natural."},
                {"role": "user", "content": mensaje_usuario}
            ]
        )

        texto_respuesta = respuesta.choices[0].message.content

        # Devuelve una respuesta válida para Alexa
        return jsonify({
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": texto_respuesta
                },
                "shouldEndSession": False
            }
        })

    except Exception as e:
        print("Error con OpenAI:", e)
        return jsonify({
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Lo siento, hubo un problema al procesar tu mensaje."
                },
                "shouldEndSession": True
            }
        })

if __name__ == "__main__":
    # Render usará Gunicorn, pero esto sirve si lo pruebas localmente
    app.run(host="0.0.0.0", port=5000)
