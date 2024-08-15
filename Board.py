import Color
import Dimension
import Position
import Block


def is_proper_board(board):
    """
        Check whether the given board is a proper board.
        - ...
        ASSUMPTIONS
        - None
        NOTE
        - You need to work out the conditions yourself as they depend on how
          you store the state of a board.
        (as they depend on the internal representation you have chosen for the board)
    """
    if not isinstance(board, tuple):
        return False
    if len(board) != 2:
        return False
    dimension, blocks = board
    if not Dimension.is_proper_dimension(dimension):
        return False
    if not isinstance(blocks, dict):
        return False;
    for position in dict.keys(blocks):
        # Each position must be a proper position
        if not Position.is_within_boundaries(dimension, position):
            return False
        # Each block must be a proper block for the dimension of the given board.
        block = dict.get(blocks, position)
        if not Block.is_proper_block_for_dimension(block, dimension):
            return False
        left_position = Position.left(dimension, position)
        # Each block must occupy a contiguous sequence of cells of a single
        # row. The length of that sequence must be equal to the length of
        # the block.
        # This check is only done for the leftmost position of the block.
        if (left_position is None) or \
                (left_position not in blocks) or \
                (dict.get(blocks, left_position) is not block):
            next_position = Position.right(dimension, position)
            for nb_cells in range(1, Block.get_length(block)):
                if dict.get(blocks, next_position, None) is not block:
                    return False
                next_position = Position.right(dimension, next_position)
            if (next_position is not None) and \
                    (dict.get(blocks, next_position, None) is block):
                return False
    return True


def make_board(dimension):
    """
        Return a new board of the given dimension without any blocks yet.
        ASSUMPTIONS
        - The given dimension is a proper dimension.
    """
    return (dimension, {})


def copy_board(board):
    """
        Return a copy of the given board loaded with copies of the blocks on
        the given board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    import copy
    return (board[0], copy.copy(board[1]))


def get_dimension(board):
    """
        Return the dimension of the given board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    return board[0]


def get_block_at(board, position):
    """
        Return the block occupying the given position of the given board.
        - The function returns None if (1) the given position is outside the
          boundaries of the given board, or if (2) no block occupies the
          given position of the given board
        ASSUMPTIONS
        - The given board is a proper board.
        - The given position is a proper position.
    """
    if not Position.is_within_boundaries(get_dimension(board), position):
        return None
    _, cells = board
    return dict.get(cells, position, None)


def is_free_at(board, position):
    """
      Check whether the cell at the given position on the given board is free.
      - True if and only if (1) the given position is within the boundaries of
        the given board, and (2) none of the blocks on the board occupies the
        given position.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given position is a proper position.
    """
    return Position.is_within_boundaries(get_dimension(board), position) and \
           get_block_at(board, position) is None


def get_leftmost_position_of(board, block):
    """
        Return the leftmost position occupied by the given block on the given board.
        - The function returns None if the given block is not loaded on the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block for the dimension of the given board.
    """
    current_position = ("a", 1)
    while current_position is not None:
        current_block = get_block_at(board, current_position)
        if current_block is block:
            return current_position
        elif current_block is None:
            step = 1
        else:
            step = Block.get_length(current_block)
        next_position = Position.right(get_dimension(board), current_position, step)
        if next_position is not None:
            current_position = next_position
        else:
            current_position = \
                Position.up(get_dimension(board), (Position.get_row(current_position), 1), 1)
    return None


def get_all_positions_of(board, block):
    """
        Return a tuple containing all the positions of all the cells occupied by
        the given block on the given board.
        - Positions are ordered from left to right in the resulting tuple.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block for the dimension of the given board.
        - The given block is loaded on the given board.
    """
    current_position = get_leftmost_position_of(board, block)
    result = [current_position]
    for nb_cells in range(1, Block.get_length(block)):
        current_position = Position.right(get_dimension(board), current_position)
        list.append(result, current_position)
    return tuple(result)


