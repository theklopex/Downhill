import time
import random

ROW_WIDTH = 75
ski_appearance = ['//', '||', '\\\\', 'XX']
LEFT = 0
STRAIGHT = 1
RIGHT = 2
CRASH = 3

# The following Getch stuff is based on code I copied from StackOverflow

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()

#TODO Test _GetchUnix on Linux.  I do not know what it will do, but
#     I fear that it will wait on user input.

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        kbhit = msvcrt.kbhit()
        if kbhit:
            char1 = msvcrt.getch()
            kbhit = msvcrt.kbhit()
            if kbhit:
                char2 = msvcrt.getch()
                char1 = char1+char2
            return char1
        else:
            return ''



# The following is all my code.

def clear_screen():
    ''' Clears the screen by printing blank lines
        '''
    for i in range(0,30):
        print('')


def build_row(center, lane_width):
    ''' Builds a row for the screen.  It includes trees on the left and right
        with a path that is <lane_width> wide that is centered at position
        <center> in the row.
        '''
    left_trees_width = int(center - lane_width/2)
    right_trees_width = int(ROW_WIDTH - left_trees_width - lane_width)
    output = '*'*left_trees_width + ' '*(lane_width-2) + '*'*right_trees_width
    return output


def insert_skis(ski_position, row, ski_direction):
    ''' Inserts two skis at <ski_position> in the <row> of text.  The skis
        are pointed downhill in either the LEFT, STRAIGHT down, or RIGHT
        orientations.
        '''
    results = True
    if (row[ski_position-1] == '*') or (row[ski_position] == '*'):
        ski_direction = CRASH
        results = False
    output = row[0:ski_position-1] + ski_appearance[ski_direction] + row[ski_position+1:len(row)]
    return (results, output)

def handle_movement(ski_position, ski_direction):
    ''' Returns an updated <ski_position> by moving the skis in <ski_direction>
        '''
    if ski_direction == LEFT:
        ski_position = ski_position - 1
    elif ski_direction == RIGHT:
        ski_position = ski_position + 1
    return ski_position

def get_hill_info():
    ''' Returns 2-tuple of (turn_length, direction) where <turn_length> is a stretch
        of hill where the direction you can ski should not change.  <direction> is the
        direction that this lane of open snow is going (left==-1, straight down==0, right==1).
        '''
    turn_length = random.randint(4,8)
    direction = random.randint(-1,1)
    return (turn_length, direction)

def get_movement():
    ''' Read a character from the user and change it into a direction
        that is meaningful to this game.
        Return either LEFT, STRAIGHT (down), or RIGHT.
        '''
    retval = STRAIGHT
    x = getch()
    if len(x) > 0:
        if (x[0] == 224) and (x[1] == 75):
            retval = LEFT
        elif (x[0] == 224) and (x[1] == 77):
            retval = RIGHT
    return retval

def next_round(round_number, lane_width, slowness):
    ''' Returns a 3-tuple describing the next round.  The 3-tuple returned
        is based on the three input parameters.  The input parameter,
        <round_number> will be incremented.  Then the properties of the
        previous round found in <lane_width> and <slowness> will be
        modified to make the next round more difficult.
        Actual return data: (round_number, lane_width, slowness)
        '''
    print('')
    print('You beat round %d!'%(round_number))
    round_number = round_number + 1
    print('Get ready for round %d'%(round_number))
    time.sleep(3)
    if round_number % 2:
        #odd rounds change slowness
        slowness = slowness * .90
    else:
        #even rounds change lane width
        lane_width = int(lane_width * .90)
    return (round_number, lane_width, slowness)



# Set up an object that we will use to get keyboard input from the user.
getch = _Getch()

# Clear any text from the console screen.
clear_screen()

# Set up the initial state of the game.
center = int(ROW_WIDTH/2)
lane_width = 30
slowness = .3
ski_position = center

round_length = 50
round_number = 1
i=round_length
hill_direction = -1
ski_direction = LEFT
turn_length = 0

# Start skiing!
while i>0:
    i = i-1
    # Get the lane to ski in.
    row = build_row(center, lane_width)
    # Get input from the user
    ski_direction = get_movement()
    # Move based on the user input
    ski_position = handle_movement(ski_position, ski_direction)
    # Draw the skis onto the row
    results, row = insert_skis(ski_position, row, ski_direction)

    # Print the row of trees, lane, and skis.
    print(row)

    # Test for collision with the trees.
    if results == False:
        print('')
        print('CRASH!!!!!!')
        time.sleep(2)
        break

    time.sleep(.2)
    # The following allows us to have periods of no change in our
    # skiing lane.  It counts down for the next possible change.
    if turn_length == 0:
        # Receives random information about the hill we will ski down.
        turn_length, hill_direction = get_hill_info()
    else:
        turn_length = turn_length - 1

    # If the lane is getting too close to the side of the screen,
    # then change the direction to go away from that side of the screen.
    if center == lane_width:
        hill_direction = 1
    elif center == ROW_WIDTH - lane_width:
        hill_direction = -1

    # Change where the center of the lane is located in the row.
    center = center + hill_direction

    # At the end of a round, set up for the next round.
    if i==0:
        round_number, lane_width, slowness = next_round(round_number, lane_width, slowness)
        i = round_length






