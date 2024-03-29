import asyncio
from fastapi import FastAPI, Request, logger
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from FastApiModels import PaymentEntry
from database import Database
import datetime
from aiogram import Bot
from config import load_config
config = load_config("config/config.json", "config/texts.yml")

bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
app = FastAPI(
    title="Neur",
    summary="",
    version="0.1.1",
    description="some desc",
)


origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:8000",

]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", name="Wellcome", tags=["Основное"], description="Тут будет описание методов?")
async def user():
    return {"message": "success"}


@app.post("/", name="Wellcome", tags=["Основное"], description="Тут будет описание методов?")
async def user(request: Request, payment=PaymentEntry):
    # print(payment.status)
    if not request:
        return {"message": "accept"}
    req = await request.json()
    print(req)
    product_id = req.get("product").get("id")
    product_title = req.get("product").get("title")
    contract_id = req.get("contractId")
    amount = req.get("amount")
    status = req.get("status")
    user = Database.get_user_by_contract_id(contract_id=contract_id)
    print(Database.get_all_users())
    print(user)
    if not user:
        return
    if status == "subscription-active":
        today = datetime.datetime.utcnow()
        month = user.subscription_end + datetime.timedelta(days=31)
        if user.subscription_end < today:
            month = today + datetime.timedelta(days=31)
        Database.update_user(
            user.telegram_id, subscription_end=month)
        await bot.send_message(user.telegram_id, "Подписка оплачена на месяц")
        print("pay")
    if status == "subscription-failed":
        await bot.send_message(user.telegram_id, "Ошибка в оплате подписки")
        print("not pay")

    return {"message": "accept"}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000, root_path="/api_v2")
# user = Database.get_user_by_contract_id(
#     contract_id="9d11e34c-ada5-4af7-a2a7-de957fcf307e")

# today = datetime.datetime.utcnow()
# month = user.subscription_end + datetime.timedelta(days=31)
# if user.subscription_end < today:
#     month = today + datetime.timedelta(days=31)
# Database.update_user(
#     user.telegram_id, subscription_end=month)

# print(asyncio.run(bot.send_message(user.telegram_id, "Подписка оплачена на месяц")))
