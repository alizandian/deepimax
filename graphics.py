"""
This class is responsible for all display materials, game-board, etc...
It contains animation and necessary pictures.
This has an update, refresh, and other options.

Written by Ali Zandian (alizandian@outlook.com) for University project, researching a better way to gauge unlimited trees.
A project at the university of Ashrafi Esfahani.
"""

import tkinter as Tkinter
import tkinter.ttk as Ttk
import entities as Entities

class Display():
    """
    Main object of graphics module. It draws board and control frames and their 
    widgets and of has update
    """

    #region Options to manipulate with the window
    TILEWIDTH = 80
    TILEHEIGHT = 80
    ROOMSIZE = 40
    ROUTWIDTH = 3
    TILECOUNTS = 6
    ROOMCOLOR = "#211b0f"
    FOXCOLOR = "orange"
    SHEEPCOLOR = "#31af5d"
    BACKGROUNDCOLOR = "#9b5628"
    MOVESPEED = 0.2
    UPDATEDELTATIME = 20
    #endregion
    def __init__(self, title, themeColor):
        """
        Initialization of the display. 
        Mainly it construct frames of window, the title and the theme color.
        It also grids the frames so their positioning to respect to each other is fixed. 
        """
        self.mainFrame = Tkinter.Tk()
        self.mainFrame.resizable(width = 0, height = 0)
        self.title = title
        self.mainFrame.title(title)
        self.themeColor = themeColor
        self.gameplayFrame = Tkinter.Frame(master = self.mainFrame)
        self.controlFrame = Tkinter.Frame(master = self.mainFrame, width = 200, borderwidth=5, background = themeColor)
        self.variableFrame = Tkinter.Frame(master = self.mainFrame, width = 200, borderwidth=5, background = themeColor)
        self.gameplayFrame.grid(column = 1, row = 0)
        self.controlFrame.grid(column = 0, row = 0, sticky = Tkinter.W)
        self.controlFrame.grid_propagate(0)
        self.variableFrame.grid(column = 2, row = 0, sticky = Tkinter.E)
        self.variableFrame.grid_propagate(0)
        self.foxNameLabel = None
        self.foxNameEntry = None
        self.foxDOALabel = None
        self.foxDOAEntry = None
        self.foxROALabel = None
        self.foxROAEntry = None
        self.sheepsNameLabel = None
        self.sheepsNameEntry = None
        self.sheepsDOALabel = None
        self.sheepsDOAEntry = None
        self.sheepsROALabel = None
        self.sheepsROAEntry = None
        self.canvas = None
        self.foxStrategyLabel = None
        self.foxStrategiesComboBox = None
        self.foxDepthLabel = None
        self.foxDepthEntry = None
        self.sheepsStrategyLabel = None
        self.sheepsStrategiesComboBox = None
        self.sheepsDepthLabel = None
        self.sheepsDepthEntry = None
        self.currentTurn = None
        self.remainingTime = None
        self.guiDrawed = False

        # Calling Routines
        self.__Tick()

    def Initialization(self, board):
        """
        This initialize everything in the main window. It can be used for reseting the whole display.
        """

        self.currentTurn = None
        self.remainingTime = None
        # Creating the canvas

        if(self.canvas != None):
            self.canvas.delete('all')
        else:
            self.canvas = Tkinter.Canvas(master = self.gameplayFrame,
                    bg = Display.BACKGROUNDCOLOR,
                    height = Display.TILEHEIGHT * Display.TILECOUNTS + Display.ROOMSIZE,
                    width = Display.TILEWIDTH * Display.TILECOUNTS + Display.ROOMSIZE)


        # Setting the height of the Control frame and Variable frame equal to the canvas frame
        self.controlFrame.config(height = self.canvas.winfo_reqheight())
        self.variableFrame.config(height = self.canvas.winfo_reqheight())
        self.__DrawBoard(board)

        if(self.guiDrawed == False):
            self.__DrawGUI()
            self.guiDrawed = True

    def __DrawBoard(self, board):
        """
        Gets an instance of a board and displays it in the gameplay frame, the canvas.
        """
        if(self.canvas == None):
            self.Initialization()
        else:
            self.canvas.delete("all")

        for row in range(len(board.rooms) -2):
            for column in range(len(board.rooms[row +1]) -2):
                neighbors = []
                if(board.rooms[row +1][column +1] != 0):
                    neighbors = board.Neighbors(row +1, column +1)

                # Draw lines between rooms
                for n in neighbors:
                    targetRow = n[0] -1
                    targetColumn = n[1] -1
                    self.canvas.create_line((column * Display.TILEWIDTH) + Display.ROOMSIZE/2,
                                (row * Display.TILEHEIGHT) + Display.ROOMSIZE/2,
                                (targetColumn * Display.TILEWIDTH) + Display.ROOMSIZE/2,
                                (targetRow * Display.TILEHEIGHT) + Display.ROOMSIZE/2,
                                fill = Display.ROOMCOLOR,
                                width = Display.ROUTWIDTH)

                # Draw rooms
                if(board.rooms[row +1][column +1] != 0):
                    self.canvas.create_oval(column * Display.TILEWIDTH,
                                row * Display.TILEHEIGHT,
                                (column * Display.TILEWIDTH) + Display.ROOMSIZE,
                                (row * Display.TILEHEIGHT) + Display.ROOMSIZE,
                                fill = Display.ROOMCOLOR)     

        # Draw Fox
        self.canvas.create_oval((board.fox[1] -1) * Display.TILEWIDTH,
                    (board.fox[0] -1) * Display.TILEHEIGHT,
                    ((board.fox[1] -1) * Display.TILEWIDTH) + Display.ROOMSIZE,
                    ((board.fox[0] -1) * Display.TILEHEIGHT) + Display.ROOMSIZE,
                    fill = Display.FOXCOLOR,
                    tags = PosToTag(board.fox))

        # Draw Sheeps
        for sheep in board.sheeps:
            self.canvas.create_oval((sheep[1] -1) * Display.TILEWIDTH,
                    (sheep[0] -1) * Display.TILEHEIGHT,
                    ((sheep[1] -1) * Display.TILEWIDTH) + Display.ROOMSIZE,
                    ((sheep[0] -1) * Display.TILEHEIGHT) + Display.ROOMSIZE, 
                    fill = Display.SHEEPCOLOR,
                    tags = PosToTag(sheep))

        self.canvasFoxLabel = self.canvas.create_text(90, 30, font=("Tahoma", 20, "bold"), text= "Fox", fill = self.FOXCOLOR)
        self.canvasFoxTitle = self.canvas.create_text(90, 55, font=("Tahoma", 12), text ="", fill = self.FOXCOLOR)
        self.canvasFoxTimer = self.canvas.create_text(90, 120, font=("Tahoma", 20, "bold"), text= "", fill = self.FOXCOLOR)
        self.canvasFoxUnderLine = self.canvas.create_rectangle(25, 10, 150, 150, outline = self.FOXCOLOR, width = 0)
        self.canvasSheepsLabel = self.canvas.create_text(435, 30, font=("Tahoma", 20, "bold"), text= "Sheeps", fill = self.SHEEPCOLOR)
        self.canvasSheepsTitle = self.canvas.create_text(435, 55, font=("Tahoma", 12), text = "", fill = self.SHEEPCOLOR)
        self.canvasSheepsTimer = self.canvas.create_text(435, 120, font=("Tahoma", 20, "bold"), text= "", fill = self.SHEEPCOLOR)
        self.canvasSheepsUnderLine = self.canvas.create_rectangle(370, 10, 500, 150, outline = self.SHEEPCOLOR, width = 0)
        self.canvas.pack()

    def __DrawGUI(self):
        #region Control Frame
        #==================
        # Label of the Fox:
        #==================
        self.foxLabel = Tkinter.Label(master = self.controlFrame, text = "Fox: ", width = 8, background = self.FOXCOLOR)
        self.foxLabel.grid(row = 0, column = 0, padx = 4, sticky = Tkinter.W)

        #================================
        # Combo box of the fox controller
        #================================
        self.foxControllerVar = Tkinter.StringVar()
        self.foxControllerComboBox = Ttk.Combobox(master = self.controlFrame, textvariable = self.foxControllerVar, width = 16)
        self.foxControllerComboBox['values'] = ('Bot', 'Player')
        self.foxControllerComboBox.bind("<<ComboboxSelected>>", self.__OnFoxComboBoxChange)
        self.foxControllerComboBox.grid(row = 0, column = 1)


        #====================
        # Label of the Sheeps
        #====================
        self.SheepsLabel = Tkinter.Label(master = self.controlFrame, text = "Sheeps: ", width = 8, background = self.SHEEPCOLOR)
        self.SheepsLabel.grid(row = 5, column = 0, padx = 4, pady = (4, 0), sticky = Tkinter.W)

        #===================================
        # Combo box of the sheeps controller
        #===================================
        self.sheepsControllerVar = Tkinter.StringVar()
        self.sheepsControllerComboBox = Ttk.Combobox(master = self.controlFrame, textvariable = self.sheepsControllerVar, width = 16)
        self.sheepsControllerComboBox['values'] = ('Bot', 'Player')
        self.sheepsControllerComboBox.bind("<<ComboboxSelected>>", self.__OnSheepsComboBoxChange)
        self.sheepsControllerComboBox.grid(row = 5, column = 1, pady = (4, 0))

        #=================
        # Label of the Turn
        #=================
        self.turnLabel = Tkinter.Label(master = self.controlFrame, text = "First Turn: ", width = 8, background = self.themeColor)
        self.turnLabel.grid(row =12, column = 0, pady = (10, 0), sticky = Tkinter.W)

        #======================
        # Radio button for turn
        #======================
        self.turnRadioVar = Tkinter.IntVar()
        self.turnFoxRadio = Tkinter.Radiobutton(master = self.controlFrame, text = "Fox", variable = self.turnRadioVar,
                                                value = 1, background = self.FOXCOLOR)
        self.turnFoxRadio.grid(row = 13, column = 0, sticky = Tkinter.W)
        self.turnSheepsRadio = Tkinter.Radiobutton(master = self.controlFrame, text = "Sheeps", variable = self.turnRadioVar,
                                                   value = 2, background = self.SHEEPCOLOR)
        self.turnSheepsRadio.grid(row = 14, column = 0, sticky = Tkinter.W)
        self.turnRandomRadio = Tkinter.Radiobutton(master = self.controlFrame, text = "Random", variable = self.turnRadioVar,
                                                   value = 3, background = self.themeColor)
        self.turnRandomRadio.grid(row = 15, column = 0, sticky = Tkinter.W)
        self.turnRadioVar.set(1)

        #===============
        # Max Move Entry
        #===============
        self.maxMoveCountLabel = Tkinter.Label(master = self.controlFrame, text = "Max Moves: ", width = 8, backgroun = self.themeColor)
        self.maxMoveCountLabel.grid(row = 16, column = 0, sticky = Tkinter.E, pady = (10, 0))
        self.maxMoveCountVar = Tkinter.StringVar()
        self.maxMoveCountVar.set(str(Entities.MaxCountGame))
        self.maxMoveCountEntry = Tkinter.Entry(master = self.controlFrame, textvariable = self.maxMoveCountVar, width = 10)
        self.maxMoveCountEntry.grid(row = 16, column = 1, sticky = Tkinter.W, pady = (10,0))

        #================
        # Turn Time Entry
        #================
        self.turnTimeLabel = Tkinter.Label(master = self.controlFrame, text = "Turn Time: ", width = 8, background = self.themeColor)
        self.turnTimeLabel.grid(row = 17, column = 0, sticky = Tkinter.E)
        self.turnTimeVar = Tkinter.StringVar()
        self.turnTimeVar.set(str(Entities.TurnTime))
        self.turnTimeEntry = Tkinter.Entry(master = self.controlFrame, textvariable = self.turnTimeVar, width = 10)
        self.turnTimeEntry.grid(row = 17, column = 1, sticky = Tkinter.W)

        #===========================
        # Bottoms of Reset and Start
        #===========================
        self.startButton = Tkinter.Button(master = self.controlFrame, text = "Start")
        self.startButton.place(x = 1, y = 430, bordermode = Tkinter.INSIDE, height = 40, width=190)
        self.resetButton = Tkinter.Button(master = self.controlFrame, text = "Reset")
        self.resetButton.place(x = 1, y = 475, bordermode = Tkinter.INSIDE, height = 40, width=190)
        #endregion

        #region Variable Frame
        #==========================
        # Label Frame of statistics, Evaluation Multipliers and Accept Button
        #=========================
        self.statisticsFrame = Tkinter.LabelFrame(master = self.variableFrame, text = "Graphs and Statistics", width = 190, height = 270, backgroun = self.themeColor)
        self.statisticsFrame.grid(row = 0, column = 0)
        self.statisticsFrame.grid_propagate(0)

        self.multipliersFrame = Tkinter.LabelFrame(master = self.variableFrame, text = "Evaluation Multipliers", width = 190, height = 200, background = self.themeColor)
        self.multipliersFrame.grid(row = 1, column = 0)
        self.multipliersFrame.grid_propagate(0)

        self.acceptButton = Tkinter.Button(master = self.variableFrame, text = "Accept!", width = 25, height = 2, command = self.AcceptMultipliers)
        self.acceptButton.grid(row = 2, column = 0, pady = (5,0))

        #==================================
        # Statistics Buttons and radioBoxes
        #==================================

        # Draw Tree part
        self.drawTreeCheckVar = Tkinter.IntVar()
        drawTreeLabel = Tkinter.Label(master = self.statisticsFrame, text = "Draw Tree: ", width = 8, background = self.themeColor)
        drawTreeCheckBox = Tkinter.Checkbutton(master = self.statisticsFrame, variable = self.drawTreeCheckVar , background = self.themeColor)
        drawTreeLabel.grid(row = 1, column = 0, sticky = Tkinter.E)
        drawTreeCheckBox.grid(row = 1, column = 1, sticky = Tkinter.E)

        # Comparison part
        self.compareVar = Tkinter.IntVar()
        compareCheckBox = Tkinter.Checkbutton(master = self.statisticsFrame, variable = self.compareVar, background = self.themeColor)
        comparisionLabel = Tkinter.Label(master = self.statisticsFrame, text = "Compare: ", width = 8, background = self.themeColor)
        compareTimeLabel = Tkinter.Label(master = self.statisticsFrame, text = "Time: ", width = 8, background = self.themeColor)
        compareSpaceLabel = Tkinter.Label(master = self.statisticsFrame, text = "Space: ", width = 8, background = self.themeColor)
        compareBasicLabel = Tkinter.Label(master = self.statisticsFrame, text = "Basic: ", width = 8, background = self.themeColor)
        self.compareTypeRadioVar = Tkinter.IntVar()

        compareTimeRadio = Tkinter.Radiobutton(master = self.statisticsFrame, background = self.themeColor, value = 1, 
                                               variable = self.compareTypeRadioVar)
        compareSpaceRadio = Tkinter.Radiobutton(master = self.statisticsFrame, background = self.themeColor, value = 2, 
                                               variable = self.compareTypeRadioVar)
        compareBasicRadio = Tkinter.Radiobutton(master = self.statisticsFrame, background = self.themeColor, value = 3, 
                                               variable = self.compareTypeRadioVar)


        comparisionLabel.grid(row = 3, column = 0, sticky = Tkinter.E)
        compareCheckBox.grid(row = 3, column = 1, sticky = Tkinter.E)
        compareTimeLabel.grid(row = 5, column = 1, sticky = Tkinter.W)
        compareTimeRadio.grid(row = 5, column = 2, sticky = Tkinter.E)
        compareSpaceLabel.grid(row = 4, column = 1, sticky = Tkinter.W)
        compareSpaceRadio.grid(row = 4, column = 2, sticky = Tkinter.E)
        compareBasicLabel.grid(row = 6, column = 1, sticky = Tkinter.W)
        compareBasicRadio.grid(row = 6, column = 2, sticky = Tkinter.E)

        # Default value of radioBoxes
        self.compareTypeRadioVar.set(3)



        #==============================
        # Graph and Statistics Options
        #==============================


        #==============================
        # Evaluation Multipliers Labels
        #==============================
        self.SMLabel = Tkinter.Label(master = self.multipliersFrame, text = "SM:", width = 8, background = self.themeColor)
        self.SCMLabel = Tkinter.Label(master = self.multipliersFrame, text = "SCM:", width = 8, background = self.themeColor)
        self.ADMLabel = Tkinter.Label(master = self.multipliersFrame, text = "ADM:", width = 8, background = self.themeColor)
        self.AMMLabel = Tkinter.Label(master = self.multipliersFrame, text = "AMM:", width = 8, background = self.themeColor)
        self.ACMLabel = Tkinter.Label(master = self.multipliersFrame, text = "ACM:", width = 8, background = self.themeColor)
        self.SMLabel.grid(row = 1, column = 0, sticky = Tkinter.E)
        self.SCMLabel.grid(row = 2, column = 0, sticky = Tkinter.E)
        self.ADMLabel.grid(row = 3, column = 0, sticky = Tkinter.E)
        self.AMMLabel.grid(row = 4, column = 0, sticky = Tkinter.E)
        self.ACMLabel.grid(row = 5, column = 0, sticky = Tkinter.E)

        #===============================
        # Evaluation Multipliers Entries
        #===============================
        # Fox Evaluation Variables
        self.SMVar = Tkinter.StringVar()
        self.SCMVar = Tkinter.StringVar()
        self.ADMVar = Tkinter.StringVar()
        self.AMMVar = Tkinter.StringVar()
        self.ACMVar = Tkinter.StringVar()

        # Evaluation Entires
        self.SMEntry = Tkinter.Entry(master = self.multipliersFrame, textvariable = self.SMVar, width = 8)
        self.SCMEntry = Tkinter.Entry(master = self.multipliersFrame, textvariable = self.SCMVar, width = 8)
        self.ADMEntry = Tkinter.Entry(master = self.multipliersFrame, textvariable = self.ADMVar, width = 8)
        self.AMMEntry = Tkinter.Entry(master = self.multipliersFrame, textvariable = self.AMMVar, width = 8)
        self.ACMEntry = Tkinter.Entry(master = self.multipliersFrame, textvariable = self.ACMVar, width = 8)
        self.SMEntry.grid(row = 1, column = 1)
        self.SCMEntry.grid(row = 2, column = 1)
        self.ADMEntry.grid(row = 3, column = 1)
        self.AMMEntry.grid(row = 4, column = 1)
        self.ACMEntry.grid(row = 5, column = 1)

        #=========================================
        # Setting Default values of Entries values
        #=========================================
        self.SMVar.set(str(Entities.SM))
        self.SCMVar.set(str(Entities.SCountM))
        self.ACMVar.set(str(Entities.ACM))
        self.AMMVar.set(str(Entities.AMM))
        self.ADMVar.set(str(Entities.ADM))
        #endregion

    def __OnFoxComboBoxChange(self, event):
        if(event.widget.get() == 'Bot'):
            # Destroy collusion widgets
            if(self.foxNameLabel):
                self.foxNameLabel.destroy()
                self.foxNameLabel = None
            if(self.foxNameEntry):
                self.foxNameEntry.destroy()
                self.foxNameEntry = None

            # Draw Strategies of the bot fox
            if(not self.foxStrategiesComboBox):
                self.__DrawFoxStrategies()

        if(event.widget.get() == 'Player'):
            # Destroy collusion widgets
            self.__destroyFoxStrategyDependences()

            # Draw player name text
            if(not self.foxNameEntry):
                self.__DrawFoxNameEntry()

    def __OnSheepsComboBoxChange(self, event):
        if(event.widget.get() == 'Bot'):
            # Destroy collusion widgets
            if(self.sheepsNameLabel):
                self.sheepsNameLabel.destroy()
                self.sheepsNameLabel = None
            if(self.sheepsNameEntry):
                self.sheepsNameEntry.destroy()
                self.sheepsNameEntry = None

            # Draw Strategies of the bot fox
            if(not self.sheepsStrategiesComboBox):
                self.__DrawSheepsStrategies()

        if(event.widget.get() == 'Player'):
            # Destroy collusion widgets
            self.__destroySheepsStrategyDependences()

            # Draw player name text
            if(not self.sheepsNameEntry):
                self.__DrawSheepsNameEntry()

    def __destroyFoxStrategyDependences(self):
        if(self.foxStrategyLabel):
            self.foxStrategyLabel.destroy()
            self.foxStrategyLabel = None
        if(self.foxStrategiesComboBox):
            self.foxStrategiesComboBox.destroy()
            self.foxStrategiesComboBox = None
        if(self.foxDepthLabel):
            self.foxDepthLabel.destroy()
            self.foxDepthLabel = None
        if(self.foxDepthEntry):
            self.foxDepthEntry.destroy()
            self.foxDepthEntry = None
        if(self.foxDOALabel):
            self.foxDOALabel.destroy()
            self.foxDOALabel = None
        if(self.foxDOAEntry):
            self.foxDOAEntry.destroy()
            self.foxDOAEntry = None
        if(self.foxROALabel):
            self.foxROALabel.destroy()
            self.foxROALabel = None
        if(self.foxROAEntry):
            self.foxROAEntry.destroy()
            self.foxROAEntry = None

    def __destroySheepsStrategyDependences(self):
        if(self.sheepsStrategyLabel):
            self.sheepsStrategyLabel.destroy()
            self.sheepsStrategyLabel = None
        if(self.sheepsStrategiesComboBox):
            self.sheepsStrategiesComboBox.destroy()
            self.sheepsStrategiesComboBox = None
        if(self.sheepsDepthLabel):
            self.sheepsDepthLabel.destroy()
            self.sheepsDepthLabel = None
        if(self.sheepsDepthEntry):
            self.sheepsDepthEntry.destroy()
            self.sheepsDepthEntry = None
        if(self.sheepsDOALabel):
            self.sheepsDOALabel.destroy()
            self.sheepsDOALabel = None
        if(self.sheepsDOAEntry):
            self.sheepsDOAEntry.destroy()
            self.sheepsDOAEntry = None
        if(self.sheepsROALabel):
            self.sheepsROALabel.destroy()
            self.sheepsROALabel = None
        if(self.sheepsROAEntry):
            self.sheepsROAEntry.destroy()
            self.sheepsROAEntry = None


    def __OnFoxStrategyComboBoxChange(self, event):
        if(event.widget.get() == Entities.Strategy.Minimax.name):
            if(not self.foxDepthEntry):
                self.__DrawFoxDepthText()
        else:
            if(self.foxDepthLabel):
                self.foxDepthLabel.destroy()
                self.foxDepthLabel = None
            if(self.foxDepthEntry):
                self.foxDepthEntry.destroy()
                self.foxDepthEntry = None

        if(event.widget.get() == Entities.Strategy.MinimaxPAB.name):
            if(not self.foxDepthEntry):
                self.__DrawFoxDepthText()
            else:
                if(self.foxDepthLabel):
                    self.foxDepthLabel.destroy()
                    self.foxDepthLabel = None
                if(self.foxDepthEntry):
                    self.foxDepthEntry.destroy()
                    self.foxDepthEntry = None
            
        if(event.widget.get() == Entities.Strategy.Expectimax.name):
            if(not self.foxDepthEntry):
                self.__DrawFoxDepthText()
            else:
                if(self.foxDepthLabel):
                    self.foxDepthLabel.destroy()
                    self.foxDepthLabel = None
                if(self.foxDepthEntry):
                    self.foxDepthEntry.destroy()
                    self.foxDepthEntry = None

        if(event.widget.get() == Entities.Strategy.Deepimax.name):
            if(not self.foxDepthEntry):
                self.__DrawFoxDepthText()
                self.__DrawFoxDeepiRequirenments()
            else:
                if(self.foxDepthLabel):
                    self.foxDepthLabel.destroy()
                    self.foxDepthLabel = None
                if(self.foxDepthEntry):
                    self.foxDepthEntry.destroy()
                    self.foxDepthEntry = None
        else:
            if(self.foxDOALabel):
                self.foxDOALabel.destroy()
                self.foxDOALabel = None
            if(self.foxDOAEntry):
                self.foxDOAEntry.destroy()
                self.foxDOAEntry = None
            if(self.foxROALabel):
                self.foxROALabel.destroy()
                self.foxROALabel = None
            if(self.foxROAEntry):
                self.foxROAEntry.destroy()
                self.foxROAEntry = None

    def __OnSheepsStrategyComboBoxChange(self, event):
        if(event.widget.get() == Entities.Strategy.Minimax.name):
            self.__DrawSheepsDepthText()
        else:
            if(self.sheepsDepthLabel):
                self.sheepsDepthLabel.destroy()
                self.sheepsDepthLabel = None
            if(self.sheepsDepthEntry):
                self.sheepsDepthEntry.destroy()
                self.sheepsDepthEntry = None

        if(event.widget.get() == Entities.Strategy.MinimaxPAB.name):
            if(not self.sheepsDepthEntry):
                self.__DrawSheepsDepthText()
            else:
                if(self.sheepsDepthLabel):
                    self.sheepsDepthLabel.destroy()
                    self.sheepsDepthLabel = None
                if(self.sheepsDepthEntry):
                    self.sheepsDepthEntry.destroy()
                    self.sheepsDepthEntry = None

        if(event.widget.get() == Entities.Strategy.Expectimax.name):
            if(not self.sheepsDepthEntry):
                self.__DrawSheepsDepthText()
            else:
                if(self.sheepsDepthLabel):
                    self.sheepsDepthLabel.destroy()
                    self.sheepsDepthLabel = None
                if(self.sheepsDepthEntry):
                    self.sheepsDepthEntry.destroy()
                    self.sheepsDepthEntry = None


        if(event.widget.get() == Entities.Strategy.Deepimax.name):
            if(not self.sheepsDepthEntry):
                self.__DrawSheepsDepthText()
                self.__DrawSheepsDeepiRequirenments()
            else:
                if(self.sheepsDepthLabel):
                    self.sheepsDepthLabel.destroy()
                    self.sheepsDepthLabel = None
                if(self.sheepsDepthEntry):
                    self.sheepsDepthEntry.destroy()
                    self.sheepsDepthEntry = None
        else:
            if(self.sheepsDOALabel):
                self.sheepsDOALabel.destroy()
                self.sheepsDOALabel = None
            if(self.sheepsDOAEntry):
                self.sheepsDOAEntry.destroy()
                self.sheepsDOAEntry = None
            if(self.sheepsROALabel):
                self.sheepsROALabel.destroy()
                self.sheepsROALabel = None
            if(self.sheepsROAEntry):
                self.sheepsROAEntry.destroy()
                self.sheepsROAEntry = None

    def __DrawFoxStrategies(self):
        self.foxStrategyLabel = Tkinter.Label(master = self.controlFrame, text = "Strategy: ", width = 8, background = self.FOXCOLOR)
        self.foxStrategyLabel.grid(row = 1, column = 0, padx = 4)
        self.foxStrategiesVar = Tkinter.StringVar()
        self.foxStrategiesComboBox = Ttk.Combobox(master = self.controlFrame, textvariable = self.foxStrategiesVar, width = 16)
        self.foxStrategiesComboBox['values'] = tuple(x.name for x in Entities.Strategy)
        self.foxStrategiesComboBox.bind("<<ComboboxSelected>>", self.__OnFoxStrategyComboBoxChange)
        self.foxStrategiesComboBox.grid(row = 1, column = 1)

    def __DrawFoxDepthText(self):
        self.foxDepthLabel = Tkinter.Label(master = self.controlFrame, text = "Depth: ", width = 8, background = self.FOXCOLOR)
        self.foxDepthLabel.grid(row = 2, column = 0, padx = 4)
        self.foxDepthVar = Tkinter.StringVar()
        self.foxDepthVar.set(str(1))
        self.foxDepthEntry = Tkinter.Entry(master = self.controlFrame, textvariable = self.foxDepthVar, width = 16)
        self.foxDepthEntry.grid(row = 2, column = 1)

    def __DrawFoxDeepiRequirenments(self):
        # Depth of accuracy part
        self.foxDOALabel = Tkinter.Label(master = self.controlFrame, text = "DOA: ", width = 8, background = self.FOXCOLOR)
        self.foxDOALabel.grid(row = 3, column = 0, padx = 4)
        self.foxDOAVar = Tkinter.StringVar()
        self.foxDOAVar.set(str(1))
        self.foxDOAEntry = Tkinter.Entry(master = self.controlFrame, textvariable = self.foxDOAVar, width = 16)
        self.foxDOAEntry.grid(row = 3, column = 1)

        # Range of accuracy part
        self.foxROALabel = Tkinter.Label(master = self.controlFrame, text = "ROA: ", width = 8, background = self.FOXCOLOR)
        self.foxROALabel.grid(row = 4, column = 0, padx = 4)
        self.foxROAVar = Tkinter.StringVar()
        self.foxROAVar.set(str(1))
        self.foxROAEntry = Tkinter.Entry(master = self.controlFrame, textvariable = self.foxROAVar, width = 16)
        self.foxROAEntry.grid(row = 4, column = 1)

    def __DrawFoxNameEntry(self):
        self.foxNameLabel = Tkinter.Label(master = self.controlFrame, text = "Name: ", width = 8, background = self.FOXCOLOR)
        self.foxNameLabel.grid(row = 1, column = 0, padx = 4)
        self.foxNameVar = Tkinter.StringVar()
        self.foxNameEntry = Tkinter.Entry(master = self.controlFrame, textvariable = self.foxNameVar, width = 16)
        self.foxNameEntry.grid(row = 1, column = 1)

    def __DrawSheepsStrategies(self):
        self.sheepsStrategyLabel = Tkinter.Label(master = self.controlFrame, text = "Strategy: ", width = 8, background = self.SHEEPCOLOR)
        self.sheepsStrategyLabel.grid(row = 6, column = 0, padx = 4)
        self.sheepsStrategiesVar = Tkinter.StringVar()
        self.sheepsStrategiesComboBox = Ttk.Combobox(master = self.controlFrame, textvariable = self.sheepsStrategiesVar, width = 16)
        self.sheepsStrategiesComboBox['values'] = tuple(x.name for x in Entities.Strategy)
        self.sheepsStrategiesComboBox.bind("<<ComboboxSelected>>", self.__OnSheepsStrategyComboBoxChange)
        self.sheepsStrategiesComboBox.grid(row = 6, column = 1)

    def __DrawSheepsDepthText(self):
        self.sheepsDepthLabel = Tkinter.Label(master = self.controlFrame, text = "Depth: ", width = 8, background = self.SHEEPCOLOR)
        self.sheepsDepthLabel.grid(row = 7, column = 0, padx = 4)
        self.sheepsDepthVar = Tkinter.StringVar()
        self.sheepsDepthVar.set(str(1))
        self.sheepsDepthEntry = Tkinter.Entry(master = self.controlFrame, textvariable = self.sheepsDepthVar, width = 16)
        self.sheepsDepthEntry.grid(row = 7, column = 1)

    def __DrawSheepsNameEntry(self):
        self.sheepsNameLabel = Tkinter.Label(master = self.controlFrame, text = "Name: ", width = 8, background = self.SHEEPCOLOR)
        self.sheepsNameLabel.grid(row = 6, column = 0, padx = 4)
        self.sheepsNameVar = Tkinter.StringVar()
        self.sheepsNameEntry = Tkinter.Entry(master = self.controlFrame, textvariable = self.sheepsNameVar, width = 16)
        self.sheepsNameEntry.grid(row = 6, column = 1)

    def __DrawSheepsDeepiRequirenments(self):
        # Depth of accuracy part
        self.sheepsDOALabel = Tkinter.Label(master = self.controlFrame, text = "DOA: ", width = 8, background = self.SHEEPCOLOR)
        self.sheepsDOALabel.grid(row = 8, column = 0, padx = 4)
        self.sheepsDOAVar = Tkinter.StringVar()
        self.sheepsDOAVar.set(str(1))
        self.sheepsDOAEntry = Tkinter.Entry(master = self.controlFrame, textvariable = self.sheepsDOAVar, width = 16)
        self.sheepsDOAEntry.grid(row = 8, column = 1)

        # Range of accuracy part
        self.sheepsROALabel = Tkinter.Label(master = self.controlFrame, text = "ROA: ", width = 8, background = self.SHEEPCOLOR)
        self.sheepsROALabel.grid(row = 9, column = 0, padx = 4)
        self.sheepsROAVar = Tkinter.StringVar()
        self.sheepsROAVar.set(str(1))
        self.sheepsROAEntry = Tkinter.Entry(master = self.controlFrame, textvariable = self.sheepsROAVar, width = 16)
        self.sheepsROAEntry.grid(row = 9, column = 1)

    def __Tick(self):
        # After 1 second -> Update Time
        if(self.currentTurn != None and self.remainingTime != None):
            if(self.remainingTime > 0):
                self.remainingTime -= 1
                self.__DrawCanvasTimer()

        self.mainFrame.after(1000, self.__Tick)

    def __DrawCanvasTimer(self):
        if(self.currentTurn == Entities.Turn.Fox):
            self.canvas.itemconfig(self.canvasFoxTimer, text = str(self.remainingTime))
            self.canvas.itemconfig(self.canvasSheepsTimer, text = "")
        else:
            self.canvas.itemconfig(self.canvasSheepsTimer, text = str(self.remainingTime))
            self.canvas.itemconfig(self.canvasFoxTimer, text = "")

    def MoveUnit(self, start, end):
        oldTag = PosToTag(start)
        newTag = PosToTag(end)
        unit = self.canvas.find_withtag(oldTag)
        if(unit is None):
            return
        self.canvas.addtag_withtag(newTag, oldTag)
        self.canvas.dtag(unit, oldTag)
        self.canvas.tag_raise(unit)
        for x in range(int(Display.TILEHEIGHT / Display.MOVESPEED)):
            self.canvas.move(unit, (end[1] - start[1]) * Display.MOVESPEED, (end[0] - start[0]) * Display.MOVESPEED)
            
        # Check for capture
        if(abs(end[1] - start[1]) == 2 or abs(end[0] - start[0]) == 2):
            sheepTag = PosToTag((
                int((start[0] + end[0]) /2) ,
                int((start[1] + end[1]) /2)
                ))
            sheep = self.canvas.find_withtag(sheepTag)
            if(sheep is not None):
                self.canvas.delete(sheepTag)

    def SetStartHandler(self,func):
        self.startButton.config(command = func)

    def SetResetHandler(self, func):
        self.resetButton.config(command = func)

    def AcceptMultipliers(self):
        try:
            Entities.ACM = int(self.ACMEntry.get())
            Entities.ADM = int(self.ADMEntry.get())
            Entities.AMM = int(self.AMMEntry.get())
            Entities.SCountM = int(self.SCMEntry.get())
            Entities.SM = int(self.SMEntry.get())

        except:
            pass

    def Running(self):
        self.startButton.config(state = Tkinter.DISABLED)

    def Ended(self):
        self.startButton.config(state = Tkinter.NORMAL)
        self.resetButton.config(state = Tkinter.NORMAL)

    def Stopped(self):
        self.resetButton.config(state = Tkinter.DISABLED)

    def SetControllersInfo(self, foxController, sheepsController):
        self.canvas.itemconfig(self.canvasFoxTitle, text = 'Bot ' + foxController.title)
        self.canvas.itemconfig(self.canvasSheepsTitle, text = 'Bot ' + sheepsController.title)

    def TurnStarted(self, turn, time):
        self.currentTurn = turn
        self.remainingTime = time
        self.__DrawCanvasTimer()
        if(turn == Entities.Turn.Fox):
            self.canvas.itemconfig(self.canvasFoxUnderLine, width = 5)
            self.canvas.itemconfig(self.canvasSheepsUnderLine, width = 0)
        else:
            self.canvas.itemconfig(self.canvasFoxUnderLine, width = 0)
            self.canvas.itemconfig(self.canvasSheepsUnderLine, width = 5)

    def GetFoxControllerType(self):
        if(self.foxControllerComboBox):
            for type in Entities.ControllerType:
                if(type.name == self.foxControllerComboBox.get()):
                    return type

    def GetSheepControllerType(self):
        if(self.sheepsControllerComboBox):
            for type in Entities.ControllerType:
                if(type.name == self.sheepsControllerComboBox.get()):
                    return type

    def GetFoxStrategy(self):
        if(self.foxStrategiesComboBox):
            for strategy in Entities.Strategy:
                if(self.foxStrategiesComboBox.get() == strategy.name):
                    return strategy

    def GetSheepsStrategy(self):
        if(self.sheepsStrategiesComboBox):
            for strategy in Entities.Strategy:
                if(self.sheepsStrategiesComboBox.get() == strategy.name):
                    return strategy

    def GetFoxDepth(self):
        if(self.foxDepthEntry):
            try:
                depth = int(self.foxDepthEntry.get())
                if(depth < 1):
                    depth = 1
                return depth
            except:
                return None

    def GetFoxROA(self):
        if(self.foxROAEntry):
            try:
                roa = int(self.foxROAEntry.get())
                if(roa < 1):
                    roa = 1
                return roa
            except:
                return None

    def GetFoxDOA(self):
        if(self.foxDOAEntry):
            try:
                doa = int(self.foxDOAEntry.get())
                if(doa < 1):
                    doa = 1
                return doa
            except:
                return None

    def GetSheepsROA(self):
        if(self.sheepsROAEntry):
            try:
                roa = int(self.sheepsROAEntry.get())
                if(roa < 1):
                    roa = 1
                return roa
            except:
                return None

    def GetSheepsDOA(self):
        if(self.sheepsDOAEntry):
            try:
                doa = int(self.sheepsDOAEntry.get())
                if(doa < 1):
                    doa = 1
                return doa
            except:
                return None


    def GetSheepsDepth(self):
        if(self.sheepsDepthEntry):
            try:
                depth = int(self.sheepsDepthEntry.get())
                if(depth < 1):
                    depth = 1
                return depth
            except:
                return None

    def GetFoxName(self):
        if(self.foxNameEntry):
            return self.foxNameEntry.get()

    def GetSheepsName(self):
        if(self.sheepsNameEntry):
            return self.sheepsNameEntry.get()

    def GetTurn(self):
        if(self.turnRadioVar.get() == 1):
            # Equal to Fox turn
            return Entities.Turn.Fox
        if(self.turnRadioVar.get() == 2):
            # Equal to Sheeps turn
            return Entities.Turn.Sheeps

    def GetMaxMoves(self):
        if(self.maxMoveCountEntry):
            try:
                return int(self.maxMoveCountEntry.get())
            except:
                return None

    def GetTime(self):
        if(self.turnTimeEntry):
            try:
                return int(self.turnTimeEntry.get())
            except:
                return None


def PosToTag(pos):
    return str(pos[0]) +','+ str(pos[1])