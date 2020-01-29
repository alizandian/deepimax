"""
game.py. This Module simulates the full gameplay of Fox and sheeps from start to the end.
This Gameplay enables us of having bot vs. bot, bot vs. player and player vs. player.

Written by Ali Zandian (alizandian@outlook.com) for University project, researching a better way to gauge unlimited trees.
A project at the university of Ashrafi Esfahani.
"""

import entities as Entities
import bot as Bot
import graphics as Graphics

class Gameplay():
    """
    A Gameplay object is a simulation of a game of fox and sheep.
    """

    def __init__(self, board, display, foxController, sheepsController, maxMoveCount , turn , time, actionUpdate, startCallFunc, endCallFunc):
        """
        Instantiate a gameplay object by given attributes.

        board -> The current board (probably the start initialized state of board) to start playing.
        isFoxBot -> Determines if the fox is controlled by a bot or by the player.
        isSheepBot -> Determines if the sheeps are controlled by a bot or by the player.
        maxMoveCount -> Max for all moves in the game. 
        isFoxTurn -> Which side of the board should start the game.
        """

        self.board = board
        self.foxController = foxController
        self.sheepsController = sheepsController
        self.isGameTerminated = False
        self.moveCounts = 0
        self.maxMoveCount = maxMoveCount
        self.turn = turn
        self.time = time
        self.display = display
        self.actionUpdate = actionUpdate
        self.startCallFunction = startCallFunc
        self.endCallFunction = endCallFunc

        self.display.SetControllersInfo(foxController = foxController, sheepsController = sheepsController)

        # If turn hasn't assigned, we randomized the first turn to be which side of the board
        if(self.turn == None):
            self.turn = Entities.Turn.Fox
        if(self.time == None):
            self.time = 30

    def Go(self):
        """
        Indicates the start of the gameplay. If this function is executed,
        the program falls in to this loop of gameplay, which sides of board taking actions one by one.
        """

        self.startCallFunction()
        self.display.Running()

        # If the game is not yet terminated we continue playing
        while(self.isGameTerminated == False):
            self.display.TurnStarted(turn = self.turn, time = self.time)
            result = None
            action = None
            top = None

            if(self.turn == Entities.Turn.Fox):    
                result = self.foxController.Action(self.board, self.turn)
                self.turn = Entities.Turn.Sheeps
            elif(self.turn == Entities.Turn.Sheeps):                        
                result = self.sheepsController.Action(self.board, self.turn)
                self.turn = Entities.Turn.Fox

            if(result != None):
                action, top = result
                self.__MoveUnit(action[0], action[1])
                if(self.turn == Entities.Turn.Fox):
                    self.actionUpdate(top, self.sheepsController)
                else:
                    self.actionUpdate(top, self.foxController)

            # handling termination 
            self.moveCounts += 1
            self.__TerminationConditionCheck()

        print ('Game ends! after ', str(self.moveCounts) ,' moves!')
        self.display.Ended()
        self.endCallFunction()
        
    def __MoveUnit(self, start, end):
        """ Private method for moving an unit. This method consists of moving logical and graphical """
        self.board.Action(start, end)
        self.display.MoveUnit(start, end)

    def __TerminationConditionCheck(self):
        """ Termination condition check for the gameplay """
        if(self.moveCounts >= self.maxMoveCount and self.maxMoveCount != 0):
            self.isGameTerminated = True

    def End(self):
        """ Wrapping up the gameplay """
        self.isGameTerminated = True
        Bot.algorithmBreak = True
        self.display.Stopped()