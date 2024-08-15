import Color
import Dimension
import Position
import Block
import Board


def let_all_full_rows_explode(board):
    """
        Let all the blocks in all the full rows on the given board explode.
        - The function starts with examining the given board collecting all the
          blocks in all rows that are completely filled. Hereafter, it will let
          each of these blocks explode exactly once in ascending order of their
          position.
        - If part of a full row has already exploded because of explosions of
          (electrified) blocks in lower rows, other blocks in that row will still
          explode (even if the row is no longer completely filled).
        - If a fragile block in a full row has already exploded because of explosions
          of (electrified) blocks in lower rows, the replacing blocks will not explode
          on their own. They may, however, explode as a result of other electrified
          blocks exploding.
        - The function returns the score resulting from all explosions.
        ASSUMPTIONS
        - The given board is a proper board.
        NOTE
        - This function is given to the students, such that the backtracking
          algorithm will not behave different because of differences in this algorithm.
    """
    blocks_to_explode = []
    full_rows_sorted = list(Board.get_all_full_rows(board))
    list.sort(full_rows_sorted)
    for row in full_rows_sorted:
        list.extend(blocks_to_explode, Board.get_all_blocks_in_row(board, row))
    total_score = 0
    for block in blocks_to_explode:
        if Board.contains_block(board, block):
            total_score += Board.let_explode(board, block)
    return total_score


def adjust_score(score, level, score_from_explosions, nb_full_rows, nb_columns):
    """
        Return the new score and the new level in view of the given score, the given
        level, the score resulting from explosions that have taken place, the total
        number of full rows in which these explosions took place and the number of
        columns on the board.
        NOTE
        - This function is given to the students. Its details are irrelevant.
    """

    def treshold_for_level(level):
        if level == 1:
            return 11 * nb_columns
        else:
            return treshold_for_level(level - 1) + (10 + level) * nb_columns * level

    extra_score = score_from_explosions * nb_full_rows * level
    score += extra_score
    if score > treshold_for_level(level):
        level += 1
    return (score, level)


def stabilize_board(level, score, board):
    """
        Stabilize the given board and return the updated level and score in view of
        the given level and given score.
        - The function continuously lets all blocks on the given board fall down,
          followed by explosions of all full rows, until the board is stable.
        - The function returns a tuple (l,s) in which l is the new level and s is
          the new score in view of the given level and given score.
        ASSUMPTIONS
        - The given level is a positive integer number.
        - The given score is a non-negative integer number.
        - The given board is a proper board.
        NOTE
        - This function is given to the students, such that the backtracking
          algorithm will not behave different because of differences in this algorithm.
    """
    Board.let_all_blocks_fall(board)
    nb_full_rows = len(Board.get_all_full_rows(board))
    while (nb_full_rows > 0):
        if nb_full_rows > 0:
            score_from_explosions = let_all_full_rows_explode(board)
            score, level = \
                adjust_score(score, level, score_from_explosions, nb_full_rows,
                             Dimension.get_nb_of_columns(Board.get_dimension(board)))
        Board.let_all_blocks_fall(board)
        nb_full_rows = len(Board.get_all_full_rows(board))
    return (level, score)


def get_all_possible_steps(board, block):
    """
       Return a sequence of all possible steps over which the given block can be
       moved on the given board.
       - The steps are in ascending order.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block for the given board.
        - The given block is loaded on the given board.
        NOTE
        - This function must not be included in the skeleton distributed among the students.
    """
    nb_steps = 0
    while Board.can_move_over(board, block, nb_steps - 1):
        nb_steps -= 1
    result = []
    while Board.can_move_over(board, block, nb_steps):
        if nb_steps != 0:
            list.append(result, nb_steps)
        nb_steps += 1
    return result


