from aiogram.dispatcher.filters.state import State, StatesGroup


class StatesAdmin(StatesGroup):
    add_book_url = State()
    add_book_waiting = State()