def get_random_position_for(board, block, row="a"):
    """
        Return a position in the given row of the given board at which the given
        block can be placed without overlapping with blocks already on the given board.
        - The function returns None if no position exists to place the given block
          in the given row.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block for the given board.
        - The given row is within the boundaries of the given board.
    """
    import random
    nb_columns = Dimension.get_nb_of_columns(get_dimension(board))
    random_columns = random.sample(range(1, nb_columns + 1), nb_columns)
    for column in random_columns:
        if can_accept_block_at(board, block, (row, column)):
            return (row, column)
    return None


def get_all_blocks_in_row(board, row):
    """
        Return a list of all the blocks in the given row of the given board.
        - Each block in the given row is stored exactly once in the resulting
          list.
        - The blocks are stored in the resulting list as they occur in the given
          row in the order from left to right.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given row is within the boundaries of the given board.
    """
    result = []
    current_position = (row, 1)
    while current_position is not None:
        block_at_position = get_block_at(board, current_position)
        if (block_at_position is not None):
            list.append(result, block_at_position)
            nb_steps = Block.get_length(block_at_position)
        else:
            nb_steps = 1
        current_position = Position.right(get_dimension(board), current_position, nb_steps)
    return result


def get_length_largest_gap_in_row(board, row):
    """
        Return the length of the largest gap (largest consecutive sequence of
        empty cells) in the given row on the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given row is within the range of the given board.
    """
    length_largest_gap_so_far = 0
    length_current_gap = 0
    current_position = (row, 1)
    while current_position is not None:
        if is_free_at(board, current_position):
            length_current_gap += 1
            current_position = Position.right(get_dimension(board), current_position)
        else:
            if length_current_gap > length_largest_gap_so_far:
                length_largest_gap_so_far = length_current_gap
            length_current_gap = 0
            length_current_block = Block.get_length(get_block_at(board, current_position))
            current_position = \
                Position.right(get_dimension(board), current_position, length_current_block)
    if length_current_gap > length_largest_gap_so_far:
        length_largest_gap_so_far = length_current_gap
    return length_largest_gap_so_far


def is_empty_row(board, row):
    """
        Check whether the given row on the given board is empty.
        - True if and only if the given row does not contain any block.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given row is within the range of the given board.
    """
    return get_all_blocks_in_row(board, row) == []


def is_full_row(board, row):
    """
        Check whether the given row on the given board is completely filled
        with blocks.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given row is within the range of the given board.
    """
    current_position = (row, 1)
    while current_position is not None:
        block_at_current_position = get_block_at(board, current_position)
        if block_at_current_position is None:
            return False
        current_position = \
            Position.right(get_dimension(board), current_position,
                           Block.get_length(block_at_current_position))
    return True


def get_all_full_rows(board):
    """
        Return a frozen set of the letters of all the rows that are completely
        filled with blocks.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    result = set()
    current_position = ("a", 1)
    while current_position is not None:
        if is_full_row(board, Position.get_row(current_position)):
            set.add(result, Position.get_row(current_position))
        current_position = Position.up(get_dimension(board), current_position)
    return frozenset(result)


def get_all_blocks(board):
    """
        Return a list of all the blocks on the given board.
        - Each block on the given board is stored exactly once in the resulting
          list.
        - The blocks are ordered according to their position on the board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    result = []
    current_position = ("a", 1)
    while current_position is not None:
        blocks_in_current_row = get_all_blocks_in_row(board, Position.get_row(current_position))
        list.extend(result, blocks_in_current_row)
        current_position = Position.up(get_dimension(board), current_position)
    return result


def contains_block(board, block):
    """
        Check whether the given board contains the given block.
        - The function returns True if and only if one of the blocks on the
          given board is the same (referential equality) as the given block.
        - The function returns False if none of the blocks is the same as the
          given block, even if some blocks on the board are identical (same length,
          same type, same position) to the given block.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
    """
    for stored_block in get_all_blocks(board):
        if stored_block is block:
            return True
    return False


def can_accept_block_at(board, block, position):
    """
      Check whether the given board can accept the given block at the given
      position.
      - True if and only if (1) the given block is a proper block for
        the dimension of the given board, (2) the given block is not already
        loaded on the given board and (3) all the cells that would
        be occupied by the given block are free and within the boundaries
        of the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        - The given position is a proper position.
    """
    if not Block.is_proper_block_for_dimension(block, get_dimension(board)):
        return False
    if not Position.is_within_boundaries(get_dimension(board), position):
        return False
    if contains_block(board, block):
        return False
    for nb_cells in range(0, Block.get_length(block)):
        if position is None:
            return False
        if not is_free_at(board, position):
            return False
        position = Position.right(get_dimension(board), position)
    return True