def get_move_with_highest_score(board, level, score):
    """
        Return the move on the given board that will yield the highest possible score
        in view of the given level and the given score.
        - If different blocks yield the same highest score, the function returns the
          block with the smallest position. If a block yields the same highest score
          with different moves, the function returns the move to the position closest
          to the left border.
        - The function returns a tuple consisting of the block to be moved followed
          by the number of steps to move over. None is returned if no move is possible.
        ASSUMPTIONS
        - The given level is a positive integer number.
        - The given score is a non-negative integer number.
        - The given board is a proper board.
        NOTE
        - This function must not be included in the skeleton distributed among the students.
    """
    highest_score_so_far = None
    all_blocks = Board.get_all_blocks(board)
    for block in all_blocks:
        for nb_steps in get_all_possible_steps(board, block):
            copy_board = Board.copy_board(board)
            Board.move_block_horizontally(copy_board, block, nb_steps)
            _, new_score = stabilize_board(level, score, copy_board)
            if (highest_score_so_far is None) or (new_score > highest_score_so_far):
                highest_score_so_far = new_score
                best_block_so_far = block
                steps_to_move_over = nb_steps
    if highest_score_so_far is None:
        return None
    else:
        return (best_block_so_far, steps_to_move_over)


def play_greedy(blocks, dimension=(8, 10)):
    """
       Play the game in a greedy way on a board with the given dimension,
       using the given blocks to fill the bottom row in each step of the game.
       The function repeatedly shifts all blocks up one row, adds new blocks to the
       bottom row and stabilizes the board, computes the move that yields the highest
       score, and makes that move.
       - The given blocks are collected in a list of which each element is a list of
         blocks to fill the bottom row once.
       - The function computes and executes in each step the move yielding the
         highest score.
       - The function returns a tuple consisting of the total score after all
         the given blocks have been used or as soon as the game has come to an end,
         followed by a list of all the moves that have been made. Each move in the
         latter list is a tuple containing the block to move, followed by the
         distance over which that block has been moved.
       ASSUMPTIONS
       - The given dimension is a proper dimension.
       - Each element in the list of blocks ((blocks[I]) is a sequence that can be
         used to fill the bottom row once in a valid way (i.e., no overlapping
         positions, no remaining gap larger than half the number of columns after
         a complete fill, ...)
       - The elements in the list of blocks (blocks[I]) are used in the order from left
         to right.
       - Each basic element in the list of blocks ((blocks[I][J]) is a tuple
         involving a (leftmost) position in the bottom row of the board followed by
         a proper block for a board with the given dimension.
    """
    current_level, total_score = 1, 0
    the_board = Board.make_board(dimension)
    moves = []
    while (len(blocks) > 0) and Board.is_empty_row(the_board, "X"):
        Board.insert_bottom_row(the_board, blocks.pop(0))
        current_level, total_score = stabilize_board(current_level, total_score, the_board)
        block, nb_steps = get_move_with_highest_score(the_board, current_level, total_score)
        Board.move_block_horizontally(the_board, block, nb_steps)
        list.append(moves, (block, nb_steps))
        current_level, total_score = stabilize_board(current_level, total_score, the_board)
    return (total_score, moves)


