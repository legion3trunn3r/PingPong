from tkinter import *

import random
 

# screen settings
WIDTH = 900
HEIGHT = 300
 
# racket settings
 
# racket width
PAD_W = 10
# racket height
PAD_H = 100
 
# ball settings

# How much will the speed of the ball increase with each hit
BALL_SPEED_UP = 1.05

# Max Ball Speed
BALL_MAX_SPEED = 40

# ball radius
BALL_RADIUS = 30

INITIAL_SPEED = 20
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED

# Player Score
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

# Adding a global variable responsible for the distance
# to the right edge of the playing field
right_line_distance = WIDTH - PAD_W

def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == "right":
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)
 
def spawn_ball():
    global BALL_X_SPEED
    # Place the ball in the center
    c.coords(BALL, WIDTH/2-BALL_RADIUS/2,
             HEIGHT/2-BALL_RADIUS/2,
             WIDTH/2+BALL_RADIUS/2,
             HEIGHT/2+BALL_RADIUS/2)
    
    # Setting the ball in the direction of the losing player,
    # but reduce the speed to the original
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED) / abs(BALL_X_SPEED)

# ball bounce function
def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    # hit with a racket
    if action == "strike":
        BALL_Y_SPEED = random.randrange(-10, 10)

        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP

        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED

# installing a window
root = Tk()
root.title("Ping pong by Legion")
 
# animation area
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#003300")
c.pack()
 
# playing field elements
 
# left line
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")

# right line
c.create_line(WIDTH-PAD_W, 0, WIDTH-PAD_W, HEIGHT, fill="white")

# center line
c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="white")
 
# installation of game objects
 
# create a ball
BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2,
                     HEIGHT/2-BALL_RADIUS/2,
                     WIDTH/2+BALL_RADIUS/2,
                     HEIGHT/2+BALL_RADIUS/2, fill="white"
                    )
 
# left racket
LEFT_PAD = c.create_line(PAD_W/2, 0, PAD_W/2, PAD_H, width=PAD_W, fill="yellow")
 
# right racket
RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2, 
                          PAD_H, width=PAD_W, fill="yellow"
                        )


p_1_text = c.create_text(WIDTH-WIDTH/6, PAD_H/4,
                         text=PLAYER_1_SCORE,
                         font="Arial 20",
                         fill="white"
                        )
 
p_2_text = c.create_text(WIDTH/6, PAD_H/4,
                          text=PLAYER_2_SCORE,
                          font="Arial 20",
                          fill="white"
                        )

# adding global variables for the speed of the ball

# horizontally
BALL_X_CHANGE = 20

# vertically
BALL_Y_CHANGE = 0
 
def move_ball():
    # determine the coordinates of the sides of the ball and its center
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2
 
    # vertical bounce

    # If we are far from the vertical lines, we simply move the ball
    if ball_right + BALL_X_SPEED < right_line_distance and \
            ball_left + BALL_X_SPEED > PAD_W:
        
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)

    # If the ball touches its right or left side of the field boundary
    elif ball_right == right_line_distance or ball_left == PAD_W:

        # Check the right or left side we touch
        if ball_right > WIDTH / 2:
            # If it is right, then we compare the position of the center of the ball
            # with the position of the right racket.
            # And if the ball is within the racket we bounce
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                bounce("strike")

            else:
                # Otherwise, the player missed - here we will leave pass for now, we will replace it 
                # with scoring and respawning the ball

                update_score("left")
                spawn_ball()
        else:
            # Same for left player
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                bounce("strike")

            else:
                update_score("right")
                spawn_ball()

    # Checking a situation in which the ball can fly out of the playing field.
    # In this case, we simply move it to the field boundary.
    else:

        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance-ball_right, BALL_Y_SPEED)

        else:
            c.move(BALL, -ball_left+PAD_W, BALL_Y_SPEED)

    # horizontal bounce
    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce("ricochet")

# let's set global variables for the speed of movement of the rackets
# the speed at which the rackets will travel
PAD_SPEED = 20

# left platform speed
LEFT_PAD_SPEED = 0

# right platform speed
RIGHT_PAD_SPEED = 0
 
# movement function of both rackets
def move_pads():
    # for convenience, we will create a dictionary where the racket corresponds to its speed
    PADS = {LEFT_PAD: LEFT_PAD_SPEED, 
            RIGHT_PAD: RIGHT_PAD_SPEED}
    # перебираем ракетки
    for pad in PADS:
        # move the racket at a given speed
        c.move(pad, 0, PADS[pad])
        # If the racket goes off the playing field, return it to its place
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])

def main():
    move_ball()
    move_pads()
    # call yourself a nurse for 30 milliseconds
    root.after(30, main)

# Setting the focus to the Canvas so it responds to keypresses
c.focus_set()
 
# Writing a keypress processing function
def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    
    if event.keysym == "w":
        LEFT_PAD_SPEED = -PAD_SPEED

    elif event.keysym == "s":
        LEFT_PAD_SPEED = PAD_SPEED

    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED

    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED
 
# Binding this function to Canvas
c.bind("<KeyPress>", movement_handler)
 
# Creating a function to respond to key release
def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED

    if event.keysym in "ws":
        LEFT_PAD_SPEED = 0

    elif event.keysym in ("Up", "Down"):
        RIGHT_PAD_SPEED = 0
 
# Binding this function to Canvas
c.bind("<KeyRelease>", stop_pad)

# starting the movement
main()
 
# starting the window
root.mainloop()