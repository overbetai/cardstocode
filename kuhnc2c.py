import random

class InfoSet:
    @staticmethod
    def create(card, actions):
        return f"{card}:{','.join(actions)}"

class RoundState:
    def __init__(self):
        self.pot = 2  # Both players ante 1 chip
        self.current_player = 0
        self.bets = [1, 1]  # Initial ante
        self.actions = []
        self.cards = None

    def legal_actions(self):
        if len(self.actions) < 2:
            return ['pass', 'bet']
        elif len(self.actions) == 2 and self.actions == ['pass', 'bet']:
            return ['pass', 'bet']  # Player 0 can still fold (pass) or call (bet)
        else:
            return []  # No more actions allowed after this

    def get_info_set(self):
        return InfoSet.create(self.cards[self.current_player], self.actions)

class ProbabilityPlayer:
    def __init__(self):
        self.bet_probabilities = {
            # Player 0 initial actions
            InfoSet.create(0, []): 0.3,
            InfoSet.create(1, []): 0.6,
            InfoSet.create(2, []): 0.9,
            # Player 0 after pass-bet
            InfoSet.create(0, ['pass', 'bet']): 0.1,
            InfoSet.create(1, ['pass', 'bet']): 0.4,
            InfoSet.create(2, ['pass', 'bet']): 0.7,
            # Player 1 facing bet
            InfoSet.create(0, ['bet']): 0.2,
            InfoSet.create(1, ['bet']): 0.5,
            InfoSet.create(2, ['bet']): 0.8,
            # Player 1 facing pass
            InfoSet.create(0, ['pass']): 0.4,
            InfoSet.create(1, ['pass']): 0.7,
            InfoSet.create(2, ['pass']): 1.0,
        }

    def get_action(self, round_state):
        info_set = round_state.get_info_set()
        if info_set in self.bet_probabilities:
            if random.random() < self.bet_probabilities[info_set]:
                return 'bet'
            else:
                return 'pass'
        else:
            # If we encounter an unknown information set, bet with 50% probability
            return 'bet' if random.random() < 0.5 else 'pass'

class RandomPlayer:
    def get_action(self, round_state):
        return random.choice(round_state.legal_actions())

class PassivePlayer:
    def get_action(self, round_state):
        return 'pass'

class AggressivePlayer:
    def get_action(self, round_state):
        return 'bet' if 'bet' in round_state.legal_actions() else 'pass'

class Game:
    def __init__(self, player1, player2):
        self.deck = [0, 1, 2]
        self.players = [player1, player2]
        self.scores = [0, 0]

    def deal_cards(self):
        return random.sample(self.deck, 2)

    def play_round(self):
        round_state = RoundState()
        round_state.cards = self.deal_cards()

        while round_state.legal_actions():
            current_player = round_state.current_player
            action = self.players[current_player].get_action(round_state)
            round_state.actions.append(action)

            if action == 'bet':
                round_state.bets[current_player] += 1
                round_state.pot += 1

            round_state.current_player = 1 - current_player

        # Determine the winner
        if round_state.actions == ['pass', 'pass']:
            winner = 0 if round_state.cards[0] > round_state.cards[1] else 1
        elif round_state.actions == ['pass', 'bet', 'pass']:
            winner = 1
        elif round_state.actions == ['pass', 'bet', 'bet'] or round_state.actions == ['bet', 'bet']:
            winner = 0 if round_state.cards[0] > round_state.cards[1] else 1
        elif round_state.actions == ['bet', 'pass']:
            winner = 0

        # Update scores
        self.scores[winner] += round_state.pot - round_state.bets[winner]
        self.scores[1 - winner] -= round_state.bets[1 - winner]

def main():
    num_games = 10000
    player1 = RandomPlayer()
    player2 = ProbabilityPlayer()
    game = Game(player1, player2)

    for _ in range(num_games):
        game.play_round()

    print(f"After {num_games} games:")
    print(f"Player 1 (Random) score: {game.scores[0]}")
    print(f"Player 2 (Probability) score: {game.scores[1]}")

if __name__ == "__main__":
    main()