from aiogram.dispatcher.filters.state import State, StatesGroup


class StatesAdmin(StatesGroup):
    unknown_user = State()

    admin = State()
    add_book_url = State()
    add_book_waiting = State()

    add_question_choice = State()
    add_question = State()
    add_question_name = State()
    add_question_true_answer = State()
    add_question_false_answer = State()
    add_question_choice_create_answers = State()


