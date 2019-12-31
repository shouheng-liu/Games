# Author:  Shouheng Liu
#
# The Pac-Man Game
#
import turtle
import math
import random

# Setup the turtle window
turtle.setup(800, 700)
turtle.title("Pac-Man")
turtle.bgcolor("black")

# Setup the turtle
turtle.speed(0)
turtle.up()
turtle.hideturtle()
turtle.tracer(False)

# Define the game timing (30 frames per second)
frame_time = 1000 // 30

# Define the maze information
maze_x       = -300
maze_y       = -270
maze_columns = 21
maze_rows    = 19

# Define the tile information
tile_size = 30

# Define the food information
food_size  = 10
food_count = 0

# Define the pacman information
pacman_size  = 30
pacman_speed = 6
pacman_x     = 0
pacman_y     = 0

# Define the ghost information
ghost_size    = 30
ghost_speed   = 6
ghost_start_x = 0
ghost_start_y = 0
ghosts        = []

# Create the variables for the pacman movement
current_move = ""   # This is the current movement
next_move = ""      # This is the next movement

# Maze of the game
#   + : wall
#   . : food
#   o : power food
#   P : starting position of pacman
#   G : starting position of ghosts
maze = [
    #012345678901234567890 - total 21 columns
    "+++ +++++++++++++ +++", # 0
    "+o.................o+", # 1
    "+.++++++++.++++++++.+", # 2
    "+.+o.............o+.+", # 3
    "+.+.++++..+..+....+.+", # 4
    "+.+.+o....+..+....+.+", # 5
    "+.+.++++..+..+....+.+", # 6
    "+.+...o+..+..+....+.+", # 7
    "+.+.++++..+..++++.+.+", # 8
    "+.+.......+.......+.+", # 9
    "+.+.+++++++++++++.+.+", # 10
    "+...................+", # 11
    "+++++.+.++ ++.+.+++++", # 12
    "     .+.+ G +.+.     ", # 13
    "+++++.+.+++++.+.+++++", # 14
    "+.........P.........+", # 15
    "+.+++.++++ ++++.+++.+", # 16
    "+o....+o.. ..o+....o+", # 17
    "+++ +++++++++++++ +++"  # 18 - total 19 rows
]

#
# Draw the maze
#
for col in range(maze_columns):
    for row in range(maze_rows):
        # Get the tile
        tile = maze[row][col]

        # Locate the tile and move to the tile position
        #
        # - Find the x, y position of the tile in the turtle window
        tile_x = maze_x + col * tile_size
        tile_y = maze_y + (maze_rows - row - 1) * tile_size

        # - Put the turtle to the tile position
        turtle.goto(tile_x, tile_y)
        
        # Draw the tiles according to the tile symbol
        #
        # - Draw the tiles for walls, food and power food
        if tile == "+":   # wall
            turtle.shape("square")
            turtle.shapesize(tile_size / 20, tile_size / 20)  # 1 denote 20 pixels
            turtle.color("blue", "black")
            turtle.stamp()
        elif tile == ".": # food
            turtle.color("yellow")
            turtle.dot(food_size / 2)

            food_count += 1
        elif tile == "o": # power food
            turtle.color("white")
            turtle.dot(food_size)

            food_count += 1
        # - Initialize the position of pacman
        elif tile == "P": # pacman
            pacman_x = tile_x
            pacman_y = tile_y
        elif tile == "G": # ghost
            ghost_start_x = tile_x
            ghost_start_y = tile_y


# Cheat mode
protect_mode = False
def toggle_protect():
    global protect_mode

    protect_mode = not protect_mode


# Score
score_heading = turtle.Turtle()
score_heading.hideturtle()
score_heading.up()
score_heading.pencolor("white")
score_heading.goto(-300, 300)
score_heading.write("Score:", font=("Arial", 15, "bold"))

score = 0

score_turtle = turtle.Turtle()
score_turtle.hideturtle()
score_turtle.up()
score_turtle.pencolor("white")

def write_score():
    score_turtle.clear()
    score_turtle.goto(-220, 300)
    score_turtle.write(score, font=("Arial", 15, "normal"))

