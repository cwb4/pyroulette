from player import create_player

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
