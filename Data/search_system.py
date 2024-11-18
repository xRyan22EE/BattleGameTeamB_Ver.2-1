def search_hit(yCooForShots, xCooForShots, player1_values, player2_values, game_over):
    # Check for valid input
    valid_input = True
    # Check for a sunken ship
    sunken_ship = False
    sunkenList = []

    # get players current values
    player1Grid = player1_values['player1Grid']
    player1_reference = player1_values['player1_reference']
    player1_fleet = player1_values['player1_fleet']
    player1Turn = player1_values['player1Turn']

    player2Grid = player2_values['player2Grid']
    player2_reference = player2_values['player2_reference']
    player2_fleet = player2_values['player2_fleet']
    player2Turn = player2_values['player2Turn']

    # Based on last turn, switch the current player and opponent
    CurrentPlayer = (player1Grid, player1_fleet, player1_reference) if player1Turn else (player2Grid, player2_fleet, player2_reference)
    CurrentOpponent = (player2Grid, player2_fleet, player2_reference) if player1Turn else (player1Grid, player1_fleet, player1_reference)

    # check game stats by looking for sunken ships
    def game_stats():
        nonlocal game_over
        ships_sunken = 0
        for ship in CurrentOpponent[1].keys():
            if CurrentOpponent[1][ship] == 0:
                ships_sunken += 1
        if ships_sunken == 7:
            game_over = True
        else:
            game_over = False

    if not game_over:
        # if shot is not a miss or empty
        if CurrentOpponent[0][yCooForShots][xCooForShots] != 'M' and CurrentOpponent[0][yCooForShots][xCooForShots] != 'H' and CurrentOpponent[0][yCooForShots][xCooForShots] != 'S':
            if CurrentOpponent[0][yCooForShots][xCooForShots] != '..':
                # get ship's name
                shipId = CurrentOpponent[0][yCooForShots][xCooForShots]
                # validate that shipId exists in the current opponent's fleet
                if str(shipId) in CurrentOpponent[1].keys():
                    # subtract one from the ship's health
                    CurrentOpponent[1][shipId] -= 1
                    # if ship's health is 0
                    if CurrentOpponent[1][shipId] == 0:
                        # create temp list to store ship's position
                        sunkenList = []
                        # iterate reference grid to find ship's position
                        for i, row in enumerate(CurrentOpponent[2]):
                            for j, cell in enumerate(row):
                                if cell == shipId:
                                    sunkenList.append((i, j))
                        # change sunken ship to 'S'
                        for i in range(len(sunkenList)):
                            CurrentOpponent[0][sunkenList[i][0]][sunkenList[i][1]] = 'S'
                        sunken_ship = True
                    # change ship's hit to 'H'
                    else:
                        CurrentOpponent[0][yCooForShots][xCooForShots] = 'H'
            # change empty to miss 'M'
            elif CurrentOpponent[0][yCooForShots][xCooForShots] == '..':
                CurrentOpponent[0][yCooForShots][xCooForShots] = 'M'

            player1_values['player1Turn'] = not player1Turn
            player2_values['player2Turn'] = not player2Turn
        else:
            game_stats()
            if not game_over:
                valid_input = False
                player1_values['player1Turn'] =  player1Turn
                player2_values['player2Turn'] =  player2Turn
    game_stats()

    # update players values
    if player1Turn:
        player1Grid, player1_fleet, player1_reference = CurrentPlayer
        player2Grid, player2_fleet, player2_reference= CurrentOpponent
    else:
        player2Grid, player2_fleet, player2_reference = CurrentPlayer
        player1Grid, player1_fleet, player1_reference = CurrentOpponent

    player1_values['player1Grid'] = player1Grid
    player1_values['player1_reference'] = player1_reference
    player1_values['player1_fleet'] = player1_fleet

    player2_values['player2Grid'] = player2Grid
    player2_values['player2_reference'] = player2_reference
    player2_values['player2_fleet'] = player2_fleet
    return (valid_input, player1_values, player2_values, game_over)
