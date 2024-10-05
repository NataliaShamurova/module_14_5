from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

#from filt.chat_types import ChatTypesFilter, IsAdmin
from kb13.reply import get_keyboard
import crud_functions


crud_functions.initiate_db()
admin_router = Router()

ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Изменить товар",
    "Удалить товар",

    placeholder="Выберите действие",
    sizes=(2, 1),
)


@admin_router.message(Command("admin"))
async def admin_features(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


# @admin_router.message(F.text == "Изменить товар")
# async def change_product(message: types.Message):
#     await message.answer("ОК, вот список товаров")
#
#
# @admin_router.message(F.text == "Удалить товар")
# async def delete_product(message: types.Message):
#     await message.answer("Выберите товар(ы) для удаления")


#Машина состояний
class AddProduct(StatesGroup):
    title = State()
    description = State()
    price = State()



@admin_router.message(StateFilter(None),
                      F.text == "Добавить товар")  #должнф встать в состояние ожидания конкретного ответа, что введе пользователь
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Введите название товара",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProduct.title)


@admin_router.message(StateFilter('*'), Command("Отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()  #Текущее состояние

    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@admin_router.message(AddProduct.title, F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание товара")
    await state.set_state(AddProduct.description)


@admin_router.message(AddProduct.title)
async def add_name2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели некорректное название")


@admin_router.message(AddProduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите стоимость товара")
    await state.set_state(AddProduct.price)


@admin_router.message(AddProduct.description)
async def add_description2(message: types.Message):
    await message.answer("Вы ввели недопустимое описание")


@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    try:
        float(message.text)
    except ValueError:
        await message.answer('Введите корректную цену')
        return

    # await state.update_data(price=message.text)
    # await crud_functions.add_products(state)
    # await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
    # await state.clear()
    product_data = (await state.get_data()).get('name'), (await state.get_data()).get('description'), float(
        message.text)
    crud_functions.add_product(product_data)
    await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
    await state.clear()

#При неккорректном введении цены
@admin_router.message(AddProduct.price)
async def add_price2(message: types.Message):
    await message.answer("Вы ввели недопустимые данные, введите цену заново")
