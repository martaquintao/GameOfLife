from PIL import Image, ImageDraw
import numpy as np
import color_hues as ch
import math
import os
import datetime

outputs_folder = 'outputs'


class GameOfLife():

    def __init__(self, num_squares, x_size,y_size):
        """Creates a new GameOfLife instance """

        # Characteristics: board
        self.num_squares = num_squares
        self.x_size = x_size
        self.y_size = y_size
        self.square_size = float(x_size-50)/self.num_squares
        self.square_ynum = int(math.floor(y_size/self.square_size))
        self.square_xnum = self.num_squares
        self.xoffset = (x_size-self.square_xnum*float(self.square_size))/2
        self.yoffset = (y_size-self.square_ynum*float(self.square_size))/2

        # Initiate Board
        self.generation = 0

        # Other initial variables
        self.folder = ''


    def set_new_random_board(self,seed):
        """Reset current board to a new random state"""

        np.random.seed(seed)
        self.board = np.zeros((self.square_xnum, self.square_ynum), dtype=bool)
        rule = np.random.random((self.square_xnum, self.square_ynum))
        self.board[0:self.square_xnum][0:self.square_ynum] = (rule >= 0.80)



    def set_new_board(self,board):
        """Reset current board to a new input state"""

        self.board = np.zeros((self.square_xnum, self.square_ynum), dtype=bool)
        rule = np.array(board)
        self.board[0:self.square_xnum][0:self.square_ynum] = (rule > 0)


    def in_bounds(self,x,y):
        """Check to see if its a viable cell"""
        return True if ((0<=x<self.square_xnum) and (0<=y<self.square_ynum)) else False



    def live(self,x,y):
        """Activate cell"""
        if self.in_bounds(x,y):
            self.board[x,y] = True
        else:
            raise ValueError("Coordinates {} {} are not available. x values must be kept between 0..{} and y between "
                             "0.. {}".format(x,y,self.square_xnum,self.square_ynum))



    def kill(self,x,y):
        """Deactivate cell"""
        if self.in_bounds(x,y):
            self.board[x,y] = False
        else:
            raise ValueError("Coordinates {} {} are not available. x values must be kept between 0..{} and y between "
                             "0.. {}".format(x,y,self.square_xnum,self.square_ynum))



    def next_generation(self):
        """Apply Conway's Game of Life rules to create the next generation"""

        for j in xrange(self.square_ynum):
            for i in range(self.square_xnum):
                alive = self.board[i,j]
                subset = self.board[max(0,i-1):min(i+2,self.square_xnum),max(0,j-1):min(j+2,self.square_ynum)]

                # Any live cell with fewer than two live neighbours dies, as if caused by under-population.
                # Any live cell with two or three live neighbours lives on to the next generation.
                # Any live cell with more than three live neighbours dies, as if by over-population.
                # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

                count_neighbours = np.sum(subset) - alive
                if (count_neighbours == 2 and alive) or count_neighbours == 3:
                    self.live(i,j)
                elif alive:
                    self.kill(i,j)

        self.generation = +1



    def draw_board(self,background,hues,saturation,value):
        """Draw current board"""

        self.background = background
        self.hues = hues
        self.saturation = saturation
        self.value = value

        img = Image.new('RGB', (self.x_size, self.y_size), background)
        draw = ImageDraw.Draw(img)
        hue_name = ch.GetIterHues(hues)

        for j in xrange(self.square_ynum):
            for i in range(self.square_xnum):
                if self.board[i,j]:
                    coord = (i*self.square_size+self.xoffset, j*self.square_size+self.yoffset,
                             (i+1)*self.square_size+self.xoffset, (j+1)*self.square_size+self.yoffset)
                    color = ch.GetRandomSquareColor(hue_name,saturation,value)
                    draw.rectangle(coord, outline=background,fill=color)

        return img,hue_name



    def save_image(self,img,hue_name,generation):
        """Saves generations to a run folder"""

        if self.folder == '':
            current_directory = os.getcwd()

            # Check if outputs_folder exists
            outputs_path = os.path.join(current_directory, outputs_folder)
            if not os.path.exists(outputs_path):
                os.makedirs(outputs_path)

            # Check if the runtime folder was created
            now = datetime.datetime.now()
            self.folder = 'Images_' + str(now.year)         + str(now.month).zfill(2) + str(now.day).zfill(2)\
                          + '_'     + str(now.hour).zfill(2)+ str(now.minute).zfill(2)+ str(now.second).zfill(2)\
                          + '_squares_' + str(self.num_squares)

            folder_path = os.path.join(current_directory, outputs_folder, self.folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

        # Save image to folder
        img.save(outputs_folder + '/' + self.folder
                      +'/img_' + str(generation).zfill(4)+ '_' + hue_name
                      +'.png','PNG')




def main(num_squares=27, x_size=697, y_size=1039, background="white", hues='cycle', saturation='narrow_upper', value='upper', generations=1000, seed = 0):
    """Example for running the game of life and printing on a standard vertical business card size"""

    new_board = GameOfLife(num_squares,x_size,y_size)
    new_board.set_new_random_board(0)
    img,hue_name = new_board.draw_board(background,hues,saturation,value)
    new_board.save_image(img,hue_name,0)

    for x in xrange(generations):
        new_board.next_generation()


        img,hue_name = new_board.draw_board(background,hues,saturation,value)
        new_board.save_image(img,hue_name,x+1)
    img.show()


if __name__ == '__main__':
    main()