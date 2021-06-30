import random

from main import VierGewinnt, print_state, NUMBER_OF_COLUMNS, get_available_actions, previous_player, next_player, step, \
    determine_winner, determine_reward, Player


def main():
    game = VierGewinnt()

    def new_game():
        print('New game:')
        print('')
        return game.reset()

    state = new_game()

    while True:
        action = choose_action(game, state)
        state, reward, done = game.step(action)
        print_state(state)

        if done:
            winner = game.determine_winner()
            print('Player ' + str(winner.value) + ' won.')
            print('')

        if done:
            return


def choose_action(game, state):
    action = mcts(game, state, 10000)
    return action


def choose_random_action(game, state):
    available_actions = game.get_available_actions()
    if len(available_actions) >= 1:
        action = random.choice(available_actions)
    else:
        raise Exception('All columns seem to be full.')
    return action


NUMBER_OF_PLAYERS = len(Player)


def mcts(game, state, number_of_iterations):
    current_node = Node(previous_player(game._current_player), None, state)
    for iteration in range(number_of_iterations):
        node = current_node
        available_actions = get_available_actions(node.state)
        if len(available_actions) >= 1:
            parent = node
            player = next_player(parent.player)
            action = random.choice(available_actions)
            state = step(parent.state, action, player)
            try:
                node = next(node for node in parent.children if node.action == action)
            except:
                node = Node(player, action, state, parent)
                parent.children.add(node)
            winner = determine_winner(node.state)
            if winner:
                reward = [
                    determine_reward(node.state, player)
                    for player
                    in Player
                ]
                node.reward = reward
                node = node.parent
                while node:
                    for index in range(NUMBER_OF_PLAYERS):
                        node.reward[index] += reward[index]
                    node = node.parent
        else:
            raise Exception('0 available states')

    player = next_player(current_node.player)
    node = max(current_node.children, key=lambda node: node.reward[player - 1])
    action = node.action

    return action


class Node:
    def __init__(self, player, action, state, parent=None):
        self.player = player
        self.action = action
        self.state = state
        self.reward = [0, 0]
        self.parent = parent
        self.children = set()


if __name__ == '__main__':
    main()
