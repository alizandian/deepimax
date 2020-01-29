"""
bot.py. This module contains AI algorithms for taking action by bots.
They all get the current state of the board and return the calculated action
based on whom turn it was.

Algorithms are Minimax (with or without alpha-beta pruning), Expectimax and Deepimax.

Written by Ali Zandian (alizandian@outlook.com) for University project, researching a better way to gauge unlimited trees.
A project at the university of Ashrafi Esfahani.
"""

import entities as Entities
import datetime as Time
import queue
import math

# This var is for having a way out of the bot algorithms, 
# Assigned in GUI by the user.
algorithmBreak = False


class Agent(Entities.Controller):
    """
    An Controller controlled by Artificial Intelligence, Its main job is to 
    take the current state and return an action based on requested strategy.
    """
    def __init__(self, strategy):
        super().__init__()
        self.strategy = strategy
        self.title = strategy.name
        self.depth = None
        self.roa = None
        self.doa = None

    def Action(self, board, turn):
        super().Action(board, turn)
        # Simple raw minimax
        if(self.strategy == Entities.Strategy.Minimax):
            return Minimax(board = self.board, turn = self.turn, depth = self.depth)

        # The minimax with alpha beta pruning
        if(self.strategy == Entities.Strategy.MinimaxPAB):
            isMax = True
            if(turn == Entities.Turn.Sheeps):
                isMax = False
            theNode = MinimaxAlphaBeta(board = board, node = None, depth = 0, maxDebth = self.depth, isMax = isMax, a = -math.inf, b = +math.inf)
            if(len(theNode.actions) != 0):
                return theNode.actions.popleft(), theNode.GetTop()

        # The expectimax
        if(self.strategy == Entities.Strategy.Expectimax):
            isMax = True
            if(turn == Entities.Turn.Sheeps):
                isMax = False
            theNode = Expectimax(board = self.board, node = None, depth = 0, maxDebth = self.depth, isMax = isMax, isExpect = False)
            if(len(theNode.actions) != 0):
                return theNode.actions.popleft(), theNode.GetTop()

        # The deepimax designed by me
        if(self.strategy == Entities.Strategy.Deepimax):
            isMax = True
            if(turn == Entities.Turn.Sheeps):
                isMax = False
            theNode = Deepimax(board = self.board, node = None, depth = 0, maxDepth = self.depth, isMax = isMax, doa = self.doa, roa = self.roa)
            if(len(theNode.actions) != 0):
                return theNode.actions.popleft(), theNode.GetTop()

def Minimax(board, turn, depth):
    """ 
    Returns and action (start, end) which start and end are 2D tuples representing
    positions in the board.

    board -> Gets the current board and calculate on it.
    isFox -> Determining which side of the board (Sheep or fox) now taking a turn.
    window -> Getting the main window in the graphics for updating purposes.
    """
    """
    Minimax: Creates a table of decisions based on all available actions for each side of the 
    game. Tree is full and all parts should be there. We go as deep as we want (here is depth limited)
    and the reason is we cant go all the way through the tree because game trees are mostly considered unlimited.
    Then in any depth we want we stop and calculate Evaluation functions for tree leaves and then trace back
    the tree and run Minimax algorithm which is in each state, we either max or min over children based on whom turn
    it is. 
    """
    global algorithmBreak
    algorithmBreak = False

    isFox = True
    if(turn == Entities.Turn.Sheeps):
        isFox = False

    currentDepth = 0
    top = Entities.MinimaxTreeNode(currentDepth)
    top.actions = queue.Queue().queue

    # Going as deeply as we want, a depth limited. It can be break by minimaxBreak
    while(algorithmBreak == False and currentDepth != depth):

        # Getting all the noes in the current depth
        states = top.GetDepthNodes(currentDepth)
        if(states == None):
            break

        # Looping over all same depth nodes for updating board and make their children
        for s in states:
            # Creating a copy of the current board
            currentBoard = Entities.Board()
            currentBoard.Copy(board)
            priviousActions = s.actions.copy()

            # Loop over all actions  respectably in this state and update the board
            for i in range(s.actions.__len__()):
                action = s.actions.popleft()
                currentBoard.Action(action[0], action[1])

            availableActions = []
            # If this is fox turn
            if(isFox == True):      
                availableActions = currentBoard.AvailableActionsFox()
            # If this is sheeps turn
            elif(isFox == False):                    
                availableActions = currentBoard.AvailableActionsSheep()

            # Loop over all available actions and for each make a child and assign to this state
            for a in availableActions:
                child = Entities.MinimaxTreeNode(currentDepth+1)
                newActions = priviousActions.copy()
                newActions.append(a)
                child.actions = newActions
                child.parent = s
                s.AddChildren(child)

        currentDepth += 1
        isFox = not isFox

    # Filling the tree is done, now we select the appropriate action
    isFox = True
    if(turn == Entities.Turn.Sheeps):
        isFox = False

    TheNode = MiniMaxValue(board, top, isFox)

    # Returning the calculated action
    if(algorithmBreak == False):
        if(len(TheNode.actions) != 0):
            return TheNode.actions.popleft(), top
    else:
        algorithmBreak = False

