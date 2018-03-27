import time
import random

ROW_WIDTH = 75
ski_appearance = ['//', '||', '\\\\', 'XX']
LEFT = 0
STRAIGHT = 1
RIGHT = 2
CRASH = 3


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




def clear_screen():
    for i in range(0,30):
        print('')


def build_row(center, lane_width):
    left_trees_width = int(center - lane_width/2)
    right_trees_width = int(ROW_WIDTH - left_trees_width - lane_width)
    output = '*'*left_trees_width + ' '*(lane_width-2) + '*'*right_trees_width
    return output


def insert_skis(ski_position, row, ski_direction):
    results = True
    if (row[ski_position-1] == '*') or (row[ski_position] == '*'):
        ski_direction = CRASH
        results = False
    output = row[0:ski_position-1] + ski_appearance[ski_direction] + row[ski_position+1:len(row)]
    return (results, output)

def handle_movement(ski_position, ski_direction):
    if ski_direction == LEFT:
        ski_position = ski_position - 1
    elif ski_direction == RIGHT:
        ski_position = ski_position + 1
    return ski_position

def get_hill_info():
    turn_length = random.randint(4,8)
    direction = random.randint(-1,1)
    return (turn_length, direction)

getch = _Getch()
def get_movement():
    retval = STRAIGHT
    x = getch()
    if len(x) > 0:
        if (x[0] == 224) and (x[1] == 75):
            retval = LEFT
        elif (x[0] == 224) and (x[1] == 77):
            retval = RIGHT
    return retval

def next_round(round_number, lane_width, slowness):
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
    return round_number, lane_width, slowness



clear_screen()

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

while i>0:
    i = i-1
    row = build_row(center, lane_width)
    xxxx = row[ski_position]
    ski_direction = get_movement()
    ski_position = handle_movement(ski_position, ski_direction)
    results, row = insert_skis(ski_position, row, ski_direction)
    # Now, insert the skis

    time.sleep(.2)
    if turn_length == 0:
        turn_length, hill_direction = get_hill_info()
    else:
        turn_length = turn_length - 1

    # If the lane is getting too close to the side of the screen.
    if center == lane_width:
        hill_direction = 1
    elif center == ROW_WIDTH - lane_width:
        hill_direction = -1

    center = center + hill_direction
    print(row)
    if results == False:
        print('')
        print('CRASH!!!!!!')
        time.sleep(2)
        break

    if i==0:
        round_number, lane_width, slowness = next_round(round_number, lane_width, slowness)
        i = round_length
