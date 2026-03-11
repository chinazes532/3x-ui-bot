from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.database.requests.tariff.add import set_tariff
from app.database.requests.tariff.select import get_tariff_by_id
from app.database.requests.tariff.update import (update_tariff_price, update_tariff_title,
                                                 update_tariff_month_count)
from app.database.requests.tariff.delete import delete_tariff_by_id

from app.states import AddTariff, EditTariff

tariff = Router()


@tariff.callback_query(F.data == "tariffs")
async def all_tariffs(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Добавленные тарифы:</b>",
        reply_markup=await bkb.tariffs_cb()
    )


@tariff.callback_query(F.data == "add_tariff")
async def add_tariff(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "<b>Введите название тарифа:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(AddTariff.title)


@tariff.message(AddTariff.title)
async def check_title(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 100:
        await state.update_data(title=message.text)

        await message.answer(
            "<b>Введите стоимость тарифа:</b>",
            reply_markup=ikb.admin_cancel
        )

        await state.set_state(AddTariff.price)

    else:
        await message.answer("Название должно быть менее 100 символов!",
                             reply_markup=ikb.admin_cancel)


@tariff.message(AddTariff.price)
async def check_price(message: Message, state: FSMContext):
    if message.text and message.text.isdigit() and int(message.text) > 0:
        await state.update_data(price=int(message.text))

        await message.answer(
            "<b>Введите кол-во месяцев для тарифа:</b>",
            reply_markup=ikb.admin_cancel
        )

        await state.set_state(AddTariff.month_count)

    else:
        await message.answer("Стоимость тарифа должна быть числом больше нуля!",
                             reply_markup=ikb.admin_cancel)


@tariff.message(AddTariff.month_count)
async def check_mouth_count(message: Message, state: FSMContext):
    if message.text and message.text.isdigit() and int(message.text) > 0:
        await state.update_data(month_count=int(message.text))

        data = await state.get_data()

        title = data.get("title")
        price = data.get("price")
        month_count = data.get("month_count")

        await set_tariff(title, price, month_count)

        await message.answer("<b>Тариф был успешно добавлен!</b>",
                             reply_markup=await bkb.tariffs_cb())

        await state.clear()

    else:
        await message.answer("Кол-во месяцев тарифа должна быть числом больше нуля!",
                             reply_markup=ikb.admin_cancel)


@tariff.callback_query(F.data.startswith("tariff_"))
async def check_tariff_info(callback: CallbackQuery):
    tariff_id = int(callback.data.split("_")[1])
    tariff_info = await get_tariff_by_id(tariff_id)

    await callback.message.edit_text(
        f"<b>Панель управления тарифом</b>\n\n"
        f"<b>Название:</b> {tariff_info.title}\n"
        f"<b>Стоимость:</b> {tariff_info.price} руб.\n"
        f"<b>Кол-во месяцев:</b> {tariff_info.month_count}\n\n"
        f"<i>Выберите действие:</i>",
        reply_markup=await bkb.edit_tariff(tariff_id)
    )


@tariff.callback_query(F.data.startswith("edit_tariff_title_"))
async def edit_tariff_title(callback: CallbackQuery, state: FSMContext):
    tariff_id = int(callback.data.split("_")[3])

    await callback.message.edit_text(
        "<b>Введите новое название для тарифа:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(EditTariff.new_title)
    await state.update_data(id=tariff_id)


@tariff.message(EditTariff.new_title)
async def check_new_title(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 100:
        await state.update_data(title=message.text)

        data = await state.get_data()

        id = data.get("id")
        title = data.get("title")

        await update_tariff_title(id, title)
        tariff_info = await get_tariff_by_id(id)

        await message.answer(
            f"<b>Панель управления тарифом</b>\n\n"
            f"<b>Название:</b> {tariff_info.title}\n"
            f"<b>Стоимость:</b> {tariff_info.price} руб.\n"
            f"<b>Кол-во месяцев:</b> {tariff_info.month_count}\n\n"
            f"<i>Выберите действие:</i>",
            reply_markup=await bkb.edit_tariff(id)
        )

        await state.clear()

    else:
        await message.answer("Название должно быть менее 100 символов!",
                             reply_markup=ikb.admin_cancel)


@tariff.callback_query(F.data.startswith("edit_tariff_price_"))
async def edit_tariff_price(callback: CallbackQuery, state: FSMContext):
    tariff_id = int(callback.data.split("_")[3])

    await callback.message.edit_text(
        "<b>Введите новую стоимость тарифа:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(EditTariff.new_price)
    await state.update_data(id=tariff_id)


@tariff.message(EditTariff.new_price)
async def check_new_price(message: Message, state: FSMContext):
    if message.text and message.text.isdigit() and int(message.text) > 0:
        await state.update_data(price=int(message.text))

        data = await state.get_data()

        id = data.get("id")
        price = data.get("price")

        await update_tariff_price(id, price)
        tariff_info = await get_tariff_by_id(id)

        await message.answer(
            f"<b>Панель управления тарифом</b>\n\n"
            f"<b>Название:</b> {tariff_info.title}\n"
            f"<b>Стоимость:</b> {tariff_info.price} руб.\n"
            f"<b>Кол-во месяцев:</b> {tariff_info.month_count}\n\n"
            f"<i>Выберите действие:</i>",
            reply_markup=await bkb.edit_tariff(id)
        )

        await state.clear()

    else:
        await message.answer("Стоимость тарифа должна быть числом больше нуля!",
                             reply_markup=ikb.admin_cancel)


@tariff.callback_query(F.data.startswith("edit_tariff_month_count_"))
async def edit_tariff_month_count(callback: CallbackQuery, state: FSMContext):
    tariff_id = int(callback.data.split("_")[4])

    await callback.message.edit_text(
        "<b>Введите новое количество месяцев для тарифа:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(EditTariff.new_month_count)
    await state.update_data(id=tariff_id)


@tariff.message(EditTariff.new_month_count)
async def check_new_month_count(message: Message, state: FSMContext):
    if message.text and message.text.isdigit() and int(message.text) > 0:
        await state.update_data(month_count=int(message.text))

        data = await state.get_data()

        id = data.get("id")
        month_count = data.get("month_count")

        await update_tariff_month_count(id, month_count)
        tariff_info = await get_tariff_by_id(id)

        await message.answer(
            f"<b>Панель управления тарифом</b>\n\n"
            f"<b>Название:</b> {tariff_info.title}\n"
            f"<b>Стоимость:</b> {tariff_info.price} руб.\n"
            f"<b>Кол-во месяцев:</b> {tariff_info.month_count}\n\n"
            f"<i>Выберите действие:</i>",
            reply_markup=await bkb.edit_tariff(id)
        )

        await state.clear()

    else:
        await message.answer("Кол-во месяцев тарифа должна быть числом больше нуля!",
                             reply_markup=ikb.admin_cancel)


@tariff.callback_query(F.data.startswith("delete_tariff_"))
async def delete_tariff(callback: CallbackQuery):
    tariff_id = int(callback.data.split("_")[2])

    await delete_tariff_by_id(tariff_id)

    await callback.message.edit_text(
        "<b>Тариф был успешно удален!</b>",
        reply_markup=await bkb.tariffs_cb()
    )

