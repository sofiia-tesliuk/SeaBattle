import random
import string


def read_file(path):
    """
    (str) -> (list)
    Reads data of battle field.
    True if there is ship by current coordinates.
    """
    try:
        with open(path, 'r', encoding='UTF-8', errors='ignore') as file:
            field = file.read().split('\n')
            field = [row + ' ' * (10 - len(row)) for row in field]
            return field
    except FileNotFoundError:
        print("There is no file with such name.")


def is_valid(field):
    """
    (list) -> (bool)
    Returns if field is right.
    If not, then AssertionError.
    """
    def right_ship(crd):
        """
        (tuple) -> (bool, size)
        Returns if ship is correct and size of this ship.
        """
        if (has_ship(field, (crd[0] - 1, crd[1])) or
            has_ship(field, (crd[0] + 1, crd[1]))) and \
                (has_ship(field, (crd[0], crd[1] - 1)) or
                 has_ship(field, (crd[0], crd[1] + 1))):
            print("Invalid shape of ships.")
            return (False, 0)
        return (True, ship_size(field, crd))

    assert len(field) == 10, "Invalid size of field."
    for row in field:
        assert len(row) == 10, "Invalid size of field."
        for el in row:
            assert el in [' ', '*', 'X'], "Invalid chars in field"

    # Checking ships in field
    ships = {1: 0, 2: 0, 3: 0, 4: 0}
    field = new_field(field)
    for i in range(1, 11):
        for j in range(1, 11):
            try:
                ship_info = right_ship((i, j))
                if not ship_info[0]:
                    return False
                if ship_info[1] != 0:
                    # Increase number of ships with such size
                    ships[ship_info[1]] += 1
            except KeyError:
                return False
    return ships == {1: 4, 2: 6, 3: 6, 4: 4}


def new_field(field):
    """
    (list) -> (list)
    Creates new field, more comfortable for further process.
    Has empty frame.
    """
    field = [[el == ('*' or 'X') for el in row] for row in field]
    field = [[False] + row + [False] for row in field]
    field = [[False] * 12] + field + [[False] * 12]
    return field


def normal_coordinates(crd):
    """
    (tuple) -> (tuple)
    Returns coordinates with first coordinate as int.
    """
    if not isinstance(crd[0], int):
        return (ord(crd[0]) - ord('A') + 1, crd[1])
    else:
        return crd


def valid_coordinates(crd):
    """
    (tuple) -> (bool)
    Returns if coordinates are possible.
    """
    crd = normal_coordinates(crd)
    return (1 <= crd[0] <= 10) and (1 <= crd[1] <= 10)


def has_ship(field, crd):
    """
    (list, tuple) -> bool
    Returns if by there coordinates is ship.
    """
    crd = normal_coordinates(crd)
    return field[crd[0]][crd[1]]


def ship_size(field, crd, pre_crd=(0, 0)):
    """
    (list, tuple) ->  (int)
    Returns size of ship be coordinates.
    """
    crd = normal_coordinates(crd)
    size = 0
    if valid_coordinates(crd) and has_ship(field, crd):
        if (crd[0] - 1, crd[1]) != pre_crd:
            size += ship_size(field, (crd[0] - 1, crd[1]), crd)
        if (crd[0] + 1, crd[1]) != pre_crd:
            size += ship_size(field, (crd[0] + 1, crd[1]), crd)
        if (crd[0], crd[1] - 1) != pre_crd:
            size += ship_size(field, (crd[0], crd[1] - 1), crd)
        if (crd[0], crd[1] + 1) != pre_crd:
            size += ship_size(field, (crd[0], crd[1] + 1), crd)
        size += 1
    return size


def field_to_str(field):
    """
    (list) -> (str)
    Returns string of field.
    Used for printing.
    """
    if isinstance(field[0], str):
        return '\n'.join(field)
    # First line of number coordinates
    line = '  ' + ' '.join([str(x) for x in range(1, 11)]) + '\n'
    for i, row in enumerate(field):
        # Letter coordinate
        line += string.ascii_uppercase[i] + ' '
        for el in row:
            if el:
                line += '* '
            else:
                line += '_ '
        line += '\n'
    return line


def generate_field():
    """
    () -> (list)
    Generating field for sea battle.
    """
    def new_ship(size, number):
        """
        (int) -> changed field.
        Put new ship into field.
        """
        def is_new_ship(crd):
            """
            (tuple) -> bool
            In this coordinates can be new ship 1*1.
            """
            for i in range(crd[0] - 1, crd[0] + 2):
                for j in range(crd[1] - 1, crd[1] + 2):
                    if field[i][j]:
                        return False
            return True

        def continue_ship(crd, size, side):
            """
            (tuple, int, str) -> bool
            Returns if ship with such size and side can be continued.
            """
            # Down
            if side:
                if (10 - crd[0]) >= size:
                    for i in range(crd[0] + 1, crd[0] + size + 2):
                        for j in range(crd[1] - 1, crd[1] + 2):
                            if field[i][j]:
                                return False
                else:
                    return False
            # Right
            else:
                if (10 - crd[1]) >= size:
                    for i in range(crd[0] - 1, crd[0] + 2):
                        for j in range(crd[1] + 1, crd[1] + size + 2):
                            if field[i][j]:
                                return False
                else:
                    return False
            return True

        def new_ship_into_field(point, side, size):
            """
            (list) -> changed field.
            """
            ship = [point]
            # Down
            if side:
                for i in range(1, size):
                    ship.append((point[0] + i, point[1]))
            else:
                for i in range(1, size):
                    ship.append((point[0], point[1] + i))

            for part in ship:
                field[part[0]][part[1]] = (number, not side, size)

        point = (random.randint(1, 10), random.randint(1, 10))
        if is_new_ship(point):
            # 0 -- right, 1 -- down
            side = random.randint(0, 1)
            if continue_ship(point, size - 1, side):
                new_ship_into_field(point, side, size)
            else:
                side = not side
                if continue_ship(point, size - 1, side):
                    new_ship_into_field(point, side, size)
                else:
                    new_ship(size, number)
        else:
            new_ship(size, number)

    field = [[False] * 12 for i in range(12)]
    number = 1
    # For each size put ship
    for size in range(4, 0, -1):
        number_of_ships = 5 - size
        for i in range(number_of_ships):
            new_ship(size, number)
            number += 1

    # Cut from frame
    field = field[1: -1]
    field = list(map(lambda x: x[1: -1], field))
    return field
