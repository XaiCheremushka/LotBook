import re


async def remove_index_and_space(input_string: str) -> str:
    pattern = re.compile(r'^\d+\s')

    # Замена совпадения пустой строкой
    result_string = re.sub(pattern, '', input_string)

    return result_string


async def sort_elements_sheet_content(sheet_content: []) -> []:

    def get_index_from_string(s):
        # Извлекаем число-индекс из строки
        index_str = re.match(r'^\d+', s)
        if index_str:
            return int(index_str.group())
        else:
            return float('inf')  # Если индекс отсутствует, ставим бесконечность

    sorted_list = sorted(sheet_content, key=lambda x: get_index_from_string(x))

    return sorted_list
