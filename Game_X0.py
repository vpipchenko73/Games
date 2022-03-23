# Игра крестики/нолики
def preambula():  # функция  обьявления игры и описание правил
    print(f"***********************************")
    print(f"*    *Игра крестики/нолики*       *")
    print(f"* Игроки по очередно делают ход   *")
    print(f"* путем ввода координат в формате *")
    print(f"* номер строки / номер столбца    *")
    print(f"***********************************")


matrix = [[' '] * 3 for i in range(3)]  # формирование матриц 3х3 и заполнение ее " "


def pole():  # функция вывода поля на консоль
    print(f"___0___1___2__")
    for i in range(3):
        z = (" | ".join(matrix[i]))
        print(f"{i}| {z} |")
    print(f"--------------")


def vvod(igrok):  # функция ввода данных
    while True:
        data = input(igrok + " делайте ход -->>").split('/')
        if len(data) != 2:  # проверка формата ввода
            print(f"Координаты ({data}) не соответвуют требуемому формату  повторите ход")
            continue
        else:
            x, y = data
        if not (x.isdigit()) or not (y.isdigit()):  # проверка ввода числа или нет
            print(f"Координаты ({x}/{y}) не соответвуют требуемому формату  повторите ход")
            continue
        else:
            x = int(x)  # пребразование стороковых в int
            y = int(y)
        if not (0 <= x <= 2 and 0 <= y <= 2):  # проверка попадают ли коорд в диапазон
            print(f"Координаты {x}/{y} вне диапазона повторите ход")
            continue
        if matrix[x][y] != " ":  # проверка занятости клетки
            print(f"Клетка занята ({matrix[x][y]}) повторите ход")
            continue
        return x, y


def analiz(igrok, igrok1):
    syndrom3 = ""
    syndrom4 = ""
    for i in range(3):
        syndrom1 = ""
        syndrom2 = ""
        syndrom3 += matrix[i][i]
        syndrom4 += matrix[i][2 - i]
        for j in range(3):
            syndrom1 += matrix[i][j]
            syndrom2 += matrix[j][i]
        if syndrom1 == igrok1 * 3 or syndrom2 == igrok1 * 3:
            print(f"Стоп игра победили {igrok}")
            return 1
            break
    if syndrom3 == igrok1 * 3 or syndrom4 == igrok1 * 3:
        print(f"Стоп игра победили {igrok}")
        return 1
    else:
        return 0


# тело игры

preambula()

for i in range(1, 10):
    if i % 2 == 1:
        igrok = "Крестики"
    else:
        igrok = "Нолики"
    x, y = vvod(igrok)
    if i % 2 == 1:
        matrix[x][y] = "X"
        igrok1 = "X"
    else:
        matrix[x][y] = "0"
        igrok1 = "0"
    pole()
    if analiz(igrok, igrok1):
        break
    if i == 9:
        print("Стоп игра - НИЧЬЯ !")
