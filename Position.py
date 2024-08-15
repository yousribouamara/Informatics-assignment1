# Positions are used to identify cells on the board
import Dimension

def is_proper_position(position):
    """
        Check whether the given position is a proper position.
        - True if and only if the given position is a tuple of length 2
          whose first element is a lower-case letter or the letter 'X',
          and whose second element is a positive integer number.
        ASSUMPTIONS
        - None
    """
    if not isinstance(position, tuple):
        return False
    if len(position) != 2:
        return False
    row, col = position
    if (not isinstance(row, str)) or (len(row) != 1) or \
            ((not str.islower(row)) and (row != 'X')):
        return False
    if not isinstance(col,int) or (col <= 0):
        return False
    return True


def get_row(position):
    """
        Return the row of the given position.
        ASSUMPTIONS
        - The given position is a proper position
    """
    return position[0]


def get_column(position):
    """
        Return the column of the given position.
        ASSUMPTIONS
        - The given position is a proper position
    """
    return position[1]


def nb_of_row(dimension,row):
    """
        Return the number of the row corresponding to the given letter in
        any board with the given dimension.
        - Rows are numbered starting from 1.
        ASSUMPTIONS
        - The given dimension is a proper dimension
        - The given row is a lower case letter or the letter 'X'.
        - The given row is in the range defined by the given dimension.
    """
    if row == "X":
        return Dimension.get_nb_of_rows(dimension)
    else:
        return ord(row) - ord("a") + 1


def id_of_row(dimension,row_nb):
    """
        Return the identification (the letter) of the nth row (n = row_nb) in
        any board with the given dimension.
        ASSUMPTIONS
        - The given dimension is a proper dimension
        - The given number is a positive integer number and does not exceed the
          number of rows of the given dimension.
    """
    if row_nb == Dimension.get_nb_of_rows(dimension):
        return "X"
    else:
        return chr(ord("a") + row_nb - 1)


def is_within_boundaries(dimension, position):
    """
        Check whether the given position is within the boundaries of a
        board of the given dimension.
        - True if and only if (1) the row of the given position is either the
          letter 'X' or its position in the alphabet is in the range of
          the number of rows of the given dimension minus 1, and the column of the
          given position is in the range of the the number of columns of the
          given dimension.
        ASSUMPTIONS
        - The given dimension is a proper dimension.
        - The given position is a proper position
    """
    nb_rows, nb_cols = dimension
    row, col = position
    if (row != "X") and (ord(row)-ord("a")+1 > nb_rows-1):
        return False
    if (col > nb_cols):
        return False
    return True


def left(dimension, position, nb_steps = 1):
    """
        Return the position on any board with the given dimension corresponding to
        the given number of steps to the left of the given position.
        - None is returned if the generated position is outside the boundaries of
          a board with the given dimension.
        ASSUMPTIONS
        - The given dimension is a proper dimension.
        - The given position is a proper position within the boundaries of
          any board with the given dimension.
        - The given number of steps is a positive integer number.
    """
    row, col = position
    if col - nb_steps < 1:
        return None
    else:
        return (row,col-nb_steps)


def right(dimension, position, nb_steps = 1):
    """
        Return the position on any board with the given dimension corresponding to
        the given number of steps to the right of the given position.
        - None is returned if the generated position is outside the boundaries of
          a board with the given dimension.
        ASSUMPTIONS
        - The given dimension is a proper dimension.
        - The given position is a proper position within the boundaries of
          any board with the given dimension.
        - The given number of steps is a positive integer number.
    """
    _, nb_cols = dimension
    row, col = position
    if col + nb_steps > nb_cols:
        return None
    else:
        return (row,col+nb_steps)


def up(dimension, position, nb_steps=1):
    """
        Return the position on any board with the given dimension corresponding to
        the given number of steps above of the given position.
        - None is returned if the generated position is outside the boundaries of
          a board with the given dimension.
        ASSUMPTIONS
        - The given dimension is a proper dimension.
        - The given position is a proper position within the boundaries of
          any board with the given dimension.
        - The given number of steps is a positive integer number.
    """
    nb_rows, _ = dimension
    row, col = position
    if nb_of_row(dimension,get_row(position)) + nb_steps > nb_rows:
        return None
    elif nb_of_row(dimension,get_row(position)) + nb_steps == nb_rows:
        return ("X",col)
    else:
        return (chr(ord(row)+nb_steps),col)


def down(dimension, position, nb_steps=1):
    """
        Return the position on any board with the given dimension corresponding to
        the given number of steps below of the given position.
        - None is returned if the generated position is outside the boundaries of
          a board with the given dimension.
        ASSUMPTIONS
        - The given dimension is a proper dimension.
        - The given position is a proper position within the boundaries of
          any board with the given dimension.
        - The given number of steps is a positive integer number.
    """
    nb_rows, _ = dimension
    row, col = position
    if row == "X":
        return (chr(ord("a")+nb_rows-2), col)
    elif row != "a":
        return (chr(ord(row)-1),col)
    else:
        return None
