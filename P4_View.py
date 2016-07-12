"""
P4_View.py. CIS 211 Spring 2016 Project 4 Final. 2016-05-28.
Author: Joel Berry. Modified Anthony Hornof's solution code for this module.
Credits: Project spec, starter code by Anthony Hornof, 2016-04-08.

Basic Model-View-Controller fire-fighting simulation.
"""

from P4_Utility import *

class View:
    '''
    The View object receives updates from the Model and presents the User with
    a graphical representation of the data in the Model.
    '''

    def __init__(self):
        # A list of all of the humans, robots, and fires in the plot.
        self.__view_size = None
        self.__cells = []
        self.__num_rows = 0
        self.__num_cols = 0
        self.__objects = {}
        self.__landmarks = {}

    def create(self, world_size):
        self.__view_size = world_size
        self.__num_rows = self.__num_cols = world_size + 1
        # Create appropriate sized 2D grid using list comprehensions.
        self.__cells = [[[] for j in range(self.__num_cols)] for i in range(self.__num_rows)].
        self.__clear_grid()

    def update_object(self, name, location):
        '''
        Keeps a dictionary of all of the non-landmark objects in the simulation.
        (name, location) -> None
        arguments: name, a lowercase string name of a map object
                    location, a tuple of two ints of a map location
        For example: {'joe':(0, 0), 'junling':(1, 1)}
        '''
        # If location equals None, delete object from objects dictionary.
        if location == None and name in self.__objects:
            del self.__objects[name]
        # Else update dictionary with object name and location.
        elif location != None:
            self.__objects.update({name:location})

    def add_landmark(self, name, location):
        '''
        Same as update_object( ) except dictionary is like {'a':(0, 0), 'b':(1, 1)}
        Adds landmark of name 'letter' at location 'location
        (The only landmarks in this particular project are the waypoints.)
        '''

        self.__landmarks.update({name:location})

    def draw(self):
        '''
        Draw all __cells.  Each cell is ' .  ', or ' WO ' with a possible
            Waypoint and Object.
        '''

        if not self.__view_size:
            raise BadMsgError("Cannot 'show' the world until it has a size")

        else:
            self.__clear_grid( )
            for name, location in self.__landmarks.items():
                contents = self.__cells[location[0]][location[1]]
                # Change second character to landmark name initial.
                contents = contents[0] + name[0].title() + '  '
                self.__cells[location[0]][location[1]] = contents

            for name, location in self.__objects.items():
                contents = self.__cells[location[0]][location[1]]
                if contents[2] == ' ':
                    # Change third character to name initial.
                    contents = ' ' + contents[1] + name[0].title() + ' '
                else:
                    # Else multiple items at this location.
                    contents = ' ' + contents[1] + '* '
                self.__cells[location[0]][location[1]] = contents

            self.__draw_grid( )

    def __clear_grid(self):

        # Clear map grid, row by row
        for j in range(self.__num_rows):
            for i in range(self.__num_cols):
                self.__cells[i][j] = ' .  '

    # Display the map in the console.
    def __draw_grid(self):

        j = self.__num_rows - 1
        # Print each row. Start with the top row and go down to 0.
        while j >= 0:
            row_string = ''
            # Show the legend on the y-axis
            if j % 5 == 0:
                row_string = '%02d' % j + ' '
            else:
                row_string = '   '
            # Add each cell in the row.
            for i in range(self.__num_cols):
                row_string += self.__cells[i][j]
            print(row_string)
            j -= 1

        # Print x-axis legend.
        row_string = '  '
        for i in range(self.__num_cols):
            if i % 5 == 0:
                row_string += '  %02d' % i
            else:
                row_string += '    '
        print(row_string)
