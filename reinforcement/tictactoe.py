import sys
import copy
import random

USAGE = """\
Assessment of TicTacToe game.

{} <player> <state>
  <state>  - Initial state (e.g. x___o___x, means x _ _).
  <player> - Player ('o' or 'x').                 _ o _
                                                  _ _ x\
"""

EMPTY = "_"
CROSS = "x"
ROUND = "o"
DRAW = "?"

COUNTER = {CROSS: 0, ROUND: 0, DRAW: 0}

COLOR = {EMPTY: "#cccccc",
         CROSS: "#ccffcc",
         ROUND: "#ffcccc",
         DRAW: "#ccccff"}

COUNT = 0

STATES = {}

T = {}

class State:
    """
    """
    def __init__(self, sid, state, status):
        """
        """
        self.id = sid
        self.state = "".join(state)
        self.status = status
        self.children = []

    def add_child(self, state, position, player):
        """
        """
        self.children.append([state, position, player])

def empty_positions(state):
    """
    """
    ans = []
    size = state.count(EMPTY)
    p = 0
    while len(ans) < size:
        p = state.index(EMPTY, p)
        ans.append(p)
        p = p + 1
    return ans

def verify_status(state):
    """
    """
    if (state[0] != EMPTY):
        if (state[0] == state[1] and state[1] == state[2]):
            return state[0]
        if (state[0] == state[3] and state[3] == state[6]):
            return state[0]

    if (state[4] != EMPTY):
        if (state[0] == state[4] and state[4] == state[8]):
            return state[0]
        if (state[3] == state[4] and state[4] == state[5]):
            return state[3]
        if (state[1] == state[4] and state[4] == state[7]):
            return state[1]
        if (state[2] == state[4] and state[4] == state[6]):
            return state[2]

    if (state[8] != EMPTY):
        if (state[6] == state[7] and state[7] == state[8]):
            return state[6]
        if (state[2] == state[5] and state[5] == state[8]):
            return state[2]

    if (state[0] != EMPTY and state[1] != EMPTY and state[2] != EMPTY and
        state[3] != EMPTY and state[4] != EMPTY and state[5] != EMPTY and
        state[6] != EMPTY and state[7] != EMPTY and state[8] != EMPTY):
        return DRAW

    return EMPTY

def change_player(player):
    """
    """
    if player == CROSS:
        return ROUND
    return CROSS

def print_dot():
    """
    """
    print("digraph {")
    print("  fontname=\"Monospace\"")
    print("  node [shape=box,fontname=\"Monospace\",style=filled]")
    print("  edge [fontname=\"Monospace\",color=\"#cccccc\"]")

    node_str = "  {} [label=\"{}\\n{}\\n{}\\n({})\",color=\"{}\"]"
    for k in STATES:
        value = T["".join(STATES[k].state)]
        line1 = STATES[k].state[:3]
        line2 = STATES[k].state[3:6]
        line3 = STATES[k].state[6:]
        status = COLOR[STATES[k].status]
        print(node_str.format(k, line1, line2, line3, value, status))

    edge_str = "  {} -> {} [label=\"{}:{}\"]"
    for k in STATES:
        for state, position, player in STATES[k].children:
            print(edge_str.format(k, state, position, player))

    print("}")

def print_state(state):
    """
    """
    print(" ".join(state[:3]))
    print(" ".join(state[3:6]))
    print(" ".join(state[6:]))

def choose_position(state, player):
    """
    """
    s = copy.copy(state)
    value = None
    move = None
    for p in empty_positions(state):
        s[p] = player
        key = "".join(s)
        print(p, T[key])
        if (move == None) or (player == ROUND and T[value] > T[key]):
            value = key
            move = p
        elif (player == CROSS):
            value = key
            move = p
        s[p] = EMPTY
        
    return move

def play(state):
    """
    """
    while verify_status(state) == EMPTY:
        print_state(state)
        position = int(input("play 'x' on position: "))
        state[position] = CROSS
        if verify_status(state) == EMPTY:
            print_state(state)
            position = choose_position(state, ROUND)
            print("'o' choosed position:", position)
            state[position] = ROUND
    update_table(state)
    print_state(state)
    print("result:", verify_status(state))

def update_table(state):
    """
    """
    result = verify_status(state)
    key = "".join(state)
    if result == CROSS:
        T[key] = +2
    elif result == ROUND:
        T[key] = -2
    else:
        T[key] = +1

def search(state, player, root=0, position=None):
    """
    """
    global COUNT
    COUNT = COUNT + 1
    count = COUNT
    status = verify_status(state)
    STATES[count] = State(count, state, status)
    if root > 0:
        STATES[root].add_child(count, position, change_player(player))
    if status == EMPTY:
        old_state = copy.copy(state)
        old_key = "".join(old_state)
        T[old_key] = 0
        for p in empty_positions(state):
            state[p] = player
            player = change_player(player)
            search(state, player, count, p)
            key = "".join(state)
            T[old_key] += T[key]
            state[p] = EMPTY
            player = change_player(player)
    else:
        COUNTER[status] += 1
        update_table(state)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        player = sys.argv[1]
        state = list(sys.argv[2])
        search(state, player)
        #print(len(T))
        #for s in T:
        #    print(s, T[s])
        print_dot()
        #play(state)
    else:
        print(USAGE.format(sys.argv[0]))
