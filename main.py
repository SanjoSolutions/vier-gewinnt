from enum import IntEnum

NUMBER_OF_ROWS = 6
NUMBER_OF_COLUMNS = 7
NUMBER_OF_CELLS_TO_WIN = 4


class Player(IntEnum):
    One = 1
    Two = 2


class CellState(IntEnum):
    Empty = 0
    Red = 1
    Yellow = 2


class VierGewinnt:
    def __init__(self):
        self._grid = None
        self._current_player = Player.One
        self.reset()

    def reset(self):
        self._grid = [None] * NUMBER_OF_ROWS
        for row in range(NUMBER_OF_ROWS):
            self._grid[row] = [CellState.Empty] * NUMBER_OF_COLUMNS
        return self._get_state()

    def step(self, action):
        column = action
        self._grid = step(self._grid, column, self._current_player)
        state = self._get_state()
        winner = self.determine_winner()
        done = winner is not None
        if not done:
            self._next_player()
        reward = determine_reward(self._grid, self._current_player)
        return state, reward, done

    def _get_state(self):
        return self._grid

    def get_available_actions(self):
        return get_available_actions(self._grid)

    def determine_winner(self):
        return determine_winner(self._grid)

    def _next_player(self):
        self._current_player = next_player(self._current_player)


def next_player(player):
    return Player((player % len(Player)) + 1)


def previous_player(player):
    return next_player(player)


def get_available_actions(grid):
    return [
        column
        for column
        in range(0, NUMBER_OF_COLUMNS)
        if get_first_empty_row(grid, column) is not None
    ]


def step(grid, column, player):
    column = column
    row = get_first_empty_row(grid, column)
    if row is None:
        raise ValueError('column ' + str(column) + ' is full.')
    grid = copy_grid(grid)
    grid[row][column] = player
    return grid


def copy_grid(grid):
    grid = grid.copy()
    for row in range(0, len(grid)):
        grid[row] = grid[row].copy()
    return grid


def get_first_empty_row(grid, column):
    for row in range(NUMBER_OF_ROWS - 1, -1, -1):
        if grid[row][column] == CellState.Empty:
            return row
    return None


def determine_winner(grid):
    for player in Player:
        for column in range(0, NUMBER_OF_COLUMNS):
            for from_row in range(0, NUMBER_OF_ROWS - NUMBER_OF_CELLS_TO_WIN + 1):
                to_row = from_row + NUMBER_OF_CELLS_TO_WIN - 1
                cells = [
                    grid[row][column]
                    for row
                    in range(from_row, to_row + 1)
                ]
                if match(cells, player):
                    return player

        for row in range(0, NUMBER_OF_ROWS):
            for from_column in range(0, NUMBER_OF_COLUMNS - NUMBER_OF_CELLS_TO_WIN + 1):
                to_column = from_column + NUMBER_OF_CELLS_TO_WIN - 1
                cells = [
                    grid[row][column]
                    for column
                    in range(from_column, to_column + 1)
                ]
                if match(cells, player):
                    return player

        for from_row in range(0, NUMBER_OF_ROWS - NUMBER_OF_CELLS_TO_WIN + 1):
            to_row = from_row + NUMBER_OF_CELLS_TO_WIN - 1
            for from_column in range(0, NUMBER_OF_COLUMNS - NUMBER_OF_CELLS_TO_WIN + 1):
                to_column = from_column + NUMBER_OF_CELLS_TO_WIN - 1

                cells = []
                row = from_row
                column = from_column
                while row <= to_row and column <= to_column:
                    cells.append(grid[row][column])
                    row += 1
                    column += 1
                if match(cells, player):
                    return player

                cells = []
                row = from_row
                column = to_column
                while row <= to_row and column >= from_column:
                    cells.append(grid[row][column])
                    row += 1
                    column -= 1
                if match(cells, player):
                    return player

    return None


def determine_reward(grid, player):
    winner = determine_winner(grid)
    if winner == player:
        reward = 1
    elif winner is not None:  # other player won
        reward = -1
    else:
        reward = 0
    return reward


def is_grid_full(grid):
    for row in range(0, NUMBER_OF_ROWS):
        for column in range(0, NUMBER_OF_COLUMNS):
            if grid[row][column] == CellState.Empty:
                return False
    return True


def match(cells, cell_state):
    return all(cell == cell_state for cell in cells)


def print_state(state):
    for row in state:
        print([cell.value for cell in row])
    print('')