def MiniMaxValue(board, node, isMax):
    """
    Gets the made tree top node and going through it recursively
    to min or max over children

    board -> Getting the current board
    node -> top node of created miniMax tree 
    isMax -> Is this iteration of recursive for maxing over children or mining
    """
    """
    MinimaxValue: Going from top to bottom of the tree and min and maxing over
    nodes considering isMax variable and returning the min or max node in each parent.
    In the end the nominated node returns with its evaluation function point.
    """

    # If this node has no children
    if(len(node.GetChildren()) == 0):
        # Making a copy of the board 
        currentBoard = Entities.Board()
        currentBoard.Copy(board)
        currentActions = node.actions.copy()

        # Looping over all actions in this node and updating the board
        for i in range(currentActions.__len__()):
            action = currentActions.popleft()
            currentBoard.Action(action[0], action[1])
        
        # Calculating the evaluation Function point
        node.point = currentBoard.EvaluationFunction()

        # returning this node
        return node
    
    # if this node has children
    else:
        # Recurse to children
        subNodes = []
        for child in node.GetChildren():
            subNodes.append(MiniMaxValue(board, child, not isMax))

        # If its the max turn, max over children nodes and return the max
        if(isMax):
            maxNode = max(subNodes, key = lambda x: x.point)
            node.point = maxNode.point
            return maxNode
        # If its the min turn, min over children nodes and return the min
        else:
            minNode = min(subNodes, key = lambda x: x.point)
            node.point = minNode.point
            return minNode

def MinimaxAlphaBeta(board, node, depth, maxDebth, isMax, a, b):
    """ 
    The minimax Method with alpha beta pruning. 
    Returns a node
    """
    
    # Creating the node
    if(depth == 0):
        node = Entities.MinimaxTreeNode(0)
        node.actions = queue.Queue().queue

    # Creating a new instance of the board
    currentBoard = Entities.Board()
    currentBoard.Copy(board)
    previousActions = node.actions.copy()

    # Updating the board
    for i in range(previousActions.__len__()):
        action = previousActions.popleft()
        currentBoard.Action(action[0], action[1])

    # Get list of available actions
    availableActions = []
    if(isMax):      
        availableActions = currentBoard.AvailableActionsFox()
    else:                
        availableActions = currentBoard.AvailableActionsSheep()

    # Check the leave (We are in the last depth or we have no children)
    if(depth == maxDebth or availableActions.__len__() == 0):
        node.point = currentBoard.EvaluationFunction()
        return node

    # Make the children
    for action in availableActions:
        child = Entities.MinimaxTreeNode(depth + 1)
        newActions = node.actions.copy()
        newActions.append(action)
        child.actions = newActions
        child.parent = node
        node.AddChildren(child)

    # Actual minimax with alpha beta pruning code
    if(isMax):
        v = -math.inf
        childNode = None
        for child in node.children:
            temp = MinimaxAlphaBeta(board, child, depth +1, maxDebth, False, a, b)
            if(temp == None):
                continue
            if(temp.point > v):
                childNode = temp
                v = temp.point
            if(v >= b):
                return None
            a = max(a, v)
        node.point = v
        return childNode
    else:
        v = math.inf
        childNode = None
        for child in node.children:
            temp = MinimaxAlphaBeta(board, child, depth +1, maxDebth, True, a, b)
            if(temp == None):
                continue
            if(temp.point < v):
                childNode = temp
                v = temp.point
            if(v <= a):
                return None
            b = min(a, v)
        node.point = v
        return childNode

