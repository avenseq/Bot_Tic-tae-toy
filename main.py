from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
router: Router = Router()
BOT_TOKEN = 'YOUR BOT TOKEN'

# with sq.connect('database_players.db') as con:
#     cur = con.cursor()
#     cur.execute("INSERT INTO players VALUES()")

data = {}
def keyboard_players():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text = '😎', callback_data='smile_😎')
    keyboard.button(text = '😈', callback_data='smile_😈')
    keyboard.button(text='👽', callback_data='smile_👽')
    keyboard.adjust()
    return keyboard.as_markup()

def keyboard_player1():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text = '😎', callback_data='smile1_😎')
    keyboard.button(text = '😈', callback_data='smile1_😈')
    keyboard.button(text='👽', callback_data='smile1_👽')
    keyboard.adjust()
    return keyboard.as_markup()

def keyboard_player2():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text = '💀', callback_data='smile2_💀')
    keyboard.button(text = '👻', callback_data='smile2_👻')
    keyboard.button(text='👹', callback_data='smile2_👹')
    keyboard.adjust()
    return keyboard.as_markup()


class process(StatesGroup):
    game_non = State()
    game_players_ready = State()
    choice_user1 = State()
    choice_user2 = State()
    game_in_process = State()
    game_over = State()



class game_board:
    def __init__(self):
        self.g_board = ['' for _ in range(9)]
        self.move = 0
    def get_g_board(self):
        keyboard = InlineKeyboardBuilder()
        for i in range(len(self.g_board)):
            if self.g_board[i] == 'x':
                keyboard.button(text='❌', callback_data=f'button_{i}')
            elif self.g_board[i] == '0':
                keyboard.button(text='🔵', callback_data=f'button_{i}')
            else:
                keyboard.button(text='⬜', callback_data=f'button_{i}')
        keyboard.adjust(3)
        return keyboard.as_markup()
    def game_over(self, board: list, sign: str):
        zeroes = board.count('')
        if board[0] == board[1] == board[2] == sign:
            return sign
        elif board[3] == board[4] == board[5] == sign:          #горизонтальная победа
            return sign
        elif board[6] == board[7] == board[8] == sign:
            return sign
        elif board[0] == board[3] == board[6] == sign:
            return sign
        elif board[1] == board[4] == board[7] == sign:         #вертикальная победа
            return sign
        elif board[2] == board[5] == board[8] == sign:
            return sign
        elif board[0] == board[4] == board[8] == sign:         #главная
            return sign
        elif board[2] == board[4] == board[6] == sign:         #побочная
            return sign
        elif zeroes == 0:
            return 'Piece'
        return False











@router.message(Command('start'))
async def start_bot(message: Message):
    await message.answer('Привет! Это игра в крестики-нолики! Напиши /choice, чтобы выбрать кто играет')

@router.message(Command('help'))
async def help(message: Message):
    await message.answer('Помощь:\n'
                         '/choice - выбор игроков\n'
                         '/play - начать игру')



@router.message(Command('choice'))
async def choice(message: Message, state: FSMContext):
    await message.answer('Первый игрок:', reply_markup=keyboard_player1())
    #await state.set_state(process.choice_user1)

@router.callback_query(F.data.startswith("smile1_"))
async def us1(callback: CallbackQuery, state: FSMContext):
    # with sq.connect('database_players.db') as con:
    #     cur = con.cursor()
    #     cur.execute(f"INSERT INTO players VALUES({callback.from_user.username}, {callback.data.split('_')[1]})")
    data['player1'] = '@' + str(callback.from_user.username)
    data['smile1'] = callback.data.split('_')[1]
    #await state.update_data(player1 = '@' + str(callback.from_user.username), smile1 = callback.data.split('_')[1])
    await callback.message.answer('1 игрок выбран! Второй игрок:', reply_markup=keyboard_player2())
    await state.set_state(process.game_players_ready)
  # await state.set_state(process.game_players_ready)

@router.callback_query(F.data.startswith("smile2_"))
async def us2(callback: CallbackQuery, state: FSMContext):
    data['player2'] = '@' + str(callback.from_user.username)
    data['smile2'] = callback.data.split('_')[1]
   # await state.update_data(player2 = '@' + str(callback.from_user.username), smile2 = callback.data.split('_')[1])
    await callback.message.answer('2 игрок выбран! Напишите /play чтобы начать')
    await state.set_state(process.game_players_ready)


@router.message(Command('play'), process.game_players_ready)
async def start_bot(message: Message, state: FSMContext):
    global gb
    gb = game_board()
   # data = await state.get_data()
    #await state.clear()
    await message.answer(f'Поехали! Ходит {data["player1"]} {data["smile1"]}'  , reply_markup= gb.get_g_board())
    #await state.set_state(process.game_in_process)

@router.callback_query(process.game_players_ready)
async def sign(callback: CallbackQuery, state: FSMContext):
    num = int(callback.data.split('_')[1])
    # if gb.game_over(gb.g_board, 'x'):
    #     await callback.message.answer(f'Победили x!')
    # elif gb.game_over(gb.g_board, '0'):
    #     await callback.message.answer(f'Победили o!')
    # else:
   # data = await state.get_data()
    if gb.g_board[num] == '':
        if gb.move % 2 == 0:
            gb.g_board[num] = 'x'
            gb.move+=1
            await callback.message.answer(f'Ходит {data["player2"]} {data["smile2"]}', reply_markup=gb.get_g_board())
            if gb.game_over(gb.g_board, 'x') == 'x':
                await callback.message.answer(f'Победил игрок {data["player1"]} {data["smile1"]}!')
                await callback.message.answer('Чтобы играть снова напишите /play')
                await state.set_state(process.game_players_ready)
            elif gb.game_over(gb.g_board, 'x') == 'Piece':
                await callback.message.answer(f'Ничья! {data["smile1"]} 🤝 {data["smile2"]}')
                await callback.message.answer('Чтобы играть снова напишите /play')
                await state.set_state(process.game_players_ready)

        else:
            gb.g_board[num] = '0'
            gb.move += 1
            await callback.message.answer(f'Ходит {data["player1"]} {data["smile1"]}', reply_markup= gb.get_g_board())
            if gb.game_over(gb.g_board, '0') == '0':
                await callback.message.answer(f'Победил игрок {data["player2"]} {data["smile2"]}!')
                await callback.message.answer('Чтобы играть снова напишите /play')
                await state.set_state(process.game_players_ready)
            elif gb.game_over(gb.g_board, '0') == 'Piece':
                await callback.message.answer(f'Ничья! {data["smile1"]} 🤝 {data["smile2"]}')
                await callback.message.answer('Чтобы играть снова напишите /play')
                await state.set_state(process.game_players_ready)


async def start():
    bot: Bot = Bot(token=BOT_TOKEN)
    dp: Dispatcher = Dispatcher()

    dp.include_router(router=router)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())
