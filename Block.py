import Color
import Dimension
import Position

ORDINARY    = 1
ELECTRIFIED = 2
FRAGILE     = 3


def make_block(length, type=ORDINARY, color = Color.BLACK):
    """
      Return a block of the given length, of the given type and with the given
      color.
      ASSUMPTIONS
      - The given length is a positive integer number.
      - The given type is either ORDINARY, ELECTRIFIED or FRAGILE.
      - The given color is a proper color.
    """
    return (length,type,color)


def is_proper_block(block):
    """
      Check whether the given block is a proper block.
      - True if and only if the given block has a positive length, has a proper type
        and a proper color.
      ASSUMPTIONS
      - None
    """
    if not isinstance(block,tuple):
        return False
    if len(block) != 3:
        return False
    length, type, color = block
    if not isinstance(length,int):
        return False
    if length <= 0:
        return False
    if type not in {ORDINARY,ELECTRIFIED,FRAGILE}:
        return False
    if not Color.is_proper_color(color):
        return False
    return True


def make_random_block(max_length):
    """
        Return a random block whose length does not exceed the given maximum length.
        - On average, 80% of the blocks will be ordinary blocks; 15% will be
          electrified blocks and 5% will be fragile blocks.
        ASSUMPTIONS
        - The given maximum length is a positive integer number.
        NOTE
        - This function may be given to the students.
    """
    import random
    length = random.randint(1,max_length)
    random_type = random.randint(1,20 if length>1 else 16)
    type = ORDINARY if random_type <= 16 \
        else ELECTRIFIED if random_type < 20 else FRAGILE
    color = Color.get_random_color()
    return make_block(length,type,color)


def split_block(block):
    """
      Split the given block in two smaller blocks.
      - The function returns a tuple of two new blocks.
      - The length of the first block in the resulting tuple is equal to the quotient
        of the length of the given block incremented by 1 and divided by 2.
      - The length of the second block in the resulting tuple is equal to the quotient
        of the length of the given block divided by 2.
      - Blocks in the resulting tuple with an even length are fragile; blocks with an
        odd length are ordinary blocks.
      - Both blocks have the same color as the given block.
      ASSUMPTIONS
      - The given block is a proper block.
    """
    length1 = (get_length(block)+1)//2
    type1 = ORDINARY if length1%2==1 else FRAGILE
    block1 = make_block(length1,type1,get_color(block))
    length2 = get_length(block)//2
    type2 = ORDINARY if length2%2==1 else FRAGILE
    block2 = make_block(length2,type2,get_color(block))
    return (block1,block2)


def is_proper_block_for_dimension(block,dimension):
    """
      Check whether the given block is a proper block for a board with
      the given dimension.
      - True if and only if the length of the given block does not exceed
        half the number of columns of the given dimension.
      ASSUMPTIONS
      - The given block is a proper block
      - The given dimension is a proper dimension
    """
    return get_length(block) <= Dimension.get_nb_of_columns(dimension)//2


def get_length(block):
    """
      Return the length of the given block.
      ASSUMPTIONS
      - The given block is a proper block
    """
    return block[0]


def get_type(block):
    """
      Return the type of the given block.
      ASSUMPTIONS
      - The given block is a proper block
    """
    return block[1]


def get_color(block):
    """
      Return the color of the given block.
      ASSUMPTIONS
      - The given block is a proper block
    """
    return block[2]


def get_symbol(block):
    """
      Return the symbol to display a single cell of the given block.
      ASSUMPTIONS
      - The given block is a proper block
      NOTE
      - The body of this function must be included in the skelet.
    """
    if get_type(block) == ORDINARY:
        return "\u25A2"
    elif get_type(block) == ELECTRIFIED:
        return "\u25A3"
    else:
        return "\u25A4"


# def print_block(block):
#     """
#         Print the given block on the standard output stream.
#         ASSUMPTIONS
#         - The given block is a proper block.
#         INTERNAL NOTE
#         - The body of this function must be included in the skeleton.
#     """
#     print("+" + "-"*(get_length(block)*3-2) + "+")
#     print("+" + "-"*(get_length(block)*3-2) + "+")

