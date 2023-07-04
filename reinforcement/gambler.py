import sys
import random

def value_iteration(p=0.5, theta=0.000000001):
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

def optimal_policy(value, p=0.5, theta=0.000000001):
    """
    """
    policy = {}
    for state in range(1, 100):
        max_action = [(0, 1)]
        for action in range(1, min(state, 100 - state) + 1):
            r = p * value[state + action] + (1 - p) * value[state - action]
            if (r - max_action[0][0]) > theta:
                max_action = [(r, action)]
            elif abs(r - max_action[0][0]) <= theta:
                max_action.append((r, action))
        policy[state] = max_action
    return policy

def flip(p):
    """
    """
    if random.random() <= p:
        return True
    return False

def player_optimal(policy, state=1, p=0.5):
    """
    """
    while (0 < state and state < 100):
        choice = random.randint(0, len(policy[state]) - 1)
        amount = policy[state][choice][1]
        coin = flip(p)
        #print(">> state", state, "amount", amount, "coin", coin, "all", policy[state])
        if coin:
            state = state + amount
        else:
            state = state - amount
    return state

def player_random(state=1, p=0.5):
    """
    """
    while (0 < state and state < 100):
        amount = random.randint(1, min(state, 100 - state))
        coin = flip(p)
        #print(">> state", state, "amount", amount, "coin", coin)
        if coin:
            state = state + amount
        else:
            state = state - amount
    return state

if __name__ == "__main__":
    """
    state = int(sys.argv[1])
    p = float(sys.argv[2])
    print(player_rand(state, p))
    """

    """
    p = float(sys.argv[1])

    value = value_iteration(p)
    policy = optimal_policy(value, p)
    for state in policy:
        for action in policy[state]:
            print(state, action[1])
    """
    state = int(sys.argv[1])
    p = float(sys.argv[2])
    value = value_iteration(p)
    policy = optimal_policy(value, p)
    #print(player_optimal(policy, state, p))
    print(player_random(state, p))
