operations_list = ["умножить", 'плюс', 'минус']
item1_list = []
item2_list = []
numbers_dict = {"ноль": 0, "один": 1, "два": 2, "три": 3, "четыре": 4, "пять": 5, "шесть": 6, "семь": 7, "восемь": 8,
                "девять": 9, "десять": 10, "одиннадцать": 11, "двенадцать": 12, "тринадцать": 13,
                "четырнадцать": 14, "пятнадцать": 15, 'шестнадцать': 16, 'семнадцать': 17,
                'восемнадцать': 18, "девятнадцать": 19, "двадцать": 20, "тридцать": 30, "сорок": 40,
                "пятьдесят": 50, "шестьдесят": 60, "семьдесят": 70, "восемьдесят": 80, "девяносто": 90, "сто": 100,
                "двести": 200, "триста": 300, "четыреста": 400, "пятьсот": 500, "шестьсот": 600, "семьсот": 700,
                "восемьсот": 800, "девятьсот": 900, "тысяча": 1000, "две тысячи": 2000, "три тысячи": 3000,
                "четыре тысячи": 4000, "пять тысяч": 5000, "шесть тысяч": 6000, "семь тысяч": 7000,
                "восемь тысяч": 8000, "девять тысяч": 9000}
def get_key(val):
    for key, value in numbers_dict.items():
         if val == value:
             return key

def define_operation(string):
    current_operation = ''
    string = string.split()

    if all(item not in operations_list for item in string) :
        print('Некорректно введены данные. Попробуйте еще раз.')
        return run_calc()
    else:
        while 'на' in string:
            string.remove('на')

        next_operation = len(string)
        previous_operation = 0
        index_current_operation = 0
        #выявление отрицательных чисел
        if string[0] == 'минус':
            string[0] = '-'
        for i in range(len(string)-1):
            if (string[i] in operations_list) and (string[i+1] == 'минус'):
                string[i+1] = '-'

        for i in string:
            if i in operations_list:
                if (i == 'умножить') or ((i == 'плюс' or i == 'минус') and 'умножить' not in string):
                    current_operation = i
                    index_current_operation = string.index(i)
                    break
        for i in string[index_current_operation + 1:]:
            if i in operations_list:
                next_operation = string.index(i, index_current_operation+1, len(string))
                break
        for i in string[:index_current_operation]:
            if i in operations_list:
                previous_operation = string.index(i)

        if previous_operation != 0:
            current_string = ' '.join(string[previous_operation+1: next_operation])
        else:
            current_string = ' '.join(string[previous_operation: next_operation])

        return calc(string, current_string, current_operation, previous_operation, next_operation)

def calc(string, current_string, current_operation, previous_operation, next_operation):
    error_flag = False
    item1_list, item2_list = [], []
    items = current_string.split(current_operation)
    # нужно разделить всё по пробелам, но ''+'тысяч' должно быть единым элементом
    for item in items[0].split():
        if ((item.strip() in numbers_dict.keys()) and ('тысяч' not in item)) or (item.strip() == '-'):
            item1_list.append(item.strip())
        elif 'тысяч' in item:
            item1_list[-1] += ' ' + item.strip()
        else:
            print('Данные введены некорректно. Попробуйте ещё раз.')
            error_flag = True
    for item in items[1].split():
        if ((item.strip() in numbers_dict.keys()) and ('тысяч' not in item)) or (item.strip() == '-'):
            item2_list.append(item.strip())
        elif 'тысяч' in item:
            item2_list[-1] += ' ' + item.strip()
        else:
            print('Данные введены некорректно. Попробуйте ещё раз')
            error_flag = True

    if error_flag:
        return run_calc()
    else:
        if item1_list[0] == '-':
            item1_list = [numbers_dict[i] for i in item1_list[1:]]
            x1 = sum(item1_list) * (-1)
        else:
            item1_list = [numbers_dict[i] for i in item1_list]
            x1 = sum(item1_list)

        if item2_list[0] == '-':
            item2_list = [numbers_dict[i] for i in item2_list[1:]]
            x2 = sum(item2_list) * (-1)
        else:
            item2_list = [numbers_dict[i] for i in item2_list]
            x2 = sum(item2_list)

        if current_operation == 'плюс':
                res = x1 + x2
        elif current_operation == 'минус':
                res = x1 - x2
        elif current_operation == 'умножить':
                res = x1 * x2

        res_list = []

        if res < 0:
            res_list.append('минус')
            res *= -1

        if res < 20:
            res_list.append(get_key(res))
        else:
            res = str(res)
            for i in range(len(res)):
                res_list.append(get_key(int(res[i]) * 10**(len(res)-i -1)))

        if len(res_list) > 1:
            while 'ноль' in res_list:
                res_list.remove('ноль')
        operation_result = ' '.join(res_list)

        if previous_operation != 0:
            del string[previous_operation+1: next_operation]
            string.insert(previous_operation + 1, operation_result)
        else:
            del string[previous_operation: next_operation]
            string.insert(previous_operation, operation_result)

        if all(item not in operations_list for item in string):
            string = ' '.join(string)
            return string
        else:
            string = ' '.join(string)
            return define_operation(string)

def check_brackets(string):
    if ('скобка' in string) and ('открывается' in string) and ('закрывается' in string):
        for i in range(len(string)):
            if string[i] == 'открывается':
                start_bracket_index = i
            if string[i] == 'закрывается':
                end_bracket_index = i
                break
        instead_brackets = define_operation(' '.join(string[start_bracket_index + 1: end_bracket_index - 1]))
        if instead_brackets != None:
            del string[start_bracket_index - 1: end_bracket_index + 1]
            string.insert(start_bracket_index - 1, instead_brackets)
            return check_brackets(string)
    else:
        #if all(item not in operations_list for item in string):
            #print(' '.join(string))
        #else:
        if define_operation(' '.join(string)) != None:
            print(define_operation(' '.join(string)))

def run_calc():
    my_string = input().split()
    return check_brackets(my_string)

run_calc()

# Добавить, что если после знака операции ничего нет то данные введены некорректно
#скобка открывается скобка открывается пять плюс шесть минус минус три скобка закрывается умножить на три скобка закрывается плюс два минус сто двадцать