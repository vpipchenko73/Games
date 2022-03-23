from random import randint
from time import sleep


class BoardException(Exception):
    pass


class BoardOutExeption(BoardException):
    def __str__(self):
        return "БАБАХ МИМО ! )))))"


class BoardUsedException(BoardException):
    def __str__(self):
        return "ДВА СНАРЯДА В ОДНУ ВОРОНКУ ! ((("


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x},{self.y})"


class Ship:
    def __init__(self, nos, l, o):
        self.nos = nos
        self.l = l
        self.o = o
        self.lives = l

    def __repr__(self):
        return f"Ship[{self.nos}:{self.l}:{self.o}]"

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            x1 = self.nos.x - 1
            y1 = self.nos.y - 1
            if self.o:
                x1 += i
            else:
                y1 += i
            ship_dots.append(Dot(x1, y1))
        return ship_dots


class Pole:
    def __init__(self, vid=False):
        self.vid = vid
        self.count = 0
        self.fiend = [[" O"] * 6 for _ in range(6)]
        self.busu = []
        self.ships = []

    def out(self, d):
        return not ((0 <= d.x <= 5) and (0 <= d.y <= 5))

    def oreol(self, ship, verb=False): # обозначение контуров кораблей
        delta = [(1, -1), (1, 0), (1, 1),
                 (0, -1), (0, 0), (0, 1),
                 (-1, -1), (-1, 0), (-1, 1)]
        for d in ship.dots:
            for dx, dy in delta:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busu:
                    if verb:
                        self.fiend[cur.x][cur.y] = " ."
                    self.busu.append(cur)

    def add_ship(self, ship): # добавление кораблей
        for d in ship.dots:
            if self.out(d) or d in self.busu:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.fiend[d.x][d.y] = " ■"
            self.busu.append(d)
        self.ships.append(ship)
        self.oreol(ship)

    def shot(self, d): # обработка выстрелов
        if self.out(d):
            raise BoardOutExeption()
        if d in self.busu:
            raise BoardUsedException()
        self.busu.append(d)
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.fiend[d.x][d.y] = " X"
                if ship.lives == 0:
                    self.count += 1
                    self.oreol(ship, verb=False)  # verb=False
                    print("Корабль уничтожен !")
                    return True
                else:
                    print("Корабль ранен !")
                    return True
        self.fiend[d.x][d.y] = " ."
        print("БАБАХ МИМО !")
        return False

    def begin(self):
        self.busu = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        print(f"Думаю )))")
        while True:
            d = Dot(randint(0, 5), randint(0, 5))
            if not (d in g.us.board.busu):
                break
        sleep(randint(0, 5)) # введение случайной задержке при выстреле компьютера
        print(f"Ход ИИ - {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self): # ввод координат выстрела
        while True:
            coords = input("Ваш выстрел -->>").split('/')
            if len(coords) != 2:  # проверка длины введенной строки
                print(f"Координаты ({coords}) не соответвуют требуемому формату  повторите ход")
                continue
            x, y = coords
            if not (x.isdigit()) or not (y.isdigit()):  # проверка ввода числа или нет
                print(f"Координаты ({x}/{y}) не соответвуют требуемому формату  повторите ход")
                continue
            else:
                x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


class Game:
    def rules(self):
        print(f"******************************************************************")
        print(f"*          6/6       ИГРА Морской Бой         6/6                *")
        print(f"*               Противник - электронный БАЛБЕС                   *")
        print(f"*        формат ввода координат - № строки/№ столбца             *")
        print(f"******************************************************************")

    def tru_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Pole()
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, 6), randint(0, 6)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.tru_board()
        return board

    def __init__(self):
        pl = self.random_board()
        co = self.random_board()
        co.vid = True  # Режим  невидимости кораблей на поле при True
        pl.vid = False
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def __str__(self): # вывод на печать досок пользователя и компьютера
        res = f"{'     Доска Пользователя '}             {' Доска Компьютера '}  "
        res += f"\n {'   1   2   3   4   5   6  '}     {'   1   2   3   4   5   6  '} "
        for i in range(6):
            s_us = ' |'.join(g.us.board.fiend[i])
            s_ai = ' |'.join(g.ai.board.fiend[i])
            if g.us.board.vid:
                s_us = s_us.replace(" ■", " O")
            if g.ai.board.vid:
                s_ai = s_ai.replace(" ■", " O")
            res += f"\n {i + 1}{'|'}{s_us}{' |'}     {i + 1}{'|'}{s_ai}{' |'}"
        return res

    def loop(self):
        num = 0
        while True:
            print(g)
            if num % 2 == 0:
                print("ХОДИТ ПОЛЬЗОВАТЕЛЬ")
                repeat = self.us.move()
            else:
                print("ХОДИТ КОМПЬЮТЕР")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai.board.count == 7:
                print("ПОЛЬЗОВАТЕЛЬ ВЫИГРАЛ !")
                print(g)
                break
            if self.us.board.count == 7:
                print("КОМПЬЮТЕР ВЫИГРАЛ !")
                print(g)
                break
            num += 1

    def start(self):
        self.rules()
        self.loop()


g = Game()
g.start()
