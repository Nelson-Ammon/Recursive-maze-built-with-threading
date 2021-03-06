"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p1.py 
Author: Ammon Nelson

Purpose: Part 1 of assignment 09, finding a path to the end position in a maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included
"""


from screen import Screen
from maze import Maze
import cv2
import sys

# Include cse 251 common Python files - Dont change
from cse251 import *
set_working_directory(__file__)

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
FIN_COLOR = (0,255,0)

# TODO add any functions


def solve_path(maze):
    """ Solve the maze and return the path found between the start and end positions.  
        The path is a list of positions, (x, y) """

    def moving():
        row,col = path[-1] # get curr pos
        poss = maze.get_possible_moves(row,col) # get moves

        for move in poss: # For move in possible move go down each path and find out if it leads to the end
            row,col = move
            maze.move(row,col,COLOR) # move 
            path.append(move) # append that move

            while True: # continue down the path until we reach the end OR dead end 
                if maze.at_end(row,col):# base case to find  the End
                    return False
                else:
                    poss = maze.get_possible_moves(row,col)
                    while poss == []: # WE have found a dead end. Go backwards until we get back to where we started loop
                        path.pop(-1)
                        maze.restore(row,col)
                        row,col = path[-1]
                        poss = maze.get_possible_moves(row,col)
                        if poss != []:
                            return False, moving() # once we get back. Call the function again and try the next possible move
                    else:
                        row,col = poss[0] # keep moving through until we reach our goal
                        maze.move(row,col,COLOR)
                        path.append(poss[0])
                        
    path = [maze.get_start_pos()]
    row,col = path[-1]
    maze.move(row,col,COLOR)
    # This gets starting POSITION ^^^
    moving()

    return path


def get_path(log, filename):
    """ Do not change this function """

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)
    path = solve_path(maze)

    log.write(f'Number of drawing commands for = {screen.get_command_count()}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True

    return path


def find_paths(log):
    """ Do not change this function """

    files = ('verysmall.bmp', 'verysmall-loops.bmp', 
            'small.bmp', 'small-loops.bmp', 
            'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    log.write('*' * 40)
    log.write('Part 1')
    for filename in files:
        log.write()
        log.write(f'File: {filename}')
        path = get_path(log, filename)
        log.write(f'Found path has length          = {len(path)}')
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_paths(log)


if __name__ == "__main__":
    main()