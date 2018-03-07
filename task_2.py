import task_1 as battleship


class Game:
    def __init__(self, number_of_players=2):
        self.__fields = []
        self.__players = []
        self.__number_of_players = number_of_players
        for i in range(number_of_players):
            self.__players.append(Player(i + 1))
            self.__fields.append(Field())
        self.__current_player = 0
        self.__game_over = False

    def read_position(self, index):
        return self.__players[index].read_position()

    def shoot_at(self, index, crd):
        """
        (int, tuple) -> bool
        """
        return self.__fields[index].shoot_at()

    def won_game(self, index):
        return self.__fields[index].hit_all_ships

    def field_without_ships(self, index):
        return self.__fields[index].field_without_ships()

    def field_with_ships(self, index):
        """
        (int) -> (str)
        """
        return self.__fields[index].field_with_ships()

    def next_player(self):
        return (self.__current_player + 1) % self.__number_of_players

    def already_checked(self, index, crd):
        return self.__fields[index].checked[crd[0]][crd][1]

    def play(self):
        while not self.__game_over:
            print(self.field_without_ships(self.next_player()))
            while True:
                crd = self.read_position(self.__current_player)
                if not self.already_checked(self.__current_player, crd):
                    break
            if not self.shoot_at(self.__current_player, crd):
                self.__current_player = self.next_player()
            else:
                self.__game_over = self.won_game(self.__current_player)


class Player:
    def __init__(self, index):
        self.__name = input('Enter you name, player {}: '.format(index))

    def read_position(self):
        position = input('{}, enter coordinates: '.format(self.__name)).strip()
        i = ord(position[0]) - ord('A')
        try:
            j = int(position[1:])
            assert (0 <= i < 10) and (0 <= j < 10)
            return (i, j)
        except (ValueError, AssertionError):
            print('Coordinates should be like: A1')
            self.read_position()


class Field:
    def __init__(self):
        self.__ships = self.generate_field()
        self.checked = [[False] * 10 for i in range(10)]
        self.__number_of_hit_ships = 0
        self.hit_all_ships = False

    def shoot_at(self, crd):
        self.checked[crd[0]][crd[1]] = True
        ship = self.__ships[crd[0]][crd[1]]
        if ship:
            ship.shoot_at(crd)
            if ship.completely_hit:
                self.__number_of_hit_ships += 1
                if self.__number_of_hit_ships == 10:
                    self.hit_all_ships = True
            print('Hit!')
            return True
        else:
            print('Missed.')
            return False

    def field_without_ships(self):
        # Do something with __field
        pass

    def field_with_ships(self):
        # Do something with __ships
        pass

    def generate_field(self):
        field = battleship.generate_field()
        new_field = [[None] * 10 for i in range(10)]
        founded_ships = dict()
        for i, row in enumerate(field):
            for j, cell in enumerate(row):
                if cell:
                    try:
                        new_field[i][j] = founded_ships[cell[0]]
                    except KeyError:
                        founded_ships[cell[0]] = \
                            Ship((i, j), cell[1], cell[2])
                        new_field[i][j] = founded_ships[cell[0]]
        return new_field


class Ship:
    def __init__(self, bow, horizontal, length):
        # Coordinate of up-left part
        self.bow = bow
        self.horizontal = horizontal
        self.__length = length
        self.__hit = [False] * length
        self.completely_hit = False

    def shoot_at(self, crd):
        if self.horizontal:
            self.__hit[crd[1] - self.bow[1]] = True
        else:
            self.__hit[crd[0] - self.bow[0]] = True
        self.completely_hit =  self.__hit == [True] * self.__length

