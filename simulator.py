import argparse
from player import create_player
from wheel import create_wheel
from table import Table
from game import RouletteGame

class Simulator:
    """ Initialized with a game and a player.
    Peform various sessions (the player playing a game),
    and record some stats

    """
    def __init__(self, game, player_class, init_duration=250,
                 init_stake=100, samples=50):
        self.init_duration =  init_duration
        self.init_stake = init_stake
        self.samples = samples
        self.durations = list()
        self.maxima = list()
        self.player_class = player_class
        self.game = game

    def session(self):
        """ Excecute a single game session, and return
        the list of stakes

        """
        stakes = list()
        player = create_player(self.player_class, self.game.table,
                               self.init_stake, self.init_duration)
        while player.playing():
            stakes.append(player.stake)
            self.game.cycle(player)
        return stakes

    def gather(self):
        """ Execute self.samples games sessions,
        collecting the stakes that was made to
        update self.durations and self.maxima

        """
        for i in range(self.samples):
            stakes = self.session()
            self.durations.append(len(stakes))
            self.maxima.append(max(stakes))


def run_simulation(init_duration, init_stake, samples, player):
    """ Run simulation, print the result to stdout

    """
    wheel = create_wheel()
    table = Table(wheel)
    game = RouletteGame(wheel, table)
    simulator = Simulator(game, player,
                          init_duration=init_duration, samples=samples,
                          init_stake=init_stake)
    simulator.gather()
    print(simulator.durations)
    print(simulator.maxima)


def main():
    """ Parse command line arguments

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--init-duration", type=int)
    parser.add_argument("--init-stake", type=int)
    parser.add_argument("--samples", type=int)
    parser.add_argument("--player")
    parser.set_defaults(init_duration=250,
                        init_stake=10,
                        samples=50,
                        player="Martingale")
    args = parser.parse_args()
    run_simulation(args.init_duration, args.init_stake,
                   args.samples, args.player)


if __name__ == "__main__":
    main()