def get_top_moves(board, blocks, min_score=100, max_nb_moves=10, level=1, score=0):
    """
       Compute the best possible moves to play the game on the given board starting from
       the given level and the given score using the given blocks to fill the bottom row
       in each step of the game to reach a score at least as high as the given minimal
       score in no more than the given maximum number of moves.
       Play starts with moving all blocks up one row, adding new blocks to the bottom
       row and stabilizing the board.
       - The given blocks are collected in a list of which each element is a list of
         blocks to fill the bottom row once.
       - The function returns None if the given minimal score cannot be reached.
         Otherwise, the function returns a list of all the moves to reach at least
         the minimal score. Each move in the latter list is a tuple containing
         the lefmost position of the block to move, followed by the block itself,
         followed by the distance over which that block has to be moved.
         The position of the block is taken at the time of the move, which may obviously
         differ from the initial position taken by that block on the board.
       - If several solutions exist to reach at least the minimal score, the function
         returns the shortest of them in terms of number of moves. If several
         shortest solutions exist, the function returns the solution that is less
         than all other solutions of the same length using Python's operator to compare
         lists.
       - Upon exit, the given board and the given list of blocks must be in the same
         state they were in upon entry.
       ASSUMPTIONS
       - The given board is a proper and stable board.
       - Each element in the list of blocks ((blocks[I]) is a sequence that can be
         used to fill the bottom row once in a valid way (i.e., no overlapping
         positions, no remaining gap larger than half the number of columns after
         a complete fill, ...)
       - The elements in the list of blocks (blocks[I]) are used in the order from left
         to right.
       - Each basic element in the list of blocks ((blocks[I][J]) is a tuple
         involving a (leftmost) position in the bottom row of the board followed by
         a proper block for a board with the given dimension.
       - The given minimal score is a non-negative integer number.
       - The given maximum number of moves is an integer number. If it is negative,
         the function must return None.
       - The given level is a positive integer number.
       - The given score is a non-negative integer number.
    """
    if (score >= min_score) and (max_nb_moves >= 0):
        return []
    if (len(blocks) == 0) or (max_nb_moves <= 0) or (not Board.is_empty_row(board, "X")):
        return None
    assert isinstance(level, int) and (level >= 0)
    assert isinstance(score, int) and (score >= 0)
    board_after_push_up = Board.copy_board(board)
    Board.push_all_blocks_up(board_after_push_up)
    blocks_to_fill_bottom_row = list.pop(blocks, 0)
    for (leftmost_position, block) in blocks_to_fill_bottom_row:
        Board.add_block_at(board_after_push_up, block, leftmost_position)
    level, score = \
        stabilize_board(level, score, board_after_push_up)
    top_solution_so_far = None
    for block in Board.get_all_blocks(board_after_push_up):
        for nb_steps in get_all_possible_steps(board_after_push_up, block):
            copy_board = Board.copy_board(board_after_push_up)
            Board.move_block_horizontally(copy_board, block, nb_steps)
            level_after_move, score_after_move = stabilize_board(level, score, copy_board)
            best_solution_from_current_move = \
                get_top_moves(copy_board, blocks, min_score, max_nb_moves - 1, level_after_move, score_after_move)
            if (best_solution_from_current_move is not None):
                best_solution_from_current_move.insert\
                    (0, (Board.get_leftmost_position_of(board_after_push_up,block), block, nb_steps))
                top_solution_so_far = best_solution_from_current_move
                max_nb_moves = len(top_solution_so_far) - 1
    list.insert(blocks, 0, blocks_to_fill_bottom_row)
    return top_solution_so_far


def let_player_move_block(board):
    """
        Let the player move one of the blocks on the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        - The bottom row of the given board is not empty.
    """
    block_to_move = None
    distance_to_move_over = None
    while (block_to_move is None) or (distance_to_move_over is None):
        players_position = \
            input("Some position of block to move: ").split(',')
        if (len(players_position) > 1) and str.isdigit(players_position[1]):
            players_position[1] = eval(players_position[1])
        players_position = tuple(players_position)
        if not Position.is_proper_position(players_position):
            print("   ---> A proper position consists of a letter, a comma and some digits!")
        elif not Position.is_within_boundaries(Board.get_dimension(board), players_position):
            print("   ---> The position is outside the boundaries of the board!")
        elif Board.is_free_at(board, players_position):
            print("   ---> No block at the given position")
        else:
            the_block = Board.get_block_at(board, players_position)
            players_distance = int(input("Enter distance to move block over : "))
            if (not isinstance(players_distance, int)) or (players_distance == 0):
                print("   ---> The distance must be a non-zero integer number.!")
            elif not Board.can_move_over(board, the_block, players_distance):
                print("   ---> The given block cannot move over the given distance")
            else:
                block_to_move = the_block
                distance_to_move_over = players_distance
    Board.move_block_horizontally(board, block_to_move, distance_to_move_over)