def add_block_at(board, block, position):
    """
        Add the given block at the given position on the given board.
        - If the given position is equal to (r,c), the given block will occupy the
          cells (r,c), (r,c+1), ..., (r,c+L-1) on the given board, in which L denotes
          the length of the given block.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        - The given position is a proper position.
        - The given board can accept the given block at the given position.
    """
    dimension, cells = board
    for nb_cells in range(0, Block.get_length(block)):
        cells[position] = block
        position = Position.right(dimension, position)


def remove_block_from(board, block):
    """
        Remove the given block from the given board.
        - No other blocks change their position as a result of removing the given
          block.
        - Nothing happens if the given block is not loaded on the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
    """
    if contains_block(board, block):
        _, blocks = board
        positions_of_block = get_all_positions_of(board, block)
        for position in positions_of_block:
            del blocks[position]


def is_airborne(board, block):
    """
        Check whether the given block is airborne on the given board.
        - True if and only if the given block is (1) not positioned on the bottom row
          of the given board, and (2) not fully or partially on top of some other block
          on the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        - The given block is loaded on the given board.
    """
    occupied_positions = get_all_positions_of(board, block)
    for position in occupied_positions:
        position_down = Position.down(get_dimension(board), position)
        if (position_down is None) or (not is_free_at(board, position_down)):
            return False
    return True


def get_adjacent_blocks_above(board, block):
    """
        Return a list of all the blocks on the given board directly adjacent
        to the top of the given block on the given board.
        - Each block in the resulting list has some part of its bottom border
          in common with some part of the top border of the given block.
        - The blocks in the resulting list are ordered in ascending order of their
          position.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        - The given block is loaded on the given board.
        NOTE
        - This function must be worked out in an ITERATIVE way.
    """
    result = []
    position_above = \
        Position.up(get_dimension(board), get_leftmost_position_of(board, block))
    nb_steps_to_take = Block.get_length(block)
    while (position_above is not None) and (nb_steps_to_take > 0):
        block_at_position_above = get_block_at(board, position_above)
        if block_at_position_above is not None:
            list.append(result, block_at_position_above)
            nb_steps = Block.get_length(block_at_position_above) - \
                       (Position.get_column(position_above) - \
                        Position.get_column(get_leftmost_position_of(board, block_at_position_above)))
        else:
            nb_steps = 1
        position_above = Position.right(get_dimension(board), position_above, nb_steps)
        nb_steps_to_take -= nb_steps
    return result


def get_adjacent_block_left(board, block):
    """
        Return the block adjacent to the left of the given block on the given board.
        - None is returned if no such block exists.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        - The given block is loaded on the given board.
    """
    adjacent_position_left = \
        Position.left(get_dimension(board), get_leftmost_position_of(board, block))
    if adjacent_position_left is None:
        return None
    return get_block_at(board, adjacent_position_left)


def get_adjacent_blocks_below(board, block, from_position=None):
    """
        Return a list of all the blocks on the given board directly adjacent
        to the bottom of the given block on the given board.
        - Each block in the resulting list has some part of its top border
          in common with some part of the bottom border of the given block.
        - The blocks in the resulting list are ordered in ascending order of their
          position.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        - The given block is loaded on the given board.
        NOTE
        - This function must be worked out in a recursive way.
    """
    if from_position is None:
        from_position = Position.down(get_dimension(board), get_leftmost_position_of(board, block))
    if (from_position is None) or (Position.get_column(from_position) > \
                                   Position.get_column(get_leftmost_position_of(board, block)) + Block.get_length
                                       (block)-1):
        return []
    block_at_position_below = get_block_at(board, from_position)
    if block_at_position_below is not None:
        result = [block_at_position_below]
        nb_steps = Block.get_length(block_at_position_below) - \
                   (Position.get_column(from_position) - \
                    Position.get_column(get_leftmost_position_of(board, block_at_position_below)))
    else:
        result = []
        nb_steps = 1
    from_position = Position.right(get_dimension(board), from_position, nb_steps)
    if from_position is not None:
        list.extend(result, get_adjacent_blocks_below(board, block, from_position))
    return result