# Initialise
write_score()

#------------------------------------------------------------------------------------
# Drawing the pacman
pacman_mouth_max    = 80
pacman_mouth_open   = pacman_mouth_max
pacman_mouth_change = 8
pacman_heading_dir  = 0
pacman_radius       = pacman_size / 2

def draw_pacman():
    global pacman_mouth_open, pacman_mouth_change

    pacman.clear()
    pacman.up()

    # Draw the pacman with mouth
    pacman.setheading(pacman_heading_dir + pacman_mouth_open / 2)

    pacman.down()
    if not protect_mode:
        pacman.color("yellow")
    elif protect_mode:
        pacman.color("green")
    pacman.begin_fill()

    pacman.forward(pacman_radius)
    pacman.left(90)
    pacman.circle(pacman_radius, 360 - pacman_mouth_open)
    pacman.left(90)
    pacman.forward(pacman_radius)
    pacman.right(180 - pacman_mouth_open)
    pacman.forward(pacman_radius)
    
    pacman.end_fill()

    # Update pacman_mouth_open angle
    if pacman_mouth_open >= pacman_mouth_max or pacman_mouth_open <= 0:
        pacman_mouth_change = -pacman_mouth_change

    pacman_mouth_open += pacman_mouth_change

    
# Drawing the ghost
ghost_radius      = ghost_size / 2
ghost_eye_size    = 12
ghost_pupil_size = ghost_eye_size / 2
ghost_eye_separation = 13

def draw_ghost_pupil(ghost, move):
    if move == "up":
        ghost.left(90)
        ghost.forward(ghost_pupil_size / 2)
    elif move == "down":
        ghost.right(90)
        ghost.forward(ghost_pupil_size / 2)
    elif move == "right":
        ghost.forward(ghost_pupil_size / 2)
    elif move == "left":
        ghost.left(180)
        ghost.forward(ghost_pupil_size / 2)
        
    ghost.dot(ghost_pupil_size, "blue")
    
    if move == "up":
        ghost.backward(ghost_pupil_size / 2)
        ghost.right(90)
    elif move == "down":
        ghost.backward(ghost_pupil_size / 2)
        ghost.left(90)
    elif move == "right":
        ghost.backward(ghost_pupil_size / 2)
    elif move == "left":
        ghost.backward(ghost_pupil_size / 2)
        ghost.right(180)
    

def draw_ghost(ghost, move):
    
    ghost.clear()

    # Draw ghost body
    ghost.dot(ghost_size)

    # Draw ghost eyes
    ghost.left(90)
    ghost.forward(2)
    ghost.right(90)
    ghost.forward(ghost_eye_separation / 2)
    ghost.dot(ghost_eye_size, "white")

    draw_ghost_pupil(ghost, move)
        
    ghost.backward(ghost_eye_separation)
    ghost.dot(ghost_eye_size, "white")

    draw_ghost_pupil(ghost, move)
        
    ghost.forward(ghost_eye_separation / 2)
    ghost.right(90)
    ghost.forward(2)
    ghost.left(90)
 
#------------------------------------------------------------------------------------

# Create the pacman turtle
#
# - Use turtle.Turtle() to make your pacman
pacman = turtle.Turtle()
pacman.hideturtle()
draw_pacman()


# Create 4 ghosts of different colors
for color in ["red", "pink", "cyan", "orange"]:
    
    # - Use turtle.Turtle() to make your ghost
    ghost = turtle.Turtle()
##    ghost_eyes = turtle.Turtle()
    
    ghost.color(color)
    
    # - Put your ghost at the starting position
    ghost.up()
    ghost.goto(ghost_start_x, ghost_start_y)
    ghosts.append({"turtle": ghost, "move": "left"})

    # Call up draw_ghost(ghost, "left")
    ghost.hideturtle() # hide the default turtle "arrow"
    draw_ghost(ghost, "left") # make the initial movement direction as e.g. "left"


# Handle the movement keys
#
# - Complete the up, down, left and right movement keys for the pacman

# Handle the "Up" key for moving up
def move_up():
    global next_move
    next_move = "up"