def play_keyboard(blocks = [], nb_rows=10, nb_columns=8):
    """
        Function to play the game on a board with the given number of rows and the
        given number of columns via the keyboard, using the given blocks to fill
        the bottom row.
       - The given blocks are collected in a list of which each element is a list of
         blocks to fill the bottom row once. The function will first use elements from
         that list until the list is exhausted. From that point on, the function will
         generate blocks to fill the bottom row in a random way.
        ASSUMPTIONS
        - The given number of rows and the given number of columns are integer numbers
          greater than 1.
    """
    score = 0
    level = 1
    the_board = Board.make_board((nb_rows, nb_columns))
    while Board.is_empty_row(the_board, "X"):
        if len(blocks) > 0:
            Board.insert_bottom_row(the_board,blocks.pop(0))
        else:
            Board.push_all_blocks_up(the_board)
            max_block_length = max(2, \
                               round(nb_columns / 4) if level <= 3 else \
                                   round(nb_columns / 3) if level <= 6 else
                                   round(nb_columns / 2))
            Board.fill_bottom_row(the_board, max_block_length)
        level, score = stabilize_board(level, score, the_board)
        Board.print_board(the_board)
        let_player_move_block(the_board)
        level, score = stabilize_board(level, score, the_board)
        print("Score: ", score, "[level: ", level, "]")
    print("Einde spel!")


if __name__ == '__main__':
    block1_1 = Block.make_block(2, color=Color.RED)
    block1_2 = Block.make_block(1, color=Color.RED)
    block1_3 = Block.make_block(3, color=Color.RED)
    block2_1 = Block.make_block(3, color=Color.BLUE)
    block2_2 = Block.make_block(2, color=Color.BLUE)
    block3_1 = Block.make_block(2, color=Color.GREEN)
    block3_2 = Block.make_block(1, color=Color.GREEN)
    block3_3 = Block.make_block(1, color=Color.GREEN)
    block4_1 = Block.make_block(3, color=Color.CYAN)
    block4_2 = Block.make_block(1, color=Color.CYAN)
    block4_3 = Block.make_block(2, Block.FRAGILE, color=Color.CYAN)
    block5_1 = Block.make_block(1, color=Color.MAGENTA)
    block5_2 = Block.make_block(1, color=Color.MAGENTA)
    block5_3 = Block.make_block(1, color=Color.MAGENTA)
    block5_4 = Block.make_block(2, color=Color.MAGENTA)
    block6_1 = Block.make_block(2, Block.ELECTRIFIED, color=Color.BLACK)
    block6_2 = Block.make_block(3, color=Color.BLACK)
    block7_1 = Block.make_block(2, Block.FRAGILE, color=Color.YELLOW)
    block7_2 = Block.make_block(1, color=Color.YELLOW)
    block7_3 = Block.make_block(2, Block.ELECTRIFIED, color=Color.YELLOW)
    blocks_to_fill = [[(("a", 1), block1_1), (("a", 4), block1_2), (("a", 5), block1_3)],
                      [(("a", 2), block2_1), (("a", 6), block2_2)],
                      [(("a", 1), block3_1), (("a", 4), block3_2), (("a", 7), block3_3)],
                      [(("a", 1), block4_1), (("a", 5), block4_2), (("a", 6), block4_3)],
                      [(("a", 1), block5_1), (("a", 2), block5_2), (("a", 3), block5_3), (("a", 4), block5_4)],
                      [(("a", 2), block6_1), (("a", 4), block6_2)],
                      [(("a", 1), block7_1), (("a", 3), block7_2), (("a", 4), block7_3)],
                      ]
    play_keyboard(blocks_to_fill,nb_rows=8,nb_columns=7)
