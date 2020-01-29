"""
Entities, objects and classes, data structures, helper functions are here.

We assume each position as a Tuple (x,y), which x and y are integers.
We assume each action as a Tuple (start, end), which starts and ends are positions.

Written by Ali Zandian (alizandian@outlook.com) for University project, researching a better way to gauge unlimited trees.
A project at the university of Ashrafi Esfahani.
"""

from enum import IntEnum
import queue

SM = 14             # Separation Multiplier for
SCountM = 10       # Sheeps Count Multiplier 
ADM = 20            # Average Distance Multiplier
AMM = 10            # Available Moves Multiplier
ACM = -10           # Available Captures Multiplier

MaxCountGame = 20
TurnTime = 60

class RoomType (IntEnum):
    Disable = 0
    Empty = 1
    Sheep = 2
    Fox = 3

class Turn (IntEnum):
    Sheeps = 0
    Fox = 1

class ControllerType(IntEnum):
    Bot = 0,
    Player = 1

class Strategy(IntEnum):
    Minimax = 0
    MinimaxPAB = 1
    Expectimax = 2
    Deepimax = 3

# Class of the board, containing the first initialization of board.
# And necessary functions to do on the board
class Board:
    # Initialize properties
    def __init__(self):
        self.fox = (3,4)
        self.sheeps = [(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(6,3),(6,4),(6,5),(7,3),(7,4),(7,5)]
        self.sheepsMax = 13
        self.rooms =   [[0,0,0,0,0,0,0,0,0],
                        [0,0,0,1,1,1,0,0,0],
                        [0,0,0,1,1,1,0,0,0],
                        [0,1,1,1,3,1,1,1,0],
                        [0,1,1,1,1,1,1,1,0],
                        [0,2,2,2,2,2,2,2,0],
                        [0,0,0,2,2,2,0,0,0],
                        [0,0,0,2,2,2,0,0,0],
                        [0,0,0,0,0,0,0,0,0]]

    def Copy(self, board):
        self.fox = board.fox
        self.sheeps.clear()
        for x in board.sheeps:
            self.sheeps.append(x)
        for r in range(len(board.rooms)):
            for c in range(len(board.rooms[r])):
                self.rooms[r][c] = board.rooms[r][c]
        self.sheepsMax = board.sheepsMax

    # Updates the Fox and Sheeps property
    def HeavyUpdate(self):
        self.sheeps = []
        for row in range(len(self.rooms) -2):
            for column in range(len(self.rooms[row +1]) -2):
                if(rooms[row +1][column +1] == 3):
                    self.fox = (row +1, column +1)
                if(rooms[row +1][column +1] == 2):
                    self.sheeps.append((row +1,column +1))

    # Get only diagonally neighbors of a room
    def __GetDiagonolyRooms(self, row, column):
        return [(row -1, column -1), (row -1, column +1),
                (row +1, column -1), (row +1, column +1)]

    # Get only straight neighbors of a room
    def __GetStraightRooms(self, row, column):
        return [(row -1, column),
                (row, column -1), (row, column +1),
                (row +1, column)]

    # Gets the neighbors of a room
    def Neighbors(self, row, column):
        neighbors = []
        output = []
        if((row == 0) or (row == 8) or (column == 0) or (column == 8)):
            neighbors = []
        elif(abs((row - column)) % 2 == 0):
            neighbors = self.__GetDiagonolyRooms(row,column) + self.__GetStraightRooms(row,column)
        else:
            neighbors = self.__GetStraightRooms(row,column) 

        for room in neighbors:
            if(self.rooms[room[0]][room[1]] != RoomType.Disable.value):
                output.append(room)

        return output

    def Action(self, start, end):
        if(self.rooms[end[0]][end[1]] != RoomType.Empty.value):
            return

        if(self.rooms[start[0]][start[1]] == RoomType.Sheep.value):
            self.sheeps.remove(start)
            self.sheeps.append(end)

        if(self.rooms[start[0]][start[1]] == RoomType.Fox.value):
            self.fox = end
            if(abs(end[0] - start[0]) == 2 or abs(end[1] - start[1]) == 2):
                possibleSheep = (int((end[0] + start[0])/2) , int((end[1] + start[1])/2))
                if(self.rooms[possibleSheep[0]][possibleSheep[1]] == RoomType.Sheep.value):
                    # Its a capture
                    self.rooms[possibleSheep[0]][possibleSheep[1]] = RoomType.Empty.value
                    self.sheeps.remove(possibleSheep)

        # Updating the board
        self.rooms[end[0]][end[1]] = self.rooms[start[0]][start[1]]
        self.rooms[start[0]][start[1]] = RoomType.Empty.value

    def ReverseAction(self, start, end):
        if(self.rooms[start[0]][start[1]] != RoomType.Empty.value):
            return

        if(self.rooms[end[0]][end[1]] == RoomType.Sheep.value):
            self.sheeps.remove(end)
            self.sheeps.append(start)

        if(self.rooms[end[0]][end[1]] == RoomType.Fox.value):
            self.fox = start

            if(abs(end[0] - start[0]) == 2 or abs(end[1] - start[1]) == 2):
                # It was a capture, Redo the capture by bringing a sheep inside
                previousSheep = ((end[0] + start[0])/2, (end[1] + start[1])/2)
                self.rooms[previousSheep[0]][previousSheep[1]] = RoomType.Sheep.value
                self.sheeps.append(previousSheep)

        # Updating the board
        self.rooms[start[0]][start[1]] = self.rooms[end[0]][end[1]]
        self.rooms[end[0]][end[1]] = RoomType.Empty.value

    def AvailableActionsFox(self):
        actions = []
        neighbors = self.Neighbors(self.fox[0], self.fox[1])
        for n in neighbors:
            if(self.rooms[n[0]][n[1]] == RoomType.Empty.value):
                actions.append((self.fox, n))
            elif (self.IsCapturable(n)):
                actions.append((self.fox, self.__GetCapturableRoom(n)))
        return actions

    def AvailableActionsSheep(self):
        actions = []
        for sheep in self.sheeps:
            neighbors = self.Neighbors(sheep[0], sheep[1])
            for n in neighbors:
                if(self.rooms[n[0]][n[1]] == RoomType.Empty.value):
                    actions.append((sheep, n))
        return actions

    def __GetCapturableRoom(self, room):
        if(self.IsCapturable(room)):
            return (room[0] + (room[0] - self.fox[0]), room[1] + (room[1] - self.fox[1]))

    def AvailableMoveCount(self):
        count = 0
        neighbors = self.Neighbors(self.fox[0], self.fox[1])
        for n in neighbors:
            if(self.rooms[n[0]][n[1]] == RoomType.Empty.value):
                count += 1
        return count

    def AvailableCaptureCount(self):
        count = 0
        neighbors = self.Neighbors(self.fox[0], self.fox[1])
        for n in neighbors:
            if(self.IsCapturable(n)):
                    count += 1
        return count

    def IsCapturable(self, room):
        if(self.rooms[room[0]][room[1]] == RoomType.Sheep.value):
                if(self.rooms[room[0] + (room[0] - self.fox[0])][room[1] + (room[1] - self.fox[1])] == RoomType.Empty.value):
                    return True

    def AverageFoxSheepDistance(self):
        count = 0
        totalDistance = 0
        for s in self.sheeps:
            count += 1
            totalDistance += abs(s[0] - self.fox[0]) + abs(s[1] - self.fox[1])

        return int(totalDistance / count)

    def SheepsSeperation(self):
        totalAdjacentEmptyRooms = 0
        for sheep in self.sheeps:
            neighbors = self.Neighbors(sheep[0], sheep[1])
            for n in neighbors:
                if(self.rooms[n[0]][n[1]] == RoomType.Empty.value):
                    totalAdjacentEmptyRooms += 1
        return int(totalAdjacentEmptyRooms / len(self.sheeps))

    def EvaluationFunction(self):
        global SCountM
        global AMM
        global ACM
        global ADM
        global SM

        if(len(self.sheeps) == 0):
            return 0

        return int((self.sheepsMax / len(self.sheeps))) * SCountM + self.AvailableMoveCount() * AMM + self.AvailableCaptureCount() * ACM + self.SheepsSeperation() * SM + self.AverageFoxSheepDistance() * ADM

class TreeNode:
    def __init__(self, depth):
        self.depth = depth
        self.parent = None
        self.children = []

    def AddChildren(self, *args):
        for x in args:
            self.children.append(x)
    
    def GetParent(self):
        return self.parent

    def GetChildren(self):
        return self.children

    def GetLeaves(self):
        if(len(self.children) != 0):
            leaves = []
            for x in self.children:
                leaves += x.GetLeaves()
            return leaves
        return [self]

    def GetTop(self):
        if(self.parent != None):
            return self.parent.GetTop()
        return self

    def GetDepthNodes(self, depth):
        if(depth == 0):
            return [self]
        elif(len(self.GetChildren()) == 0):
            return []
        else:
            nodes = []
            for x in self.GetChildren():
                nodes += x.GetDepthNodes(depth -1)
            return nodes

    def GetNeighburs(self):
        if(self.parent == None):
            return self
        return self.parent.GetChildren()

    def SameDepthNodes(self):
        if(self.parent != None):
            return self.GetTop().GetDepthNodes(self.depth)
        return self

    def GetBottom(self):
        leaves = self.GetLeaves()
        return max(leaves, key = lambda x: x.depth)
    
class MinimaxTreeNode(TreeNode):
    def __init__(self, depth):
        super().__init__(depth)
        self.actions = queue.Queue().queue
        self.point = None

class DeepimaxTreeNode(MinimaxTreeNode):
    def __init__(self, depth):
        super().__init__(depth)
        self.nominies = []

class Controller():
    def __init__(self):
        self.title = None

    def Action(self, board, turn):
        self.turn = turn
        self.board = board
        pass