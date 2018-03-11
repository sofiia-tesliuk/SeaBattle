import task_1 as battleship
import string


class Game:
    def __init__(self, number_of_players=2):
        """
        Creating new game.
        :param number_of_players: number of players in game.
        """
        # list of fields of players
        self.__fields = []
        self.__players = []
        self.__number_of_players = number_of_players
        for i in range(number_of_players):
            self.__players.append(Player(i + 1))
            self.__fields.append(Field())
        # Player going to move
        self.__current_player = 0
        self.__game_over = False

    def read_position(self, index):
        """
        Reads coordinates, where player want to hit.
        :param index: player index (int)
        :return: tuple of two integers (coordinates)
        """
        return self.__players[index].read_position()

    def shoot_at(self, index, crd):
        """
        Returns have players shoot at opponents's ship.
        :param index: player index (int)
        :param crd: coordinates to shoot (tuple)
        :return: bool
        """
        return self.__fields[index].shoot_at(crd)

    def won_game(self, index):
        """
        :param index: player index
        :return: have won current player (bool)
        """
        return self.__fields[self.next_player()].hit_all_ships

    def field_without_ships(self, index):
        """
        :param index: player index
        :return: field without ships of current player (str)
        """
        return self.__fields[index].field_without_ships()

    def field_with_ships(self, index):
        """
        :param index: player index
        :return: field with ships of current player (str)
        """
        return self.__fields[index].field_with_ships()

    def next_player(self):
        """
        :return: object of next to move player.
        """
        return (self.__current_player + 1) % self.__number_of_players

    def already_checked(self, index, crd):
        """
        :param index: player index
        :param crd: coordinates to shoot (tuple)
        :return: have player already shoot at this point.
        """
        checked = self.__fields[index].checked[crd[0]][crd[1]]
        if checked:
            print('You have already checked this point.')
        return checked

    def show_all_fields(self):
        """
        After finished game.
        :prints: fields of all players with ships.
        """
        print(self.__players[self.__current_player].message_won())
        for index in range(self.__number_of_players):
            print(self.__players[index].message_field())
            print(self.__fields[index].field_with_ships())

    def play(self):
        """
        Start play after initialisation of game.
        """
        while not self.__game_over:
            print(self.field_without_ships(self.next_player()))
            while True:
                crd = self.read_position(self.__current_player)
                if not self.already_checked(self.next_player(), crd):
                    break
            if not self.shoot_at(self.next_player(), crd):
                self.__current_player = self.next_player()
            else:
                self.__game_over = self.won_game(self.__current_player)
        self.show_all_fields()


class Player:
    def __init__(self, index):
        """
        Initialisation
        :param index: player index
        """
        self.__name = input('Enter your name, player {}: '.format(index))

    def read_position(self):
        """
        Reads coordinates, where player want to hit.
        :return: tuple of two integers (coordinates)
        """
        position = input('{}, enter coordinates: '.format(self.__name)).strip()
        try:
            i = (ord(position[0].upper()) - ord('A'))
            j = int(position[1:])
            assert (0 <= i < 10) and (0 < j <= 10)
            return (i, j - 1)
        except (ValueError, AssertionError, IndexError):
            print('Coordinates should be like: A1')
            return self.read_position()

    def message_won(self):
        """
        :return: Message that this player has won.
        """
        return '\nYou won this game, {}!\n'.format(self.__name)

    def message_field(self):
        """
        :return: field with ships of player
        """
        return "{}'s field:".format(self.__name)


class Field:
    def __init__(self):
        """
        Initialisation
        """
        self.__ships = self.generate_field()
        self.checked = [[False] * 10 for i in range(10)]
        self.__number_of_hit_ships = 0
        self.hit_all_ships = False

    def checked_frame(self, ship):
        """
        :param ship:
        :changes: add to field frame of checking around
        completely destroyed ship.
        """
        size = ship.ship_size()
        for i in range(ship.bow[0] - 1, ship.bow[0] + size[0] + 1):
            for j in range(ship.bow[1] - 1, ship.bow[1] + size[1] + 1):
                if battleship.valid_coordinates((i, j)):
                    self.checked[i][j] = True

    def shoot_at(self, crd):
        """
        Returns have players shoot at opponents's ship.
        Prints some information about shoot.
        :param crd: coordinates to shoot (tuple)
        :return: bool
        """
        self.checked[crd[0]][crd[1]] = True
        ship = self.__ships[crd[0]][crd[1]]
        if ship:
            ship.shoot_at(crd)
            print('Hit!')
            if ship.completely_hit:
                self.checked_frame(ship)
                self.__number_of_hit_ships += 1
                if self.__number_of_hit_ships == 10:
                    self.hit_all_ships = True
                print('You destroyed whole ship!')
            return True
        else:
            print('Missed.')
            return False

    def field_without_ships(self):
        """
        :return: (str) field without ships.
        """
        line = '\n  ' + ' '.join([str(x) for x in range(1, 11)]) + '\n'
        for i, row in enumerate(self.__ships):
            # Letter coordinate
            line += string.ascii_uppercase[i] + ' '
            for j, ship in enumerate(row):
                if self.checked[i][j]:
                    if ship:
                        if ship.completely_hit:
                            line += '■ '
                        else:
                            line += 'X '
                    else:
                        line += '• '
                else:
                    line += '□ '
            line += '\n'
        return line

    def field_with_ships(self):
        """
        :return: (str) field with ships.
        """
        line = '  ' + ' '.join([str(x) for x in range(1, 11)]) + '\n'
        for i, row in enumerate(self.__ships):
            # Letter coordinate
            line += string.ascii_uppercase[i] + ' '
            for j, ship in enumerate(row):
                if ship:
                    if self.checked[i][j]:
                        if ship.completely_hit:
                            line += '■ '
                        else:
                            line += 'X '
                    else:
                        line += '* '
                else:
                    line += '  '
            line += '\n'
        return line

    def generate_field(self):
        """
        :return: generated new field.
        """
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
        """
        Initialisation
        :param bow: coordinate of up-left part
        :param horizontal: bool
        :param length: int
        """
        # Coordinate of up-left part
        self.bow = bow
        self.horizontal = horizontal
        self.__length = length
        self.__hit = [False] * length
        self.completely_hit = False

    def shoot_at(self, crd):
        """
        Some process after shoot.
        :param crd:
        """
        self.__hit[crd[self.horizontal] - self.bow[self.horizontal]] = True
        self.completely_hit = self.__hit == [True] * self.__length

    def ship_size(self):
        """
        :return: size of ship.
        """
        size = [1, 1]
        size[self.horizontal] = self.__length
        return size


def main():
    """
    Main program.
    """
    print("This is a game 'SEA BATTLESHIP'")
    try:
        number_of_players = int(input('Enter number of players: '))
        assert number_of_players > 0
    except (TypeError, AssertionError, ValueError):
        print('Must be natural number. Please, try again.\n')
        main()

    game = Game(number_of_players)
    game.play()


if __name__ == "__main__":
    main()
