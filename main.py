from initial_processing import get_big_data
from models.table_info import get_info

if __name__ == '__main__':
    get_big_data()
    user_input = input('Введите номер раздела 5.3. '
                       '(пример: "5.3.002"), '
                       'номер параграфа 5.2. '
                       '(пример: "5.2.3.07") '
                       'или "Parameter name": ')
    get_info(user_input)
