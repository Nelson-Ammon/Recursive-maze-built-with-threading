"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: Ammon Nelson
Purpose: Part 2 of assignment 09, finding the end position in the maze
Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included
- Each thread requires a different color by calling get_color()
This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.
What would be your strategy?  
Pass in the path to the first thread and then when smaller threads are spawned then that path is passed to the child threads.
That path will get passed to all the kids and the one thread that makes it to the end would be the path that we could pass back
for the final path that we use.
Why would it work?
It would work because the entire path is passed to each child and is then just added on. Although it could be quite expensive to use.
But it should work.


"""
import math
import sys
import threading 
from screen import Screen
from maze import Maze

import cv2

# Include cse 251 common Python files - Dont change
from cse251 import *
set_working_directory(__file__)

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color

def thread_move(pos, color, maze, maze_lock):
    with maze_lock: # with lock, Write to the maze.
        if maze.can_move_here(pos[0], pos[1]):
            maze.move(pos[0], pos[1], color)
            return True
        return False

def thread_solve(pos, color, maze, maze_lock, thread_list):
    global stop
    if stop or not thread_move(pos, color, maze, maze_lock): # if stop then stop.
        return
    if maze.at_end(pos[0], pos[1]): # found the end
        stop = True
        return
    while True:
        moves = maze.get_possible_moves(pos[0], pos[1]) # Get possible moves
        first_move = True
        for move in moves: # for every move 
            if first_move:  # If we can take this first move, take it.
                if stop:
                    return
                can_move = thread_move(move, color, maze, maze_lock) 
                if can_move:
                    pos = move
                    first_move = False
                    if maze.at_end(pos[0], pos[1]): # if at the end then signal all the others 
                        stop = True
                        return
            else:
                thread = threading.Thread(target = thread_solve, args=(move, get_color(), maze, maze_lock, thread_list))
                thread.start()
                thread_list.append(thread)
        # It went through without making any moves.
        if first_move:
            return

def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """
    global stop
    stop = False # When one of the threads finds the end position, stop all of them
    
    maze_lock = threading.Lock()
    
    thread_list = []
    thread = threading.Thread(target = thread_solve, args=(maze.get_start_pos(), get_color(), maze, maze_lock, thread_list))
    
    thread.start()
    thread_list.append(thread)

    for thread in thread_list:
        thread.join()
    global thread_count 
    
    thread_count = len(thread_list)


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

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



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()