def get_adjacent_block_right(board, block):
    """
        Return the block adjacent to the right of the given block on the given board.
        - None is returned if no such block exists.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        - The given block is loaded on the given board.
    """
    adjacent_position_right = \
        Position.right(get_dimension(board), get_leftmost_position_of(board, block), Block.get_length(block))
    if adjacent_position_right is None:
        return None
    return get_block_at(board, adjacent_position_right)


def get_supporting_blocks(board, block):
    """
        Return a frozen set of all the positions of the blocks on the given board
        directly or indirectly supporting the given block on the given board.
        - The definition of what it means for a block A to directly or indirectly
          support some other block B is given in the documentation of the function
          get_supported_blocks. Obviously if block A is directly or indirectly supporting
          block B, block B is directly or indirectly supported by block A.
        - The resulting set only includes the position of the leftmost cell of each
          of the supporting blocks (and not all positions it occupies).
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        - The given block is loaded on the given board.
        NOTE
        - This function must be worked out in an ITERATIVE way.
    """
    blocks_to_handle = [block]
    handled_block_ids = []
    supporting_block_positions = frozenset()
    while len(blocks_to_handle) > 0:
        current_block = list.pop(blocks_to_handle, len(blocks_to_handle) - 1)
        list.append(handled_block_ids, id(current_block))
        if current_block is not block:
            supporting_block_positions |= \
                frozenset([get_leftmost_position_of(board, current_block)])
        if Position.get_row(get_leftmost_position_of(board, current_block)) != "a":
            block_positions = get_all_positions_of(board, current_block)
            for position in block_positions:
                block_below = get_block_at(board, Position.down(get_dimension(board), position))
                if (block_below is not None) and (id(block_below) not in handled_block_ids) and \
                        (block_below not in blocks_to_handle):
                    list.append(blocks_to_handle, block_below)
    return supporting_block_positions


def get_supported_blocks(board, block, handled_block_ids=None):
    """
        Return a mutable set of all the positions of the blocks on the given board
        directly or indirectly supported by the given block on the given board.
        - A block B directly supports another block S if the top border of at least
          one of B's cells coincides with the bottom border of block S.
        - A block B indirectly supports another block S if it supports at least one
          other block X that directly or indirectly supports block S.
        - The resulting set only includes the position of the leftmost cell of each
          of the supported blocks (and not all positions it occupies).
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        - The given block is loaded on the given board.
        NOTE
        - This function must be worked out in a RECURSIVE way.
        - Leave out the parameter "handled_block_ids" in the skeleton distributed to the
          students.
    """
    if handled_block_ids is None:
        handled_block_ids = []
    list.append(handled_block_ids, id(block))
    supported_block_positions = set()
    if Position.get_row(get_leftmost_position_of(board, block)) != "X":
        blocks_directly_above = get_adjacent_blocks_above(board, block)
        for block_above in blocks_directly_above:
            if id(block_above) not in handled_block_ids:
                set.add(supported_block_positions, get_leftmost_position_of(board, block_above))
                extra_blocks = get_supported_blocks(board, block_above, handled_block_ids)
                set.update(supported_block_positions, extra_blocks)
    return supported_block_positions


def let_fall(board, block):
    """
        Let the given block fall down until it is no longer airborne.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        - The given block is loaded on the given board.
    """
    if is_airborne(board, block):
        new_position_for_block = get_leftmost_position_of(board, block)
        position_below_new_position = \
            Position.down(get_dimension(board), new_position_for_block)
        remove_block_from(board, block)
        while (position_below_new_position is not None) and \
                can_accept_block_at(board, block, position_below_new_position):
            new_position_for_block = position_below_new_position
            position_below_new_position = \
                Position.down(get_dimension(board), position_below_new_position)
        add_block_at(board, block, new_position_for_block)


