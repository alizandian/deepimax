"""
This is the main python file for running the whole project, of course, it has 
all available options to manipulate the game and results.
It also should be able to connect with all other associated python files.

Written by Ali Zandian (alizandian@outlook.com) for University project, researching a better way to gauge unlimited trees.
A project at the university of Ashrafi Esfahani.
"""

import entities as Entities
import graphics as Graphics
import bot as Bot
import profiler as Profiler
import statistics as Statistics
import game as Game
import player as Player
import threading as Threading
import statistics

# Global instances
Display = Graphics.Display("Fox and Sheeps!", '#ccb684')
Board = Entities.Board()
Gameplay = None
GameplayThread = None

def Initialization():
    """ Each time we are refreshing the page, we're doing this """
    Display.Initialization(Board)

def Start():
    """ Equivalent to the action of the 'Start' button. Roughly making a new game play """
    global GameplayThread
    global DefaultFox
    global oncePressed
    global Gameplay
    global Display

    #region Figuring out the fox controller
    foxController = None
    foxControllerType = Display.GetFoxControllerType()
    if(foxControllerType == Entities.ControllerType.Bot):
        strategy = Display.GetFoxStrategy()
        if(strategy != None):
            foxController = Bot.Agent(strategy)
            depth = Display.GetFoxDepth()
            if(depth != None):
                foxController.depth = depth
            if(strategy == Entities.Strategy.Deepimax):
                roa = Display.GetFoxROA()
                if(roa != None):
                    foxController.roa = roa
                doa = Display.GetFoxDOA()
                if(doa != None):
                    foxController.doa = doa
    elif(foxControllerType == Entities.ControllerType.Player):
        name = Display.GetFoxName()
        if(name != None):
            foxController = Player.Player(name, Display)
    
    # Default controller for Fox
    if(foxController == None):
        foxController = Bot.Agent(Entities.Strategy.Minimax)
        foxController.depth = 1
    #endregion

    #region Figuring out the sheeps controller
    sheepsController = None
    sheepsControllerType = Display.GetSheepControllerType()
    if(sheepsControllerType == Entities.ControllerType.Bot):
        strategy = Display.GetSheepsStrategy()
        if(strategy != None):
            sheepsController = Bot.Agent(strategy)
            depth = Display.GetSheepsDepth()
            if(depth != None):
                sheepsController.depth = depth
            if(strategy == Entities.Strategy.Deepimax):
                roa = Display.GetSheepsROA()
                if(roa != None):
                    sheepsController.roa = roa
                doa = Display.GetSheepsDOA()
                if(doa != None):
                    sheepsController.doa = doa
    elif(sheepsControllerType == Entities.ControllerType.Player):
        name = Display.GetSheepsName()
        if(name != None):
            foxController = Player.Player(name, Display)

    # Default controller for Fox
    if(sheepsController == None):
        sheepsController = Bot.Agent(Entities.Strategy.Minimax)
        sheepsController.depth = 1
    #endregion

    # Other options of the board
    maxMoves = Display.GetMaxMoves()
    if(maxMoves == None):
        maxMoves = 0

    time = Display.GetTime()
    if(time == None):
        time = 0

    turn = Display.GetTurn()
    if(turn == None):
        turn = 0

    Gameplay = Game.Gameplay(board = Board,
                                display = Display,
                                foxController = foxController,
                                sheepsController = sheepsController,
                                maxMoveCount = maxMoves,
                                time = time,
                                turn = turn,
                                actionUpdate = ActionUpdate,
                                startCallFunc = GameplayStarts,
                                endCallFunc = GameplayEnds)

    #===================================================================
    # The Game-play thread Starts here (A new thread deviates from here)
    #===================================================================

    GameplayThread = Threading.Thread(target = Gameplay.Go)
    GameplayThread.start()

# GAME PLAY THREAD
def GameplayStarts():
    """ For startups of everything by the gameplay """
    Profiler.Start()
    pass

# GAME PLAY THREAD
def ActionUpdate(topNode, controller):
    """ Each time any action is being taken, here we call the update """

    controllerTitle = controller.title
    if(Bot.Agent == type(controller)):
        controllerTitle +=  " " + str(controller.depth)
        if(controller.strategy == Entities.Strategy.Deepimax):
            controllerTitle += " (" + str(controller.doa) + "," + str(controller.roa) + ")"

    if(Display.drawTreeCheckVar.get() == 1):
        Statistics.DrawTree(topNode, controllerTitle)

    if(Display.compareVar.get() == 1):
        if(Profiler.previousProfileData != None):
            print ("previous Data is not null, ready to draw")
            previouseData = Profiler.previousProfileData
            Statistics.DrawComparison(previouseData, Profiler.Print(True, controllerTitle), int(Display.compareTypeRadioVar.get()))
        else:
            Profiler.Print(True, controllerTitle)

        Profiler.DumpProfilerInfo()
    pass

# GAME PLAY THREAD
def GameplayEnds():
    """ For warping of everything by the gameplay """
    # Do things when the gameplay thread finishes
    Profiler.End()

    if(Display.compareVar.get() == 0):
        Profiler.Print(False, "")

def Reset():
    """
    Refresh the whole window for other experiments, it also 
    terminate the current thread of the gameplay, in the other hand,
    terminate the current running game.
    """
    global Display
    global Gameplay
    global Board
    global GameplayThread
    if(Gameplay != None):
        if(Gameplay.isGameTerminated == False):
            Gameplay.End()
        Gameplay = None
    
    Board = Entities.Board()
    Initialization()

#========================
# Application Starts here
#========================

Initialization()

# Linking graphics inputs
Display.SetStartHandler(func = Start)
Display.SetResetHandler(func = Reset)

# Main loop
Display.mainFrame.mainloop()