def Expectimax(board, node, depth, maxDebth, isMax, isExpect):
    """ The expectimax algorithm """
        # Creating the node
    if(depth == 0):
        node = Entities.MinimaxTreeNode(0)
        node.actions = queue.Queue().queue

    # Creating a new instance of the board
    currentBoard = Entities.Board()
    currentBoard.Copy(board)
    previousActions = node.actions.copy()

    # Updating the board
    for i in range(previousActions.__len__()):
        action = previousActions.popleft()
        currentBoard.Action(action[0], action[1])

    # Get list of available actions
    availableActions = []
    if(isMax):      
        availableActions = currentBoard.AvailableActionsFox()
    else:                
        availableActions = currentBoard.AvailableActionsSheep()

    # Check the leave (We are in the last depth or we have no children)
    if(depth == maxDebth or availableActions.__len__() == 0):
        node.point = currentBoard.EvaluationFunction()
        return node

    # Make the children
    for action in availableActions:
        child = Entities.MinimaxTreeNode(depth + 1)
        newActions = node.actions.copy()
        newActions.append(action)
        child.actions = newActions
        child.parent = node
        node.AddChildren(child)

    # Actual minimax with alpha beta pruning code
    if(not isExpect): # Maximum
        v = -math.inf
        childNode = None
        for child in node.children:
            temp = Expectimax(board, child, depth +1, maxDebth, not isMax , True)
            if(temp == None):
                continue
            if(temp.point > v):
                childNode = temp
                v = temp.point
        node.point = v
        return childNode
    else: # Expecting
        v = 0
        childNode = None
        for child in node.children:
            temp = Expectimax(board, child, depth +1, maxDebth, not isMax ,  False)
            if(temp == None):
                continue
            v = v + temp.point
        node.point = v / node.children.__len__()
        return node

def Deepimax(board, node, depth, maxDepth, isMax, doa, roa):
    """
    This is the algorithm i made to go as deep as we can while maintaining good decisions.
    """
    if(depth == 0 and node == None):
        node = Entities.DeepimaxTreeNode(0)
        node.actions = queue.Queue().queue

    # Creating a new instance of the board
    currentBoard = Entities.Board()
    currentBoard.Copy(board)
    previousActions = node.actions.copy()

    # Updating the board
    for i in range(previousActions.__len__()):
        action = previousActions.popleft()
        currentBoard.Action(action[0], action[1])

    # Get list of available actions
    availableActions = []
    if(isMax):      
        availableActions = currentBoard.AvailableActionsFox()
    else:                
        availableActions = currentBoard.AvailableActionsSheep()

    # Check the leave (We are in the last depth or we have no children)
    if(depth == maxDepth or availableActions.__len__() == 0 or(roa == 0 and doa == 0)):
        node.point = currentBoard.EvaluationFunction()
        return node

    theNode = None
    tempChildren = []
    # Make the children
    for action in availableActions:
        child = Entities.DeepimaxTreeNode(node.depth + 1)
        newActions = node.actions.copy()
        newActions.append(action)
        child.actions = newActions
        if((depth % doa) == 0 and depth != 0):
            tempChildren.append(child)
        else:
            child.parent = node
            node.AddChildren(child)

    # Actual Deepimax Algorithms
    if((depth % doa) == 0 and depth != 0):
        # Expecting
        v = 0
        for child in tempChildren:
            temp = Deepimax(board, child, maxDepth, maxDepth, isMax, 0, 0)
            if(temp == None):
                continue
            v = v + temp.point
        node.point = v / tempChildren.__len__()
        return node
    else:
        for child in node.children:
            temp = Deepimax(board, child, depth +1, maxDepth, not isMax, doa, roa)
            if(temp == None):
                continue
            if((depth % doa) == doa -1): # Collective
                node.nominies.append(temp)
                continue
            else:
                node.nominies += temp.nominies
        theNode = node

    if((depth % doa) == 0):
        if(theNode.nominies.__len__() != 0): # We have nominees, so we re engage again
            theNode.nominies = sorted(theNode.nominies, key=lambda x: x.point, reverse = isMax)

            # Re-engage for 'range of accuracy' times
            results = []
            theMaxDepth = maxDepth - doa

            if(doa > 1):
                doa -= 1
                
            currentRoa = roa
            if(currentRoa > 1):
                currentRoa -= 1

            for i in range(roa):
                if(i > theNode.nominies.__len__() - 1):
                    break

                # Call
                if(theMaxDepth == 0):
                    results.append(theNode.nominies[i])
                else:
                    temp = Deepimax(board, theNode.nominies[i], 0, theMaxDepth, not isMax, doa, currentRoa)
                    if(temp != None):
                        results.append(temp)

            result = None
            if(isMax):
                result = max(results, key = lambda x: x.point)
            else:
                result = min(results, key = lambda x: x.point)

            theNode.point = result.point
            return result

        else:
            return theNode
    else:
        return theNode

