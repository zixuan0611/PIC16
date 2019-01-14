# import module Tkinter
import Tkinter as Tk

# define our class for the implementation details
class knights_tour_game:
    # initializations
    def __init__(self, master, n):
        self.master = master
        self.canvas = Tk.Canvas(master, width=n*50, height=n*50)
        # draw all the grids white
        for i in range(n):
            for j in range(n):
                self.canvas.create_rectangle(i*50, j*50, (i+1)*50, (j+1)*50, fill="white")
        self.canvas.pack()
        # make the upper left corner be the initial position as required
        self.canvas.create_rectangle(0, 0, 50, 50, fill="orange")
        self.clicked = [[0, 0]]  # a 2D list to store our clicked positions
        self.canvas.bind("<Button-1>", self.rectangle)

    def board(self):
        # to mark all the clicked positions blue
        for i in range(len(self.clicked)):
            self.canvas.create_rectangle(self.clicked[i][0]*50, self.clicked[i][1]*50,
                                         (self.clicked[i][0]+1)*50, (self.clicked[i][1]+1)*50, fill="blue")

    def rectangle(self, event):
        self.board()
        # extract the last position
        l_x = self.clicked[-1][0]
        l_y = self.clicked[-1][1]
        x = event.x / 50
        y = event.y / 50
        # check if the move is valid from the last position
        # if valid, mark the current position orange and append the new clicked position
        # if not valid, mark the last position orange and continue our game
        if ((x == l_x + 2 or x == l_x - 2) and (y == l_y - 1 or y == l_y + 1)) or (
                (x == l_x + 1 or x == l_x - 1) and (y == l_y - 2 or y == l_y + 2)):
            self.canvas.create_rectangle(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill="orange")
            self.clicked.append([x, y])
        else:
            self.canvas.create_rectangle(l_x * 50, l_y * 50, (l_x + 1) * 50, (l_y + 1) * 50, fill="orange")
            print ("invalid move!")

# a function to land our game
# can take a variable n, representing n * n knight's tour game
def knights_tour(n):
    root = Tk.Tk()
    knights_tour_game(root, n)
    root.mainloop()


# add our main to make it convenient to play the game
if __name__ == "__main__":
    knights_tour(5)
