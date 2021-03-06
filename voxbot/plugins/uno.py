from voxbot.bot import Plugin

import shelve
import os

class Uno(Plugin):
    '''usage: ^uno blabla'''
    
    def __init__(self, bot):
        super(Uno, self).__init__(bot)
        if not os.path.exists('./data/'):
            os.mkdir('./data/')
        self.data = shelve.open('./data/uno.dat')
        self._start_game()
        self._stop_game()
        self._player_join()
    
    def __del__(self):
        self.data.close()
    
    @Plugin.command('^uno')
    def _start_game(self, cmd, args, MIN=2, MAX=10):
        if not self.data.get('game_started', '') or not self.data['game_started']:
            try:
                if not args:
                    raise ValueError
                else:
                    players = int(args)
                if players < MIN or players > MAX:
                        raise ValueError
            except ValueError:
                self.reply("Please specify the number of players (2-10)")
                return
            self.reply("Uno game starting")
            self.data['game_started'] = True
            self.data['num_players'] = players
            self.data['players'] = [self.user]
        else:
            self.reply("Game already in progress")

    @Plugin.command('^stopuno')
    def _stop_game(self, cmd, args):
        if self.data.get('game_started', ''):
            self.data['game_started'] = False
            self.reply("Uno game stopped")
        else:
            self.reply("No uno game in progress")

    @Plugin.command('^join')
    def _player_join(self, cmd, args):
        if self.data.get('game_started', ''):
            PLUS_ONE = len(self.data['players']) + 1 
            
            if self.user in self.data['players']:
                self.reply("{0}: You are already in the game!".format(self.user))
            elif self.data.get('in_progress', ''):
                self.reply("Sorry {0}, the game has already begun.".format(self.user))
            elif self.data.get('num_players', '') >= PLUS_ONE:
                self.data['players'] = self.data['players'] + [self.user]
                self.reply("{0} joined the game. ({1}/{2} players)".format(self.user, len(self.data['players']), self.data['num_players']))
            else:
                self.reply('There are already enough players for this game!')
        else:
            self.reply("{0}: There is no game going on".format(self.user))


