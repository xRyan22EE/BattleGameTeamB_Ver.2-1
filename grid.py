def CreateGameGrid(rows, cols, CellSize, pos):
    # create game grid with coordinate for each cell 
    
    # startx and starty are the starting position of the grid
    startx = pos[0]
    starty = pos[1]

    # create a list to hold the coordinate of each cell in the grid
    CoordGrid = []

    # loop through the rows and columns to create the grid
    for row in range(rows):
        # create a list to hold the coordinate of each cell in a row
        rowx = []

        # loop through the columns to create the cells in a row
        for col in range(cols):

            # add the coordinate of the cell to the row list
            rowx.append((startx, starty))

            # move to the next cell in the row
            startx += CellSize

        # add the row list to the grid list and move to the next row in the grid 
        CoordGrid.append(rowx)
        # reset the starting position of the next row
        startx = pos[0]
        # move to the next column in the next row
        starty += CellSize

    # return the grid list with the coordinates of each cell in the grid
    return CoordGrid

def UpdateGameLogic(rows, cols):
    # create game logic grid with empty string for each cell
    game_logice = []
    # loop through the rows and columns to create the grid
    for row in range(rows):

        # create a list to hold the value of each cell in a row
        rowx = []

        # loop through the columns to create the cells in a row
        for col in range(cols):

            # add the value of the cell to the row list
            rowx.append(" ")

        # add the row list to the grid list and move to the next row in the grid
        game_logice.append(rowx)
        
    return game_logice
