
''' Ошибки при создании киниги и вопросов '''
class QuestionError(Exception):
    pass


class ErrorParsePage(QuestionError):
    pass


class ErrorTableOfContentEmpty(ErrorParsePage):
    pass


class ErrorSendData(QuestionError):
    pass


class ErrorGetSectionData(QuestionError):
    pass