def let_all_blocks_fall(board):
    """
        Let all the blocks in the given board fall down until none of them is still
        airborne.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    if Dimension.get_nb_of_rows(get_dimension(board)) > 2:
        current_position = ("b", 1)
    else:
        current_position = ("X",1)
    while current_position is not None:
        blocks_in_row = get_all_blocks_in_row(board, Position.get_row(current_position))
        for block in blocks_in_row:
            let_fall(board, block)
        current_position = Position.up(get_dimension(board), current_position)


def let_explode(board, block):
    """
        Let the given block on the given board explode.
        - The function returns the score resulting from the explosion.
        - If the given block is an ordinary block, the given block is removed from
          the given board. The score for having an ordinary block explode is equal
          to the length of that block.
        - If the given block is a fragile block, the given block is replaced on the
          given board by the blocks obtained from splitting the given block. The score
          for having a fragile block explode is equal to twice the length of that block.
        - If the given block is an electrified block, the given block is removed from
          the given board, and all the blocks immediately below and above the given block
          explode. The score for having an electrified block explode is equal to
          the length of that block incremented with the scores of explosions of blocks
          above and below the given block.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        - The given block is loaded on the given board.
    """
    if Block.get_type(block) == Block.ORDINARY:
        remove_block_from(board, block)
        return Block.get_length(block)
    if Block.get_type(block) == Block.FRAGILE:
        position_of_block = get_leftmost_position_of(board, block)
        remove_block_from(board, block)
        replacing_blocks = Block.split_block(block)
        for replacing_block in replacing_blocks:
            add_block_at(board, replacing_block, position_of_block)
            position_of_block = \
                Position.right(get_dimension(board), position_of_block,
                               Block.get_length(replacing_block))
        return 2 * Block.get_length(block)
    elif Block.get_type(block) == Block.ELECTRIFIED:
        adjacent_blocks = \
            get_adjacent_blocks_below(board, block) + get_adjacent_blocks_above(board, block)
        remove_block_from(board, block)
        total_score = Block.get_length(block)
        for block in adjacent_blocks:
            if contains_block(board, block):
                total_score += let_explode(board, block)
        return total_score


def is_stable(board):
    """
        Check whether the given board is stable.
        - True if and only if none of the blocks on the given board are airborne.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    for block in get_all_blocks(board):
        if is_airborne(board, block):
            return False
    return True


def push_all_blocks_in_row_up(board, row):
    """
        Push all the blocks in the given row of the given board one row up.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given row is within the boundaries of the given board.
        - The given row is not the overflow row of the given board.
        - The row above the given row is empty.
    """
    blocks_in_row = get_all_blocks_in_row(board, row)
    for block in blocks_in_row:
        new_position = Position.up(get_dimension(board), get_leftmost_position_of(board, block))
        remove_block_from(board, block)
        add_block_at(board, block, new_position)


def push_all_blocks_up(board):
    """
        Push all the blocks on the given board one row up.
        ASSUMPTIONS
        - The given board is a proper board.
        - The overflow row of the given board is empty.
    """
    for row_nb in range(Dimension.get_nb_of_rows(get_dimension(board)) - 1, 0, -1):
        current_row = Position.id_of_row(get_dimension(board), row_nb)
        push_all_blocks_in_row_up(board, current_row)


def fill_bottom_row(board, max_block_length):
    """
        Fill the bottom row of the given board with new blocks whose length does
        not exceed the given maximum length.
        - Upon completion, there will be at least one free cell in the bottom row and
          it will not be possible to add an additional block of the given maximum
          length to the bottom row.
        ASSUMPTIONS
        - The given board is a proper board.
        - The bottom row of the given board is empty.
        - The given maximum length is at least 2 and does not exceed halve the number
          of columns in the given board.
        NOTE
        - This function must not be worked out by the students.
    """
    nb_filled_cells = 0
    block_to_add = Block.make_random_block(max_block_length)
    position_for_block = get_random_position_for(board, block_to_add)
    while (position_for_block is not None) and \
            (nb_filled_cells + Block.get_length(block_to_add) < \
             Dimension.get_nb_of_columns(get_dimension(board))):
        add_block_at(board, block_to_add, position_for_block)
        nb_filled_cells += Block.get_length(block_to_add)
        block_to_add = Block.make_random_block(max_block_length)
        position_for_block = get_random_position_for(board, block_to_add)


