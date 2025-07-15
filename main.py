import os
import requests
from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
AFFILIATE_LINK = os.getenv("AFFILIATE_LINK")

def get_product_info(shopee_url):
    # Simulação básica de retorno fixo para demonstração
    return {
        "title": "Vestido Longo Evangélico Floral Casual Elegante",
        "price": "R$ 79,99",
        "image_url": "https://cf.shopee.com.br/file/fakeimagem.jpg"
    }

def build_affiliate_link(base_url):
    return AFFILIATE_LINK

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    requests.post(url, json=payload)

@app.post("/")
async def receive_update(req: Request):
    data = await req.json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if "shopee.com.br" in text:
        product = get_product_info(text)
        link = build_affiliate_link(text)
        response = (
            f"📦 <b>{product['title']}</b>\n"
            f"💸 <b>Preço atual:</b> {product['price']}\n"
            f"🔗 <b>Compre aqui:</b> <a href='{link}'>{link}</a>\n"
            f"🛍️ Achado enviado por <b>@meuachado_bot</b>"
        )
        send_message(chat_id, response)
    else:
        send_message(chat_id, "Envie um link válido da Shopee para gerar o achado.")
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)