import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from i18n import get_text

load_dotenv()

def get_user_locale(user) -> str:
    if hasattr(user, 'language_code') and user.language_code:
        if user.language_code.startswith('en'):
            return "en"
    return "ru"

def build_main_keyboard(user) -> InlineKeyboardMarkup:
    locale = get_user_locale(user)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("events_button", locale), callback_data="events")],
        [InlineKeyboardButton(text=get_text("guides_button", locale), callback_data="guides_disabled")],
        [InlineKeyboardButton(text=get_text("referral_button", locale), callback_data="referral")],
        [InlineKeyboardButton(text=get_text("help_button", locale), url="https://t.me/Iren4ik17"),
         InlineKeyboardButton(text=get_text("faq_button", locale), callback_data="faq")],
    ])

def build_practices_keyboard(user) -> InlineKeyboardMarkup:
    locale = get_user_locale(user)
    buttons = [
        [InlineKeyboardButton(text="Ночь Самайна", callback_data="practice_samhain")],
        [InlineKeyboardButton(text="Полнолуние. Разрыв кармических связей.", callback_data="practice_fullmoon_break")],
        [InlineKeyboardButton(text="Ритуал Равности Любви", callback_data="practice_equality_love")],
        [InlineKeyboardButton(text="KALI 909", callback_data="practice_kali_909")],
        [InlineKeyboardButton(text="Rave meditation 808", callback_data="practice_rave_808")],
        [InlineKeyboardButton(text="Летнее солнцестояние", callback_data="practice_summer_solstice")],
        [InlineKeyboardButton(text="Новолуние", callback_data="practice_new_moon")],
        [InlineKeyboardButton(text="Ритуал на полнолуние с Наташей Волкош", callback_data="practice_fullmoon_ritual")],
        [InlineKeyboardButton(text="Весеннее обновление", callback_data="practice_spring_renewal")],
        [InlineKeyboardButton(text="Городские мантры reLove: только Любовь", callback_data="practice_city_mantras_love_only")],
        [InlineKeyboardButton(text="Городские мантры reLove", callback_data="practice_city_mantras")],
        [InlineKeyboardButton(text=get_text("back", locale), callback_data="events")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def build_events_keyboard(user) -> InlineKeyboardMarkup:
    locale = get_user_locale(user)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("closed_channel", locale), callback_data="events_closed_channel")],
        [InlineKeyboardButton(text=get_text("hero_path", locale), callback_data="events_hero_path")],
        [InlineKeyboardButton(text=get_text("live_streams", locale), callback_data="events_live_streams")],
        [InlineKeyboardButton(text=get_text("practices_meditations", locale), callback_data="events_practices")],
        [InlineKeyboardButton(text=get_text("back", locale), callback_data="back_main")],
    ])

async def on_start(message: Message):
    await message.answer(get_text("welcome_full", get_user_locale(message.from_user)), reply_markup=build_main_keyboard(message.from_user))

async def on_guides_disabled(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.answer(get_text("guides_disabled", locale), show_alert=True)

async def on_events(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("events_text", locale), reply_markup=build_events_keyboard(call.from_user))
    await call.answer()

def build_faq_keyboard(user) -> InlineKeyboardMarkup:
    locale = get_user_locale(user)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("back", locale), callback_data="back_main")],
    ])

async def on_faq(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("faq_text", locale), reply_markup=build_faq_keyboard(call.from_user))
    await call.answer()

def build_event_pay_keyboard(user) -> InlineKeyboardMarkup:
    locale = get_user_locale(user)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("pay", locale), callback_data="events_pay_disabled")],
        [InlineKeyboardButton(text=get_text("back", locale), callback_data="events")],
    ])

def build_practice_pay_keyboard(user) -> InlineKeyboardMarkup:
    locale = get_user_locale(user)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("pay", locale), callback_data="events_pay_disabled")],
        [InlineKeyboardButton(text=get_text("back", locale), callback_data="events_practices")],
    ])

def build_referral_keyboard(user) -> InlineKeyboardMarkup:
    locale = get_user_locale(user)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("get_link", locale), callback_data="referral_disabled")],
        [
            InlineKeyboardButton(text=get_text("balance", locale), callback_data="referral_disabled"),
            InlineKeyboardButton(text=get_text("withdraw", locale), callback_data="referral_disabled"),
        ],
        [
            InlineKeyboardButton(text=get_text("referrals", locale), callback_data="referral_disabled"),
            InlineKeyboardButton(text=get_text("rules", locale), callback_data="referral_disabled"),
        ],
        [InlineKeyboardButton(text=get_text("back", locale), callback_data="back_main")],
    ])

async def on_referral(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("referral_text", locale), reply_markup=build_referral_keyboard(call.from_user))
    await call.answer()

