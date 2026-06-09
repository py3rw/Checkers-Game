from graphics import *
import random
import sys
import time

rank_letter = ["a", "b", "c", "d", "e", "f", "g", "h"]
file = [1, 2, 3, 4, 5, 6, 7, 8]

def board(): # FOR TESTING
    positions = {}
    win = GraphWin("Checkers", 600, 600)

    win.setCoords(0,0,8,8) # tels the window that bottom left is 0,0 and top right is 8,8
    for row in range(8):
        for col in range(8):
            po1 = Point(col, row)
            po2 = Point(col + 1, row + 1) # adds one to the value of x and y
            square = Rectangle(po1, po2)
            square.draw(win)

            if (row + col) % 2 == 0: # tile checker pattern
                square.setFill("light blue")
                square.setOutline("light blue")
                positions[f"{(rank_letter[col])}{(file[row])}"] = square # gets the black square notations and adds to dict

            else:
                square.setFill("white")
                square.setOutline("white")
                positions[f"{str(rank_letter[col])}{str(file[row])}"] = square # gets the white square notations and adds to dict

    return win, positions

def notation_trainer(win, positions):

    answered = False # the question is not answer
    highscore = 0 # high score is 0

    while answered == False:
        print("")
        print(f"Highscore: {highscore}") # prints highscore
        letter = random.choice(rank_letter) # column
        number = random.choice(file) # row
        notation = letter + str(number) # chess notation

        if int(ord(letter) + number - 96) % 2 == 0: # checks if its white or black tile
            tile_color = "light blue"
        else:
            tile_color = "white"

        correct = positions[notation]
        right = False

        print("\033[1m" + notation + "\033[0m")

        p1 = correct.getP1()
        p2 = correct.getP2()

        last_square = None

        while right == False:
            click = win.getMouse()

            if click.getX() >= p1.getX() and click.getX() <= p2.getX() and click.getY() >= p1.getY() and click.getY() <= p2.getY():
                right = True
                highscore += 1

                correct.undraw()
                correct.setFill("Green")
                correct.setOutline("Green")
                correct.draw(win)
                time.sleep(0.5)
                correct.undraw()
                correct.setFill(tile_color)
                correct.setOutline(tile_color)
                correct.draw(win)

            else:
                print("Wrong Answer.")

                x = click.getX() # gets the last coordinates of the mouse during the click
                y = click.getY()

                for key in positions:
                    sq = positions[key]
                    p1 = sq.getP1()
                    p2 = sq.getP2()

                    if p1.getX() <= x <= p2.getX() and p1.getY() <= y <= p2.getY():

                        if last_square != None:
                            last_square.setOutline("red")
                            last_square.setFill("red")

                        last_square = sq
                        sq.setOutline("Red")
                        sq.setFill("Red")

                correct.undraw()
                correct.setFill("Green")
                correct.setOutline("Green")
                correct.draw(win)
                time.sleep(0.5)

                over_msg = Text(Point(4,4),"Highscore: " + str(highscore))
                over_msg.setSize(30)
                over_msg.draw(win)

                print("")
                print(f"Highscore: {highscore}")
                time.sleep(1)
                sys.exit(0)

"""if __name__ == "__main__": # TEST
    try:
        win, positions = board()
        time.sleep(1)
        notation_trainer(win, positions)
    except GraphicsError:
        print("Graphics Error")
        sys.exit(0)"""