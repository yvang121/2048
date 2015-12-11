__author__ = 'Ye Vang && Evan Weiler'

import random
from tkinter import *
import tkinter.messagebox as mBox


class Block:
    '''Creates block objects with characteristics to manipulate'''
    def __init__(self, number, canvasID):
        '''Initializes a self object'''
        self.number = number
        self.canvasID = canvasID
        self.old = False

    def getNumber(self):
        '''Returns the number associated with the block'''
        return self.number

    def getID(self):
        '''Returns the canvas ID'''
        return self.canvasID

    def makeOld(self):
        '''Makes a newly created block, old, so that we can combine in the next move input'''
        self.old = True

    def isOld(self):
        '''Checks the status of the block'''
        return self.old


class gameGUI:
    '''Creates the game 2048 Game User Interface'''
    def __init__(self):
        '''This is where the game will be stored and its methods accessed'''
        self.mainWin = Tk()
        self.mainWin.title("Python 2048")
        self.mainWin.minsize(550, 550) # Creates a minimum window size
        self.canvas = Canvas(self.mainWin, bg = '#F5DEB3', width = 550, height = 550) # Canvas size taking into account the size of vertical and horizontal lines.

        self.mainWin.bind('<w>', self.move) # All the different key bindings available for the user to press
        self.mainWin.bind('<a>', self.move)
        self.mainWin.bind('<s>', self.move)
        self.mainWin.bind('<d>', self.move)
        self.mainWin.bind('<Up>', self.move)
        self.mainWin.bind('<Left>', self.move)
        self.mainWin.bind('<Down>', self.move)
        self.mainWin.bind('<Right>', self.move)
        self.mainWin.bind('<W>', self.move)
        self.mainWin.bind('<A>', self.move)
        self.mainWin.bind('<S>', self.move)
        self.mainWin.bind('<D>', self.move)
        self.mainWin.bind('<Enter>', self.windowCommand)
        self.mainWin.bind('<Return>', self.windowCommand)
        self.mainWin.bind('<Escape>', self.windowCommand)

        # All the buttons and labels for the game.
        self.instructionLabel = Label(self.mainWin, text = 'Press W, A, S, D or the arrow keys to move the tiles. \n The same numbers will merge to form a new tile. \n Try reaching 2048! \n Press Enter to start new game. Escape will close window.', pady = 10, padx = 5, font = 'Verdana 11', justify = CENTER, relief = GROOVE) # Provides instructions for the user to read
        self.scoreLabel = Label(self.mainWin, text = "Score:", padx = 10, justify = LEFT, font = 'Verdana 11')
        self.scoreNumber = Label(self.mainWin, text = "0", justify = LEFT, font = 'Verdana 11', padx = 10, relief = RIDGE) # Shows the score from all the combinations
        self.quitButton = Button(self.mainWin, text = 'Quit', command = self.quit, padx = 10, pady = 0, justify = LEFT, bg = '#FF3333', fg = 'black', font = 'Verdana 11', relief = RIDGE) # Provides a button to exit out of the window.
        self.newGameButton = Button(self.mainWin, text = 'New Game!', command = self.newGame, padx = 10, pady = 0, justify = LEFT, bg = '#EEE8AA', font = 'Verdana 11', relief = RIDGE) # Provides the option of a new game
        self.highScoreLabel = Label(self.mainWin, text = 'High Score:', font = 'Verdana 11', padx = 10)
        self.highScoreNumber = Label(self.mainWin, text = '0', font = 'Verdana 11', justify = CENTER, relief = RIDGE, padx = 10) # Shows the highest score the user achieved

        self.canvas.grid(row = 0, column = 0, columnspan = 2) # Placing widgets onto the grid
        self.instructionLabel.grid(row = 1, column = 0)
        self.quitButton.grid(row = 10, column = 1)
        self.newGameButton.grid(row = 10, column = 0)
        self.scoreLabel.grid(row = 2, column = 1)
        self.scoreNumber.grid(row = 3, column = 1)
        self.highScoreLabel.grid(row = 2, column = 0)
        self.highScoreNumber.grid(row = 3, column = 0)

        self.canvas.create_line(0, 5, 550, 5, fill = '#D2B48C', smooth = True, width = 10)
        self.canvas.create_line(0, 140, 550, 140, fill = '#D2B48C', smooth = True, width = 10)
        self.canvas.create_line(0, 275, 550, 275, fill = '#D2B48C', smooth = True, width = 10) # Create the lines to signify a grid
        self.canvas.create_line(0, 410, 550, 410, fill = '#D2B48C', smooth = True, width = 10)
        self.canvas.create_line(0, 545, 550, 545, fill = '#D2B48C', smooth = True, width = 10)
        self.canvas.create_line(5, 0, 5, 550, fill = '#D2B48C', smooth = True, width = 10)
        self.canvas.create_line(140, 0, 140, 550, fill = '#D2B48C', smooth = True, width = 10)
        self.canvas.create_line(275, 0, 275, 550, fill = '#D2B48C', smooth = True, width = 10)
        self.canvas.create_line(410, 0, 410, 550, fill = '#D2B48C', smooth = True, width = 10)
        self.canvas.create_line(545, 0, 545, 550, fill = '#D2B48C', smooth = True, width = 10)

        self.highScoreList = [] # Holds the scores the user achieved.

        self.imageDict = {2: PhotoImage(file = 'block/num_2.gif'), # Assigning number values to pictures so that pictures can be easily called
                     4: PhotoImage(file = 'block/num_4.gif'),
                     8: PhotoImage(file = 'block/num_8.gif'),
                     16: PhotoImage(file = 'block/num_16.gif'),
                     32: PhotoImage(file = 'block/num_32.gif'),
                     64: PhotoImage(file = 'block/num_64.gif'),
                     128: PhotoImage(file = 'block/num_128.gif'),
                     256: PhotoImage(file = 'block/num_256.gif'),
                     512: PhotoImage(file = 'block/num_512.gif'),
                     1024: PhotoImage(file = 'block/num_1024.gif'),
                     2048: PhotoImage(file = 'block/num_2048.gif')}
        self.grid = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]] # The 'behind-the-scenes' grid
        self.randomAnte()

    def newGame(self):
        '''Enables the game to restart by grabbing the entries that aren't None
        and deleting them. Also resets the score. Sends the score to a list. The
        list sorts these values and prints the highest value to high score box.'''
        for Column in range(4):
            for Row in range(4):
                if self.grid[Column][Row] != None:
                    self.canvas.delete(self.grid[Column][Row].getID())
                    self.grid[Column][Row] = None
        self.randomAnte()
        self.highScoreList.append(int(self.scoreNumber['text'])) # Writes the score into high score list
        self.highestScore = max(self.highScoreList)             # Identifies the maximum
        self.highScoreNumber['text'] = str(self.highestScore)  # Writes the maximum into high score label
        self.scoreNumber['text'] = '0'                        # Deletes the score by putting 0 there

    def anteBlock(self, Column, Row):
        '''This function places a block object with number 2 or 4 onto the canvas'''
        number = random.randint(1, 16) # Set these integers so that the number 2 has more chances of appearing.
        if number < 15:
            number = 2
        else:
            number = 4
        (self.canvasColumn, self.canvasRow) = self.generateCoords(Column, Row)
        self.grid[Column][Row] = Block(number, self.canvas.create_image(self.canvasColumn, self.canvasRow, image = self.imageDict[number], anchor = NW))

    def randomAnte(self):
        '''For the purpose of generating a value of either 2 or 4, onto random
        locations on the grid after newGame() is called'''
        numBlocks = 0
        while numBlocks < 2 and self.emptyCheck(): # While there are empty spaces, and while number of blocks is less than 2
            randColumn = random.randrange(4)      # Generate random Column and Row grid coordinates
            randRow = random.randrange(4)
            if self.grid[randColumn][randRow] == None:
                self.anteBlock(randColumn, randRow)
                numBlocks += 1

    def afterMove(self):
        '''This function is used specifcally for the purpose of placing a new ante on
        the grid after the user inputs a keyboard command'''
        numBlocks = 0
        while numBlocks < 1 and self.emptyCheck():
            randColumn = random.randrange(4)
            randRow = random.randrange(4)
            if self.grid[randColumn][randRow] == None:
                self.anteBlock(randColumn, randRow)
                numBlocks += 1

    def emptyCheck(self):
        '''This function checks the grid for "None" in the grid'''
        for Column in range(4):
            for Row in range(4):
                if self.grid[Column][Row] == None:
                    return True
        return False

    def loseCheck(self):
        '''This function iterates through the grid and if the grid cannot do anymore
        combinations and is full, then print message box saying so.'''
        offSetList = [(-1, 0), (1, 0), (0, -1), (0, 1)] # The directions for each location in the grid
        if self.emptyCheck() == False:  # If the grid is full
            for Column in range(0, 4): # Iterate through the grid
                for Row in range(0, 4):
                    for offset in offSetList: # For each tuple in offSetList
                        (x, y) = offset # Get the Column and Row value
                        if Column + x < 0 or 3 < Column + x or Row + y < 0 or 3 < Row + y: # This constraint prevents the grid from going outside of it
                            continue # If it goes offgrid, then skip/continue on
                        if self.grid[Column][Row].getNumber() == self.grid[Column + x][Row + y].getNumber():
                            return False # If the grid's numbers are the same, which means they can combine, then return False
            return True # Return True if the grid number's aren't the same for each block
        return False    # If there are empty spaces, make it false


    def winCheck(self):
        '''This function checks to see if the 2048 tile has been achieved.
        If it has, display win message'''
        for Column in range(0, 4):
            for Row in range(0, 4):
                if self.grid[Column][Row] != None and self.grid[Column][Row].getNumber() == 2048:
                    self.win = mBox.showinfo("You won!", "Congratulations, you've achieved the 2048 tile! You win!")
                    print("Game status: ", self.win)

    def move(self, event):
        '''Moves the blocks on the grid in the direction of the input by user and also
        places a single ante onto the grid in a random location. If the block is
        moving into a block with a similar Number in its Block object then combine/merge
        them.'''
        if event.keysym == 'w' or event.keysym == 'W' or event.keysym == 'Up':
        # If any of the keys pressed are these, then move object in the upward direction
            movedTile = False
            for Column in range(0, 4):
                for Row in range(1, 4): # For rows 1, 2 and 3
                    if self.grid[Column][Row] != None:
                        for r in range(Row, 0, -1): # For the column up tile before 0
                            if self.grid[Column][r - 1] != None: # If the tile above is occupied
                                if self.grid[Column][r - 1].getNumber() == self.grid[Column][Row].getNumber(): # If the block numbers are the same
                                    self.canvas.delete(self.grid[Column][Row].getID()) # Delete block from projectile tile
                                    self.grid[Column][Row] = None # Reset the block from projectile tile to None
                                    self.canvas.delete(self.grid[Column][r - 1].getID()) # Deletes the block from target tile
                                    self.grid[Column][r - 1] = self.newBlock(self.grid[Column][r - 1].getNumber(), Column, r - 1) # Set the target tile to new block
                                    num = self.grid[Column][r - 1].getNumber()
                                    self.score(num)
                                    movedTile = True
                                else:
                                    (x, y) = self.generateCoords(Column, r) # Generate coordinates for the canvas for the tile below occupied tile
                                    self.canvas.coords(self.grid[Column][Row].getID(), x, y) # Move the block from (Column, Row) to the coordinate below occupied tile
                                    self.grid[Column][r] = self.grid[Column][Row] # Copy block into new location
                                    if r != Row:
                                        self.grid[Column][Row] = None #Erase block from old location
                                        movedTile = True
                                break
                            elif self.grid[Column][0] == None: # If top row is empty then move the block to the row, and delete its old spot.
                                (x, y) = self.generateCoords(Column, 0)
                                self.canvas.coords(self.grid[Column][Row].getID(), x, y)
                                self.grid[Column][0] = self.grid[Column][Row]
                                self.grid[Column][Row] = None
                                movedTile = True
                                break
            if movedTile:
                self.afterMove()
        elif event.keysym == 'a' or event.keysym == 'A' or event.keysym == 'Left': # Move objects in the left direction
            movedTile = False
            for Column in range(1, 4): # For columns 1, 2, and 3
                for Row in range(0, 4):
                    if self.grid[Column][Row] != None:
                        for r in range(Column, 0, -1): # For the row in left direction to tile before 0
                            if self.grid[r - 1][Row] != None: # If the column after 0 is occupied,
                                if self.grid[Column][Row].getNumber() == self.grid[r - 1][Row].getNumber(): # If the block numbers are the same
                                    '''If the block numbers are the same, combine them. Else, move them next to each other'''
                                    self.canvas.delete(self.grid[r - 1][Row].getID())  # Delete the target tile
                                    self.grid[r - 1][Row] = self.newBlock(self.grid[Column][Row].getNumber(), r - 1, Row) # Set target tile to newly combined block
                                    self.canvas.delete(self.grid[Column][Row].getID()) # Delete the projectile tile
                                    self.grid[Column][Row] = None # Reset the acquired block to None
                                    num = self.grid[r - 1][Row].getNumber()
                                    self.score(num)
                                    movedTile = True
                                else:
                                    (x, y) = self.generateCoords(r, Row) # Generate coordinates
                                    self.canvas.coords(self.grid[Column][Row].getID(), x, y)
                                    self.grid[r][Row] = self.grid[Column][Row]
                                    if r != Column:
                                        self.grid[Column][Row] = None # Erases block ID from old location in grid
                                        movedTile = True
                                break
                            elif self.grid[0][Row] == None:
                                (x, y) = self.generateCoords(0, Row)
                                self.canvas.coords(self.grid[Column][Row].getID(), x, y)
                                self.grid[0][Row] = self.grid[Column][Row]
                                self.grid[Column][Row] = None
                                movedTile = True
                                break
            if movedTile:
                self.afterMove()
        elif event.keysym == 'd' or event.keysym == 'D' or event.keysym == 'Right': # Move objects right
            movedTile = False
            for Column in range(2, -1, -1): # In columns 2, 1 and 0
                for Row in range(0, 4): # In rows 0, 1, 2 and 3
                    if self.grid[Column][Row] != None:
                        for r in range(Column, 3): # For all the columns to the right of existing tile
                            if self.grid[r + 1][Row] != None: # If the column after r is occupied,
                                if self.grid[Column][Row].getNumber() == self.grid[r + 1][Row].getNumber(): # If the block numbers are the same
                                    '''If the block numbers are the same, combine them. Else, move them next to each other'''
                                    self.canvas.delete(self.grid[r + 1][Row].getID())
                                    self.grid[r + 1][Row] = self.newBlock(self.grid[Column][Row].getNumber(), r + 1, Row) # Set target tile to newly combined block
                                    self.canvas.delete(self.grid[Column][Row].getID()) # Delete the projectile tile
                                    self.grid[Column][Row] = None # Reset the acquired block to None
                                    num = self.grid[r + 1][Row].getNumber()
                                    self.score(num)
                                    movedTile = True
                                else:
                                    (x, y) = self.generateCoords(r, Row) # Generate coordinates
                                    self.canvas.coords(self.grid[Column][Row].getID(), x, y)
                                    self.grid[r][Row] = self.grid[Column][Row]
                                    if r != Column: # If the r from line above are not equal to each other, delete old tile. We don't want to delete the ID if it's in correct place.
                                        self.grid[Column][Row] = None # Erases block ID from old location in grid
                                        movedTile = True
                                break
                            elif self.grid[3][Row] == None:
                                (x, y) = self.generateCoords(3, Row)
                                self.canvas.coords(self.grid[Column][Row].getID(), x, y)
                                self.grid[3][Row] = self.grid[Column][Row]
                                self.grid[Column][Row] = None
                                movedTile = True
                                break
            if movedTile:
                self.afterMove()
        elif event.keysym == 's' or event.keysym == 'S' or event.keysym == 'Down': # Move objects downward
            movedTile = False
            for Column in range(0, 4): # For columns 0, 1, 2 and 3
                for Row in range(2, -1, -1): # For rows 2, 1 and 0
                    if self.grid[Column][Row] != None:
                        for r in range(Row, 3):
                            if self.grid[Column][r + 1] != None:
                                if self.grid[Column][Row].getNumber() == self.grid[Column][r + 1].getNumber():
                                    self.canvas.delete(self.grid[Column][r + 1].getID())
                                    self.grid[Column][r + 1] = self.newBlock(self.grid[Column][Row].getNumber(), Column, r + 1)
                                    self.canvas.delete(self.grid[Column][Row].getID())
                                    self.grid[Column][Row] = None
                                    num = self.grid[Column][r + 1].getNumber()
                                    self.score(num)
                                    movedTile = True
                                else:
                                    (x, y) = self.generateCoords(Column, r)
                                    self.canvas.coords(self.grid[Column][Row].getID(), x, y)
                                    self.grid[Column][r] = self.grid[Column][Row]
                                    if r != Row:
                                        self.grid[Column][Row] = None
                                        movedTile = True
                                break
                            elif self.grid[Column][3] == None:
                                (x, y) = self.generateCoords(Column, 3)
                                self.canvas.coords(self.grid[Column][Row].getID(), x, y)
                                self.grid[Column][3] = self.grid[Column][Row]
                                self.grid[Column][Row] = None
                                movedTile = True
                                break
            if movedTile:
                self.afterMove()
        if self.loseCheck():
            self.lose = mBox.showerror("Game Over", "You've run out of available moves.")
            print("Game status: ", self.lose)
        self.makeBlocksOld() # Makes all the blocks old, releasing them to be able to form after the move
        self.winCheck() # Loops through the grid searching for the 2048 tile after each move input

    def score(self, number):
        '''Gets the value from the label, turns it into an integer, adds the number
        from the block with this value, then rewrites into the label the new score as a string.'''
        self.Score = int(self.scoreNumber['text']) + number
        self.scoreNumber['text'] = self.Score
        return self.Score

    def windowCommand(self, event):
        '''If Enter or Return are pressed, start a new game. If Escape is pressed,
        exit the window.'''
        if event.keysym == 'Enter' or event.keysym == 'Return':
            self.newGame()
        elif event.keysym == 'Escape':
            self.quit()

    def makeBlocksOld(self):
        '''This method makes a newly created block's status to old. All new
        blocks that are created are new'''
        for Column in range(0, 4):
            for Row in range(0, 4):
                if self.grid[Column][Row] != None:
                    self.grid[Column][Row].makeOld()

    def generateCoords(self, Column, Row):
        '''Generates the canvas coordinates given the grid coordinates.'''
        return (10 + 135*Column, 10 + 135*Row)

    def newBlock(self, Number, Column, Row):
        '''Takes in the number associated with the block object, multiplies it
        by 2 (add them), and accesses the dictionary using the new number as a key'''
        addBlocks = int(Number*2)
        (x, y) = self.generateCoords(Column, Row)
        return Block(addBlocks, self.canvas.create_image(x, y, image = self.imageDict[addBlocks], anchor = NW))

    def quit(self):
        self.mainWin.destroy()

    def startGUI(self):
        self.mainWin.mainloop()

gameGUI().startGUI()