def move_down():
    global next_move
    next_move = "down"
def move_right():
    global next_move
    next_move = "right"
def move_left():
    global next_move
    next_move = "left"

# Set up the key press events
turtle.onkeypress(move_up, "Up")
turtle.onkeypress(move_down, "Down")
turtle.onkeypress(move_right, "Right")
turtle.onkeypress(move_left, "Left")
turtle.onkeypress(toggle_protect, "c")

# Need to use listen for key events to work
turtle.listen()

#------------------------------------------------------------------------------------

# This is the game main loop, which is mainly used to:
#
# - Determine the movement of pacman
# - Determine if pacman hits a wall or food

def game_loop():
    global current_move, next_move
    global pacman_x, pacman_y
    global food_count
    global pacman_heading_dir
    global score

    # Handle the pacman next move
    #
    # - Update the condition of the following if statement so that
    #   pacman can only move along the rows and columns of the maze
    if next_move != "":
        current_move = next_move
        next_move = ""

    if (pacman_x - maze_x) % tile_size == 0 and (pacman_y - maze_y) % tile_size == 0 and next_move != "":
        current_move = next_move
        next_move = ""

    # Find the pacman new position
    #
    # - Complete the down, left and right moves
    #   (the up move has been given to you)
    if current_move == "up":
        new_x = pacman_x
        new_y = pacman_y + pacman_speed
        pacman_heading_dir = 90
    elif current_move == "down":
        new_x = pacman_x
        new_y = pacman_y - pacman_speed
        pacman_heading_dir = 270
    elif current_move == "right":
        new_x = pacman_x + pacman_speed
        new_y = pacman_y
        pacman_heading_dir = 0
    elif current_move == "left":
        new_x = pacman_x - pacman_speed
        new_y = pacman_y
        pacman_heading_dir = 180
    else:
        new_x = pacman_x
        new_y = pacman_y

    # new_x, new_y now contains the intended position the pacman wants to goto,
    # BUT not taken effect yet (until it pass the collision test)

    # Tunneling
    # Pacman going out of the left, right border
    if new_x < maze_x:  # Left border
        new_x = maze_x + (maze_columns - 1) * tile_size
    elif new_x > (maze_x + (maze_columns - 1) * tile_size): # Right border
        new_x = maze_x

    # Handle going out of top, bottom gameboard
    if new_y < maze_y:  # Bottom border
        new_y = maze_y + (maze_rows - 1) * tile_size
    elif new_y > (maze_y + (maze_rows - 1) * tile_size): # Top border
        new_y = maze_y

    #
    # Handle the collision of pacman, food and walls
    #
    for i in range(maze_columns):
        for j in range(maze_rows):
            # Get the tile
            tile = maze[j][i]

            # Locate the tile and calculate the distance
            #
            # - Find the x, y position of the tile in the turtle window
            tile_x = maze_x + i * tile_size
            tile_y = maze_y + (maze_rows - j - 1) * tile_size
            # - Find the distance between pacman and the tile in dx, dy
            dx = math.fabs(new_x - tile_x)
            dy = math.fabs(new_y - tile_y)


            # Collision detection
            #
            # - If pacman collides with any wall, stop pacman from moving
            # reset the new_x, new_y back to the current pacman position
            if dx < (pacman_size + tile_size) / 2 and dy < (pacman_size + tile_size) / 2 and tile == "+":
                new_x = pacman_x
                new_y = pacman_y
                break
            
            # - If pacman collides with any food, eat the food (remove the food)
            elif dx < (pacman_size + food_size) / 2 and dy < (pacman_size + food_size) / 2 and tile == ".":
                turtle.goto(tile_x, tile_y)
                turtle.color("black")
                turtle.dot(food_size / 2 + 2)
                # rebuild the whole string in maze[j]
                maze[j] = maze[j][:i] + " " + maze[j][i+1:]
                food_count -= 1
                score += 1
                write_score()
                break
            
            elif dx < (pacman_size + food_size) / 2 and dy < (pacman_size + food_size) / 2 and tile == "o":
                turtle.goto(tile_x, tile_y)
                turtle.color("black")
                turtle.dot(food_size + 2)
                # rebuild the whole string in maze[j]
                maze[j] = maze[j][:i] + " " + maze[j][i+1:]
                food_count -= 1
                score += 5
                write_score()
                break


    # Move the pacman
    #
    # - Move pacman to the new position
    # - Update pacman_x and pacman_y
    pacman.goto(new_x, new_y)
    pacman_x = new_x
    pacman_y = new_y

    # Draw the pacman with new mouth opening angle
    draw_pacman()

    #---------------------------------------------------------------------------------

    # Move one ghost at a time
    for ghost_item in ghosts:
        ghost = ghost_item["turtle"]
        ghost_move = ghost_item["move"]

        ghost_x = ghost.xcor()
        ghost_y = ghost.ycor()

        if (ghost_x - maze_x) % tile_size == 0 and (ghost_y - maze_y) % tile_size == 0:
            # Given the ghost x, y it returns the i (col), j (row)
            i = int((ghost_x - maze_x) / tile_size)
            j = (maze_rows - 1) - int((ghost_y - maze_y) / tile_size)

            moves = [] # A list to store the valid moving direction for the ghost

            # Check the content of the surrounding 4 tiles
            if j > 0 and maze[j - 1][i] != "+":
                moves.append("up")
            if j < (maze_rows - 1) and maze[j + 1][i] != "+":
                moves.append("down")
            if i < (maze_columns - 1) and maze[j][i + 1] != "+":
                moves.append("right")
            if i > 0 and maze[j][i - 1] != "+":
                moves.append("left")

            # Avoid turning around
            if len(moves) > 1:
                
                if ghost_move == "up" and "down" in moves:
                    moves.remove("down")
                if ghost_move == "down" and "up" in moves:
                    moves.remove("up")
                if ghost_move == "right" and "left" in moves:
                    moves.remove("left")
                if ghost_move == "left" and "right" in moves:
                    moves.remove("right")

            ghost_item["move"] = random.choice(moves)
            ghost_move = ghost_item["move"]
            
        # Process the ghost movement
        if ghost_move == "up":
            ghost_x = ghost_x
            ghost_y = ghost_y + ghost_speed
        elif ghost_move == "down":
            ghost_x = ghost_x
            ghost_y = ghost_y - ghost_speed
        elif ghost_move == "right":
            ghost_x = ghost_x + ghost_speed
            ghost_y = ghost_y
        elif ghost_move == "left":
            ghost_x = ghost_x - ghost_speed
            ghost_y = ghost_y
        else:
            ghost_x = ghost_x
            ghost_y = ghost_y

        # - Move ghost to the new position
        # - Update ghost_x and ghost_y
        ghost.goto(ghost_x, ghost_y)

        # Draw the ghost
        draw_ghost(ghost, ghost_move)

    # Update the window content
    turtle.update()

    # Exit the above for loop, after processing the movement of ALL ghosts

    #-------------------------------------------------------------------------------

    # If not protect_mode: process collision
    if not protect_mode:
        # Collision checking between pacman and any ghosts
        for ghost_item in ghosts:
            ghost      = ghost_item["turtle"]
            ghost_move = ghost_item["move"]
            ghost_x    = ghost.xcor()
            ghost_y    = ghost.ycor()

            # Find dx, dy between pacman and ghost
            dx = math.fabs(pacman_x - ghost_x)
            dy = math.fabs(pacman_y - ghost_y)

            # Game over message
            if dx < (pacman_size + ghost_size) / 2 and dy < (pacman_size + ghost_size) / 2:
                turtle.goto(0, -20)
                turtle.color("red")
                turtle.write("Game over!", font=("Arial", 50, "bold"), align="center")
                return # Exit the game

    # Eat all of the food, you win message
    #
    if food_count == 0:
        turtle.goto(0, -20)
        turtle.color("white")
        turtle.write("You win!", font=("Arial", 50, "bold"), align="center")
        return # Exit the game

    # Keep on running the game loop
    turtle.ontimer(game_loop, frame_time)

#------------------------------------------------------------------------------------

# Start the game loop
game_loop()

turtle.done()
