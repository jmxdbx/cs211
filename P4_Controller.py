"""
P4_Controller.py. CIS 211 Spring 2016 Project 4 Final. 2016-05-28.
Author: Joel Berry
Credits: Project spec, starter code by Anthony Hornof, 2016-04-08.

Basic Model-View-Controller fire-fighting simulation.
"""
import sys

import P4_Model
import P4_View
from P4_Utility import *

def main ():

# Create a local instance of a Controller and start the run() function.

    the_controller = Controller()
    the_controller.run()

class Controller:
    '''
    The controller object handles user keyboard input and provides textual to
    the console.  It follows the model view-controller software design pattern.
    '''

    def __init__(self):
        self.__input_filename = "commands.txt"
        self.__input_file_object = None
        self.__the_model = P4_Model.Model()
        self.__view = P4_View.View()
        self.__the_model.attach_view(self.__view)

    def run(self):
        '''
        () -> None.
        Process the command lines for the human-robot simulation.
        '''

        print("Starting Human-Robot Interaction Simulation")

        # Attempt to open input file from command line else default commands.txt.
        self.open_initial_input_file()

        # Command loop
        while True:
            try:

                # Get the next line of input whether it is from the user or a file.
                line = self.get_next_input_line()
                line_list = line.lower().split()

                # Quit Command.
                if len(line_list) == 1 and line_list[0] == "quit":
                    if self.__input_file_object:
                        print("Are you sure you want to quit? (Y/N)", end =" ")
                        if self.get_next_input_line().lower() == "y":
                            break
                        else:
                            continue
                    # Otherwise in user input mode, confirm that user wants to quit.
                    if input("Are you sure you want to quit? (Y/N)> ").lower().strip() == "y":
                        break
                    else:
                        continue

                # Status Command.
                elif len(line_list) == 1 and line_list[0] == "status":
                    self.__the_model.describe_all()

                # Show Command.
                elif len(line_list) == 1 and line_list[0] == "show":
                    self.do_show_command()

                # Create Command.
                elif len(line_list) > 1 and line_list[0] == "create":
                    self.__the_model.create_sim_object(line_list)

                # Go Update Command.
                elif len(line_list) == 1 and line_list[0] == "go":
                    self.__the_model.update()

                # Open Command.
                elif len(line_list) == 2 and line_list[0] == "open":
                    self.__input_filename = line_list[1]
                    self.open_input_file()

                # Human Robot Command.
                elif line_list and (self.__the_model.get_human(line_list[0]) or \
                    self.__the_model.get_robot(line_list[0])):
                    self.do_human_robot_command(line_list)

                # Else command is invalid, print error message.
                elif line:
                    raise BadLineError

            # Catch unrecognized commands and print error message.
            except BadLineError:
                print("Unrecognized command:", line)

            # Catch BadMsgErrors and print argument, the error message.
            except BadMsgError as message:
                print("Error:", message)

        # If file object exists, close file object.
        if self.__input_file_object:
            self.__input_file_object.close()
            self.__input_file_object = None

        return None

    def get_next_input_line(self):
        '''
        ( ) -> string
        • Displays the prompt.
        • Returns the next line to be processed, or '' if there is no line.
        • Gets the next line of text either from an input file or from the user,
          depending on the current setting of current_input_mode.
        • When reading from an input file, and either a blank line or an end of file
          is encountered, close the input file and set the file object var to None.
        '''

        user_line_prompt = "Time " + str(self.__the_model.get_time()) + " > "
        file_line_prompt = "Time " + str(self.__the_model.get_time()) + " FILE>"

        # Determine input mode by checking if open file object exists.
        if self.__input_file_object:
            # Read line into placeholder variable.
            next_line = self.__input_file_object.readline().strip()
            if not next_line:
                print("Closing file")
                self.__input_file_object.close()
                self.__input_file_object = None
            # Next line not empty, print file prompt.
            else:
                print(file_line_prompt, next_line)
            return next_line
        # Otherwise no file object, so proceed with user input mode.
        else:
            return input(user_line_prompt).strip()

    #===========================================================================
    def open_initial_input_file (self):
        '''
        Attempt to open a file for an initial set of commands.
        ( ) -> None
        If a filename was entered as a command line argument, overwrite the
          controller's member variable with that new filename.
        '''
        # Check command line for argument.
        if len(sys.argv) > 1:
            # Assign new file name to member variable.
            self.__input_filename = sys.argv[1]
        self.open_input_file()
        return None

    def open_input_file (self):
        '''
        ( ) -> None
        Attempts to open the filename in the input file member variable to
        execute a set of commands.
        '''
        # Attempt to open input file, assign file object to member variable.
        try:
            self.__input_file_object = open(self.__input_filename, 'r')
            print("Reading file:", self.__input_filename)
        except FileNotFoundError:
            print("File not found:", self.__input_filename)
        except PermissionError:
            print("You do not have permission to open file:", self.__input_filename)
        return None

    # Execute commands

    def do_human_robot_command(self, args):
        '''
        Parameters: args, a list of arguments that is already confirmed to be
                          nonempty with the first argument a traveler in the model.
        Returns:    None

        Processes the remainder of the arguments to insure that they at least
        represent valid locations on the map.  If they are valid,
        call the appropriate function calls in the model to build them.
        '''

        a_traveler = self.__the_model.get_object(args[0])

        # Check if stop command.
        if len(args) == 2 and args[1] == 'stop':
            a_traveler.stop()
            msg = a_traveler.get_class_name() + " " + a_traveler.get_name().title() +\
                  " stopped at location " + a_traveler.get_location()
            print(msg)

        elif len(args) > 1 and args[1] == 'move':
            if len(args) > 2:
                a_traveler.journey_to(args[2:])
            else:
                raise BadMsgError("Invalid move command")

        # Check if attack fire command.
        elif len(args) == 3 and type(a_traveler) == P4_Model.Robot:
            # Assign fire at location return value to variable.
            a_fire = self.__the_model.fire_at_location(a_traveler.get_location())
            if a_fire:
                a_traveler.fight_fire(a_fire)
                a_traveler.stop()
                print("Robot", a_traveler.get_name().title(), "at location",\
                      a_traveler.get_location(), "extinguishing fire",\
                      a_fire.get_name().title())
            #Else if fire exists but not in the same location, raise error.
            elif self.__the_model.get_fire(args[2]):
                msg = "Robot " + a_traveler.get_name().title() + " is not in the same location as fire " +\
                      args[2].title()
                raise BadMsgError(msg)

        else:
            if type(a_traveler) == P4_Model.Human:
                raise BadMsgError("Invalid human command")
            elif type(a_traveler) == P4_Model.Robot:
                raise BadMsgError("Invalid robot command")
        return None


    def do_show_command(self):
        '''
        ( ) -> None
        Calls draw method to display the map view.
        '''
        self.__view.draw()

#===============================================================================
main ()
#===============================================================================
