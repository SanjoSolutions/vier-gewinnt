import random
import time

from main import VierGewinnt, print_state, NUMBER_OF_COLUMNS, get_available_actions, previous_player, next_player, step, \
    determine_winner, determine_reward, Player, is_grid_full


def main():
    game = VierGewinnt()

    def new_game():
        print('New game:')
        print('')
        state = game.reset()
        print_state(state)
        return state

    state = new_game()

    while True:
        action = choose_action(game, state)
        state, reward, done = game.step(action)
        print_state(state)

        if done:
            winner = game.determine_winner()
            print('Player ' + str(winner.value) + ' won.')
            print('')
            return


def choose_action(game, state):
    action = mcts(game, state, duration=10)
    return action


NUMBER_OF_PLAYERS = len(Player)


def mcts(game, state, duration):
    start_time = time.time()
    current_node = Node(previous_player(game.current_player), None, state)
    while time.time() - start_time < duration:
        node = current_node
        while not is_terminal_node(node):
            available_actions = get_available_actions(node.state)
            if len(available_actions) >= 1:
                parent = node
                player = next_player(parent.player)
                action = random.choice(available_actions)
                state = step(parent.state, action, player)
                try:
                    node = next(node for node in parent.children if node.action == action)
                except StopIteration:
                    node = Node(player, action, state, parent)
                    parent.children.add(node)
            else:
                raise Exception('0 available states')
        winner = determine_winner(node.state)
        if winner:
            reward = [
                determine_reward(node.state, player)
                for player
                in Player
            ]
            while node:
                for index in range(NUMBER_OF_PLAYERS):
                    node.reward[index] += reward[index]
                node.playouts += 1
                node = node.parent

    player = next_player(current_node.player)
    if current_node.playouts >= 1:
        node = max(current_node.children, key=lambda node: node.reward[player - 1] / float(node.playouts))
    else:
        node = random.choice(get_available_actions(current_node.state))
    action = node.action

    return action


def is_terminal_node(node):
    winner = determine_winner(node.state)
    if winner is not None:
        return True
    else:
        return is_grid_full(node.state)


class Node:
    def __init__(self, player, action, state, parent=None):
        self.player = player
        self.action = action
        self.state = state
        self.reward = [0, 0]
        self.playouts = 0
        self.parent = parent
        self.children = set()


if __name__ == '__main__':
    main()