async def on_referral_disabled(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.answer(get_text("guides_disabled", locale), show_alert=True)

async def on_events_category(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.answer(get_text("development", locale), show_alert=True)

async def on_events_closed_channel(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("events_closed_channel_text", locale), reply_markup=build_event_pay_keyboard(call.from_user))
    await call.answer()

async def on_events_hero_path(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("events_hero_path_text", locale), reply_markup=build_event_pay_keyboard(call.from_user))
    await call.answer()

async def on_events_live_streams(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("events_live_streams_text", locale), reply_markup=build_event_pay_keyboard(call.from_user))
    await call.answer()

async def on_events_practices(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer("Выберите практику или медитацию:", reply_markup=build_practices_keyboard(call.from_user))
    await call.answer()

async def on_practice_samhain(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("practice_samhain_text", locale), reply_markup=build_practice_pay_keyboard(call.from_user))
    await call.answer()

async def on_practice_fullmoon_break(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("practice_fullmoon_break_text", locale), reply_markup=build_practice_pay_keyboard(call.from_user))
    await call.answer()

async def on_practice_equality_love(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("practice_equality_love_text", locale), reply_markup=build_practice_pay_keyboard(call.from_user))
    await call.answer()

async def on_practice_kali_909(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("practice_kali_909_text", locale), reply_markup=build_practice_pay_keyboard(call.from_user))
    await call.answer()

async def on_practice_rave_808(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("practice_rave_808_text", locale), reply_markup=build_practice_pay_keyboard(call.from_user))
    await call.answer()

async def on_practice_summer_solstice(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("practice_summer_solstice_text", locale), reply_markup=build_practice_pay_keyboard(call.from_user))
    await call.answer()

async def on_practice_new_moon(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("practice_new_moon_text", locale), reply_markup=build_practice_pay_keyboard(call.from_user))
    await call.answer()

async def on_practice_fullmoon_ritual(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("practice_fullmoon_ritual_text", locale), reply_markup=build_practice_pay_keyboard(call.from_user))
    await call.answer()

async def on_practice_spring_renewal(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("practice_spring_renewal_text", locale), reply_markup=build_practice_pay_keyboard(call.from_user))
    await call.answer()

async def on_practice_city_mantras_love_only(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("practice_city_mantras_love_only_text", locale), reply_markup=build_practice_pay_keyboard(call.from_user))
    await call.answer()

async def on_practice_city_mantras(call: CallbackQuery):
    locale = get_user_locale(call.from_user)
    await call.message.delete()
    await call.message.answer(get_text("practice_city_mantras_text", locale), reply_markup=build_practice_pay_keyboard(call.from_user))
    await call.answer()

async def on_back_main(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(get_text("welcome_full", get_user_locale(call.from_user)), reply_markup=build_main_keyboard(call.from_user))
    await call.answer()

async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Ошибка: токен бота не найден!")
        print("Пожалуйста, создайте файл .env и добавьте в него:")
        print("BOT_TOKEN=ваш_токен_здесь")
        return
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.message.register(on_start, CommandStart())
    dp.callback_query.register(on_guides_disabled, F.data == "guides_disabled")
    dp.callback_query.register(on_events, F.data == "events")
    dp.callback_query.register(on_faq, F.data == "faq")
    dp.callback_query.register(on_referral, F.data == "referral")
    dp.callback_query.register(on_referral_disabled, F.data == "referral_disabled")
    dp.callback_query.register(on_events_closed_channel, F.data == "events_closed_channel")
    dp.callback_query.register(on_events_hero_path, F.data == "events_hero_path")
    dp.callback_query.register(on_events_live_streams, F.data == "events_live_streams")
    dp.callback_query.register(on_events_practices, F.data == "events_practices")
    dp.callback_query.register(on_practice_samhain, F.data == "practice_samhain")
    dp.callback_query.register(on_practice_fullmoon_break, F.data == "practice_fullmoon_break")
    dp.callback_query.register(on_practice_equality_love, F.data == "practice_equality_love")
    dp.callback_query.register(on_practice_kali_909, F.data == "practice_kali_909")
    dp.callback_query.register(on_practice_rave_808, F.data == "practice_rave_808")
    dp.callback_query.register(on_practice_summer_solstice, F.data == "practice_summer_solstice")
    dp.callback_query.register(on_practice_new_moon, F.data == "practice_new_moon")
    dp.callback_query.register(on_practice_fullmoon_ritual, F.data == "practice_fullmoon_ritual")
    dp.callback_query.register(on_practice_spring_renewal, F.data == "practice_spring_renewal")
    dp.callback_query.register(on_practice_city_mantras_love_only, F.data == "practice_city_mantras_love_only")
    dp.callback_query.register(on_practice_city_mantras, F.data == "practice_city_mantras")
    dp.callback_query.register(on_events_category, F.data == "events_pay_disabled")
    dp.callback_query.register(on_back_main, F.data == "back_main")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


