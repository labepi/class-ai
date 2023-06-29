import sys
import random

def value_iteration(theta=0.001, p=0.5):
    """
    """
    delta = theta + 1
    value = [0] * 101
    value[100] = 1
    while delta > theta:
        delta = 0.0
        for state in range(1, 100):
            v = value[state]
            max_action = (0, 1)
            for action in range(1, min(state, 100 - state) + 1):
                r = p * value[state + action] + (1 - p) * value[state - action]
                if r > max_action[0]:
                    max_action = (r, action)
            value[state] = max_action[0]
            delta = max(delta, abs(v - value[state]))
    return value

def flip(p):
    """
    """
    if random.random() <= p:
        return True
    return False

def player_rand(state=1, p=0.5):
    """
    """
    while (0 < state and state < 100):
        amount = random.randint(1, min(state, 100 - state))
        coin = flip(p)
        print(">> state", state, "amount", amount, "coin", coin)
        if coin:
            state = state + amount
        else:
            state = state - amount
    return state

if __name__ == "__main__":
    """
    state = int(sys.argv[1])
    p = float(sys.argv[2])
    print(player(state, p))
    """
    value = value_iteration()
    for i in range(0, len(value)):
        print(i, value[i])
