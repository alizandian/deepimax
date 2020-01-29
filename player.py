"""
This class is a handler for player inputs. They precept the board and they take actions.
This class would be a 'friend' to graphics options as lots of graphical manipulations are involved.

Written by Ali Zandian (alizandian@outlook.com) for University project, researching a better way to gauge unlimited trees.
A project at the university of Ashrafi Esfahani.
"""

import entities as Entities
import graphics as Graphics

class Player(Entities.Controller):
    def __init__(self, name, display):
        super().__init__()
        self.title = name

    def Action(self, board, turn):
        return super().Action(board, turn)