def insert_bottom_row(board, blocks):
    """
        Push all blocks on the given board one row up, and subsequently fill the
        bottom row of the given board with the given sequence of blocks.
        ASSUMPTIONS
        - The given board is a proper board.
        - The overflow row of the given board is empty.
        - Each basic element in the list of blocks ((blocks[I][J]) is a tuple
          involving a (leftmost) position in the bottom row of the board followed by
          a proper block for a board with the given dimension.
        NOTE
        - This function must not be worked out by the students.
    """
    push_all_blocks_up(board)
    for (leftmost_position, block) in blocks:
        add_block_at(board, block, leftmost_position)


def can_move_over(board, block, nb_steps):
    """
        Check whether the given block on the given board can be moved horizontally
        over the given number of steps .
        - The movement is to the left if the given number of steps is negative;
          it is to the right if the given number of steps is positive.
        - True if and only if each of the cells over which the block has to move
          (1) is within the boundaries of the given board and (2) is free.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        - The given block is loaded on the given board.
    """
    if not isinstance(nb_steps, int):
        return False
    current_position = get_leftmost_position_of(board, block)
    if (nb_steps > 0) and (Block.get_length(block) > 1):
        current_position = Position.right(get_dimension(board), current_position, Block.get_length(block) - 1)
    while nb_steps != 0:
        if nb_steps < 0:
            current_position = Position.left(get_dimension(board), current_position)
            nb_steps += 1
        else:
            current_position = Position.right(get_dimension(board), current_position)
            nb_steps -= 1
        if (current_position is None) or (not is_free_at(board, current_position)):
            return False
    return True


def move_block_horizontally(board, block, nb_steps):
    """
        Move the given block on the given board over the given number of steps.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        - The given block is loaded on the given board.
        - The given block can move over the given number of steps.
    """
    leftmost_position = get_leftmost_position_of(board, block)
    if nb_steps < 0:
        new_position = Position.left(get_dimension(board), leftmost_position, -nb_steps)
    else:
        new_position = Position.right(get_dimension(board), leftmost_position, nb_steps)
    remove_block_from(board, block)
    add_block_at(board, block, new_position)


def print_board(board):
    """
        Print the given board on the standard output stream.
        ASSUMPTIONS
        - The given board is a proper board.
        INTERNAL NOTE
        - The body of this function must be included in the skeleton.
    """
    current_position = ("X", 1)
    while current_position is not None:
        for lines in range(0, 2):
            if lines == 1:
                print("\033[1;31;48m" + '{:2}'.format(Position.get_row(current_position)), end="  ")
            else:
                print("\033[1;30;48m" + "  ", end="  ")
            column_position = current_position
            left_position = None
            while column_position is not None:
                current_block = get_block_at(board, column_position)
                right_position = Position.right(get_dimension(board), column_position)
                if current_block is None:
                    print("\033[1;30;48m" + ("|   " if lines == 1 else "----"), end="")
                else:
                    block_symbol = Block.get_symbol(current_block)
                    if (left_position is None) or \
                            (get_block_at(board, left_position) is not current_block):
                        # Leftmost cell of a block.
                        if lines == 1:
                            print("\033[1;" + str(Block.get_color(current_block)) + ";48m|" + block_symbol * 3, end="")
                        else:
                            print("\033[1;30;48m----", end="")
                    else:
                        if lines == 1:
                            print("\033[1;" + str(Block.get_color(current_block)) + ";48m" + block_symbol * 4, end="")
                        else:
                            print("\033[1;30;48m----", end="")
                left_position = column_position
                column_position = right_position
            print("\033[1;30;48m" + ("|" if lines == 1 else "-"))
        current_position = Position.down(get_dimension(board), current_position)
    print("   ", "\033[1;30;48m" + ("-" * (Dimension.get_nb_of_columns(get_dimension(board)) * 4 + 1)))
    print("    ", end="")
    for column in range(1, Dimension.get_nb_of_columns(get_dimension(board)) + 1):
        print("\033[1;30;48m" + '{:3d}'.format(column), end=" ")
    print()

