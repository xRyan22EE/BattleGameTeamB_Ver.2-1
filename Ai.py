import random
from time import sleep

import pygame


class ai_thinking():
    def __init__(self,grid_size, ai_values, player1_values):
        self.last = pygame.time.get_ticks()
        self.cooldown = 10
        self.grid_size = grid_size
        self.ai_values = ai_values
        self.player1_values = player1_values

    def fire(self):
        # fire gun, only if cooldown has been 2 seconds since last
        now = pygame.time.get_ticks()
        if now - self.last >= self.cooldown:
            self.last = now
            return ai_level1(self.grid_size, self.ai_values, self.player1_values)

def ai_level1(grid_size, ai_values, player1_values):
    xCooForShots = random.randrange(grid_size)
    yCooForShots = random.randrange(grid_size)
    while (xCooForShots, yCooForShots) in ai_values['shots_taken']:
        xCooForShots = random.randrange(grid_size)
        yCooForShots = random.randrange(grid_size)
    else:
        ai_values['shots_taken'].append((xCooForShots, yCooForShots))
    
    return xCooForShots, yCooForShots , ai_values

def ai_level2(grid_size, ai_values, player1_values):

    # ai_values['unknown_cells'] = []
    # for i in range(grid_size):
    #     ai_values['unknown_cells'].append(['..' for j in range(grid_size)])

    # Set opponent values
    player_grid = player1_values['player1Grid']
    xCooForShots, yCooForShots = player1_values['last_hit']
    first_hit = ai_values['first_hit']

    print('------------------------------------------')
    print(xCooForShots, yCooForShots)
    print(ai_values['shots_taken'])

    print(player_grid[xCooForShots][yCooForShots])

    print(player1_values['last_hit'])
    print(ai_values['last_hit'])


    last_hit = ''

    try:
        # Search if last try is a hit
        if player_grid[xCooForShots][yCooForShots] == 'H':
            print("enter")
            # make the next shot adjacent to the last shot
            # if last hit is right, continue to hit the right cell
            if ai_values['last_hit'] == 'right':
                # Reset possibilities
                possibly_hits = []
                possibly_hits.append((xCooForShots + 1, yCooForShots))
                last_hit = 'right'
                ai_values['last_hit'] = last_hit
                first_hit = False

            # if last hit is right, continue to hit the right cell
            elif ai_values['last_hit'] == 'left':
                # Reset possibilities
                possibly_hits = []
                possibly_hits.append((xCooForShots - 1, yCooForShots))
                last_hit = 'left'
                ai_values['last_hit'] = last_hit
                first_hit = False

            # if last hit is right, continue to hit the right cell
            elif ai_values['last_hit'] == 'down':
                # Reset possibilities
                possibly_hits = []
                possibly_hits.append((xCooForShots, yCooForShots - 1))
                last_hit = 'down'
                ai_values['last_hit'] = last_hit
                first_hit = False

            # if last hit is right, continue to hit the right cell
            elif ai_values['last_hit'] == 'up':
                # Reset possibilities
                possibly_hits = []
                possibly_hits.append((xCooForShots, yCooForShots + 1))
                last_hit = 'up'
                ai_values['last_hit'] = last_hit
                first_hit = False

            # if it's a new hit, try all sides
            else:
                # Reset possibilities
                possibly_hits = []
                print("don't know the previous hit")
                possibly_hits.append((xCooForShots + 1, yCooForShots))
                possibly_hits.append((xCooForShots - 1, yCooForShots))
                possibly_hits.append((xCooForShots, yCooForShots - 1))
                possibly_hits.append((xCooForShots, yCooForShots + 1))

                ai_values['last_hit'] = last_hit

                first_hit = True

            # search if adjacent is not taken
            if not first_hit:
                for hit in possibly_hits:
                    print(hit)
                    if hit not in ai_values['shots_taken']:
                        if (hit[0], hit[1]) == (xCooForShots + 1, yCooForShots):
                            last_hit = 'right'
                            ai_values['last_hit'] = last_hit
                            if 0 <= hit[0] < 10 and 0 <= hit[1] < 10:
                                xCooForShots, yCooForShots = hit[0], hit[1]

                        elif (hit[0], hit[1]) == (xCooForShots - 1, yCooForShots):
                            last_hit = 'left'
                            ai_values['last_hit'] = last_hit
                            if 0 <= hit[0] < 10 and 0 <= hit[1] < 10:
                                xCooForShots, yCooForShots = hit[0], hit[1]

                        elif (hit[0], hit[1]) == (xCooForShots, yCooForShots - 1):
                            last_hit = 'down'
                            ai_values['last_hit'] = last_hit
                            if 0 <= hit[0] < 10 and 0 <= hit[1] < 10:
                                xCooForShots, yCooForShots = hit[0], hit[1]

                        elif (hit[0], hit[1]) == (xCooForShots, yCooForShots + 1):
                            last_hit = 'up'
                            ai_values['last_hit'] = last_hit
                            if 0 <= hit[0] < 10 and 0 <= hit[1] < 10:
                                xCooForShots, yCooForShots = hit[0], hit[1]

            else:
                if ai_values['tries'] <= 4 :
                    hit = (possibly_hits[ai_values['tries']][0], possibly_hits[ai_values['tries']][1])
                    if hit not in ai_values['shots_taken']:
                        if 0 <= hit[0] < 10 and 0 <= hit[1] < 10:
                            yCooForShots, xCooForShots = hit[0], hit[1]
                        print(xCooForShots, yCooForShots)
                    ai_values['tries'] += 1
                else:
                    ai_values['tries'] = 0



        else:  # if not hit, continue searching
            print("in")
            print(xCooForShots, yCooForShots, 'before')
            xCooForShots = random.randrange(grid_size)
            yCooForShots = random.randrange(grid_size)
            while (xCooForShots, yCooForShots) in ai_values['shots_taken']:
                xCooForShots = random.randrange(grid_size)
                yCooForShots = random.randrange(grid_size)
            else:
                ai_values['shots_taken'].append((xCooForShots, yCooForShots))
            print(xCooForShots, yCooForShots, 'after')
    except:
        pass
    print('------------------------------------------')
    print(ai_values)
    print('------------------------------------------')
    return xCooForShots, yCooForShots, ai_values
