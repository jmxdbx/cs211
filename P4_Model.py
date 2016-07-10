"""
P4_Model.py. CIS 211 Spring 2016 Project 4 Final. 2016-05-28.
Author: Joel Berry
Credits: Project spec, starter code by Anthony Hornof, 2016-04-08.

Basic Model-View-Controller fire-fighting simulation.
"""
from P4_Utility import *

# Global constants.
WORLD_STR = 'world'
WAYPOINT_STR = 'waypoint'
HUMAN_STR = 'human'
ROBOT_STR = 'robot'
FIRE_STR = 'fire'
SIMS_STR = (WAYPOINT_STR, HUMAN_STR, ROBOT_STR, FIRE_STR)

class Model:
    '''
    The Model object keeps track of everything in the simulated world.
    Only one Model should be created in each run of the simulation.
    '''

    def __init__(self):
        self.__world_size = None
        self.__sim_objects = []
        self.__humans = []
        self.__robots = []
        self.__fires = []
        self.__waypoints = []
        self._time = 0
        self.__view = None
        global the_model
        the_model = self

    def __str__(self):
        if self.__world_size:
            return "The world is of size " + str(self.__world_size)

    def attach_view(self, v):
        self.__view = v

    def update(self):
        '''
        Update all simulation objects in the order in which they were created.
        Advance time by one minute.
        '''
        self._time += 1

        for item in self.__sim_objects:
            item.update()


    def notify_location(self, name, location):
        self.__view.update_object(name, location)

    def get_world_size(self):
        return self.__world_size

    def get_time(self):
        return self._time

    # Method to determine if location exists in the world.
    def get_valid_location(self, arg1, arg2=None):
        '''
        Determine if a location is in the world.  If yes, returns a tuple of ints.
        This function is made polymorphic by using "switch on type".

        Parameters: arg1 and arg2 are ints, OR
                    arg1 and arg2 are strings, OR
                    arg1 is a tuple of two ints, and no arg2 is provided, OR
                    arg1 is a tuple of two strings, and no arg2 is provided
        Returns:    a tuple of ints if the location is in the world
                    Raises BadMsgError if location invalid.

        Examples of use if the world is of size 30:
        self.get_valid_location(10, 20) -> (10, 20)
        self.get_valid_location('10', '20') -> (10, 20)
        self.get_valid_location((10, 20)) -> (10, 20)
        self.get_valid_location('a', '20') -> None
        self.get_valid_location(1.0, 20) -> None
        '''
        # Case 1, arg1 and arg2 are ints.
        if type(arg1) == type(arg2) == int:
            # Check if arg1, arg2 are a valid location in world.
            if all(0 <= i <= self.__world_size for i in (arg1, arg2)):
                return (arg1, arg2)

        # Case 2, arg1 and arg2 are strings.
        elif type(arg1) == type(arg2) == str:
            if arg1.isdigit() and arg2.isdigit():
                # Convert arg1, arg2 to int and assign to placeholder variables.
                x, y = int(arg1), int(arg2)
                # Check if x,y are a valid location in world.
                if all(0 <= i <= self.__world_size for i in (x, y)):
                    return (x, y)

        # Case 3,4 arg1 is a tuple, arg2 is not provided.
        elif type(arg1) == tuple and arg2 == None and len(arg1) == 2:
            # Assign arg1[0], arg1[1] to placeholder variables x,y.
            x, y = arg1[0], arg1[1]
            # Check if Case 3, tuple of two ints.
            if type(x) == type(y) == int:
                # Check if tuple is a valid location in world.
                if all(0 <= i <= self.__world_size for i in (x, y)):
                    return (x, y)
            # Else check if Case 4, tuple of two numeric strings.
            elif type(x) == type(y) == str:
                if x.isdigit() and y.isdigit():
                    # x,y numeric, so convert to int.
                    x, y = int(x), int(y)
                    # Check if tuple is a valid location in world.
                    if all(0 <= i <= self.__world_size for i in (x, y)):
                        return (x, y)
        # Otherwise, location was not a valid format or not in world, return None.
        return None


    def create_sim_object(self, arg_list):
        '''
        Create a simulation object based on the contents of the arg_list.
        Parameters: arg_list, list of strings entered after "create" command.
        Raises BadMsgError when a message needs to be passed to Controller,
        or BadLineError when the command could not be parsed.
        Returns:    None.

        The only assumption that can be made about the arg_list when entering
        this function is that there was at least one string in the command line
        after "create".
        '''

        MIN_WORLD_SIZE = 5
        MAX_WORLD_SIZE = 30

        # Check if command is create world, length 3, 3rd item is digit.
        if len(arg_list) == 3 and arg_list[1] == WORLD_STR and arg_list[2].isdigit():
            if self.__world_size:
                raise BadMsgError("World already exists")
            size = int(arg_list[2])
            if not MIN_WORLD_SIZE <= size <= MAX_WORLD_SIZE:
                raise BadMsgError("World size is out of range")
            # Else world size is valid, overwrite world size member variable.
            else:
                self.__view.create(size)
                self.__world_size = size
                print("Creating world of size ", size, sep="")

        # Verify command is create a valid object, and argument is length 5.
        elif len(arg_list) == 5 and arg_list[1] in SIMS_STR and arg_list[3].isdigit() and \
                arg_list[4].isdigit():

            if not self.__world_size:
                raise BadMsgError("A world must be created before any other objects")
            name = arg_list[2].lower()
            # Store potential location as tuple.
            loc = (int(arg_list[3]), int(arg_list[4]))

            # Check if command is create waypoint.
            if  arg_list[1] == WAYPOINT_STR:
                if not (name.isalpha() and len(name) == 1):
                    raise BadMsgError("Waypoint names must be single letters")
                # Check if waypoint already exists with name or location.
                for w in self.__waypoints:
                    if name == w.get_name() or loc == w.get_location():
                        msg = "Waypoint " + w.get_name().upper() + \
                                  " already exists at location " + str(w.get_location())
                        raise BadMsgError(msg)
                # Make sure location is valid.
                if not self.get_valid_location(loc):
                    raise BadMsgError("Invalid location")

                # Create New Waypoint object, append to __waypoints.
                self.__waypoints.append(Waypoint(name, loc))
                self.__view.add_landmark(name, loc)
                print("Creating waypoint ", name.title(), " at location ", loc, sep="")

            # Else arg_list[1] is human, robot, or fire.
            else:
                if not name.isalnum():
                    raise BadMsgError("Name must be alphanumeric")

                # Check if name is already used.
                if self.get_object(name):
                    # Assign object with preexisting name to placeholder.
                    dupe = self.get_object(name)
                    dupe_msg = dupe.get_class_name() + " already exists with that name"
                    raise BadMsgError(dupe_msg)

                # Make sure location is valid.
                if not self.get_valid_location(loc):
                    raise BadMsgError("Invalid location")
                print("Creating ", arg_list[1], " ", name.title(), " at location ", loc, sep='')

                # For each type of sim object, create the object and add it to its list.
                if arg_list[1] == HUMAN_STR:
                    new_sim = Human(name, loc)
                    self.__humans.append(new_sim)
                elif arg_list[1] == ROBOT_STR:
                    new_sim = Robot(name, loc)
                    self.__robots.append(new_sim)
                # Else arg_list[1] == FIRE_STR:
                else:
                    new_sim = Fire(name, loc)
                    self.__fires.append(new_sim)

                # Append new sim object to list of all non-waypoint sim objects.
                self.__sim_objects.append(new_sim)

                # Update the view with the new Sim Object
                self.__view.update_object(name, loc)

        # Otherwise argument could not be parsed.
        else:
            raise BadLineError

    def get_human(self, name):
        '''
        # Takes a name string.  Looks for a human with that name.  If one exists,
        #   returns that human.  If one does not, returns None.

        Parameters: name, a string
        Returns:    Either a pointer to a human object, or None
        '''
        # Return human object pointer if name in __humans list.
        for human in self.__humans:
            if human.get_name() == name:
                return human
        return None

    def get_robot(self, name):
        '''
        Takes a name string.  Looks for a robot with that name.  If one exists,
        returns that robot.  If one does not, returns None.

        Parameters: name, a string
        Returns:    Either a pointer to a robot object, or None
        '''
        # Return robot object pointer if name in __robots list.
        for robot in self.__robots:
            if robot.get_name() == name:
                return robot
        return None

    def get_fire(self, name):
        '''
        Takes a name string.  Looks for a fire with that name.  If one exists,
        returns that fire.  If one does not, returns None.

        Parameters: name, a string
        Returns:    Either a pointer to a fire object, or None
        '''
        # Return fire object pointer if name in __fires list.
        for fire in self.__fires:
            if fire.get_name() == name:
                return fire
        return None

    def fire_at_location(self, location):
        '''
        Takes a location string.  Looks for a fire at that location.  If one exists,
        returns that fire object. Otherwise returns None.

        Parameters: location, a tuple of ints
        Returns:    Either a pointer to a fire object, or None
        '''
        # Return fire object pointer if name in __fires list.
        for fire in self.__fires:
            if fire.get_location() == location:
                return fire
        return None

    # Delete fire object from model and view.
    def delete_fire(self, name):
        # Calling view update object with location argument None deletes object from view.
        self.__view.update_object(name, None)
        #Delete object from fires list.
        for fire in self.__fires:
            if fire.get_name() == name:
                self.__fires.remove(fire)
        # Delete object from Sim Objects list.
        for item in self.__sim_objects:
            if item.get_name() == name and type(item) == Fire:
                self.__sim_objects.remove(item)


    def get_object(self, name):
        '''
        Takes a name string.  Looks for an SimObject other than waypoint
        with that name.  If one exists,
        #returns that object.  If one does not, returns None.

        Parameters: name, a string
        Returns:    Either a pointer to an object, or None
        '''
        # Return object pointer if name in __sim_objects list.
        for item in self.__sim_objects:
            if item.get_name() == name:
                return item
        return None

    def get_waypoint_location(self, name):
        '''
        Takes a name string.  Looks for a waypoint with that name.  If one exists,
        returns waypoint location.  If one does not, returns None.

        Parameters: name, a string
        Returns:    Either a waypoint location, or None
        '''
        # Return waypoint object location if name in __waypoints list.
        for waypoint in self.__waypoints:
            if waypoint.get_name() == name:
                return waypoint.get_location()
        return None

    def describe_all(self):
        '''
        Each of the simulation objects describes itself in text.
        ( ) -> None
        '''
        # Print initial line as per spec, regardless of world contents.
        print("The contents of the world are as follows:")
        if self.__world_size:
            print(self)
        for item in self.__waypoints:
            print(item)
        for item in self.__humans:
            print(item)
        for item in self.__robots:
            print(item)
        for item in self.__fires:
            print(item)
        return None


#===============================================================================
class SimObject:
    '''
    SimObject superclass.
    '''
    def __init__(self, name, location):
        self._name = name.lower()
        self._location = location
    def __str__(self):
        return self._name.title() + " at location " + str(self._location)

    def get_name(self):
        return self._name

    def get_location(self):
         return self._location

    def get_class_name(self):
        return self.__class__.__name__

class Traveler(SimObject):
    '''
    Traveler class. Inherits from SimObject.
    '''
    def __init__(self, name, location):
        # Call parent's init method.
        super().__init__(name, location)
        self._destination_list = []
        self._moving = False

    def move_to(self, location):
        self._location = location
        #If arrived at next destination:
        if location == self._destination_list[0]:
            # Remove first item of destination list.
            self._destination_list = self._destination_list[1:]
            # If list is now empty, set moving status to false.
            if not self._destination_list:
                self.stop()
                print(self.get_class_name(), " ", self._name.title(), " arrived at location ", self._location, sep="")
        # Notify the_model that location moved.
        the_model.notify_location(self._name, self._location)

    def set_moving(self):
        self._moving = True

    def journey_to(self, destination_list):
        '''
        Accepts a list of potential destinations. Verifies that they are valid locations
        and could be reached with only straight line movements. If so, updates destination_list
        and moving member variables. If not, raises BadMsgError.
        :param destination_list: list
        :return: None
        '''
        #Initialize 'previous' location variable to compare to next destination.
        prev = self._location
        tup_list = []
        for loc in destination_list:
            # Create msg error string for potential errors.
            msg = "'" + loc + "'" + " is not a valid location for this 'move'"
            if loc.isalpha():
                # Assign return value of get_waypoint_location to loc.
                loc = the_model.get_waypoint_location(loc)
                if not loc:
                    raise BadMsgError(msg)
            # Check if item is length 3 or greater in csv form with one comma.
            elif len(loc) > 2 and (',' in loc[1:-1]) and loc.count(',') == 1:
                # split at the comma.
                ici_list = loc.split(',')
                if ici_list[0].isdigit() and ici_list[1].isdigit():
                    loc = tuple([int(i) for i in ici_list])
            if not the_model.get_valid_location(loc):
                raise BadMsgError(msg)
            # Location exists on map. Verify straight line path from previous location.
            if not ((loc[0] == prev[0]) or (loc[1] == prev[1])):
                raise BadMsgError(msg)
            #Destination is valid, append to tuple list.
            tup_list.append(loc)
            #Assign loc to prev and continue next iteration.
            prev = loc
        # All items in destination_list have been verified
        # Set destination list member variable to tup_list of destination location tuples.
        self._destination_list = tup_list
        # Set moving member variable to True.
        self.set_moving()
        print(self.get_class_name(), self._name.title(), "at location",\
        self._location, "moving to", ", ".join(str(item) for item in self._destination_list))



    def get_next_moving_location(self):
        '''
        If traveler currently moving, returns location one unit closer to next location in
        destination list.
        :return: location tuple of two ints
        '''
        if self._moving:
            # Temporarily assign current location coordinates to next_x, next_y.
            next_x, next_y = self._location
            # Check if next movement is vertical, x-coordinates will be equal.
            if self._destination_list[0][0] == self._location[0]:
                # If difference of destination y-cord and current location is positive
                if (self._destination_list[0][1] - self._location[1]) > 0:
                    # Assign correct y-cord value.
                    next_y = self._location[1] + 1
                # Else movement will be downwards, assign correct y-cord value.
                else:
                    next_y = self._location[1] - 1
            # Else next movement horizontal, y coordinates will be equal.
            else:
                # If difference of destination x-cord and current location is positive
                if (self._destination_list[0][0] - self._location[0]) > 0:
                    # Assign correct y-cord value.
                    next_x = self._location[0] + 1
                # Else movement will be downwards, assign correct y-cord value.
                else:
                    next_x = self._location[0] - 1
            return (next_x, next_y)



    def stop(self):
        if self._moving:
            self._moving = False
            # Clear destination list.
            self._destination_list = []


class Human(Traveler):
    '''
    A human in the simulation. Subclass of Traveler.
    '''
    def __str__(self):
        if self._moving:
            return "Human " + super().__str__() + " moving to " +\
                   ", ".join(str(item) for item in self._destination_list)
        else:
            return "Human " + super().__str__()

    def update(self):
        if self._moving:
            next_loc = self.get_next_moving_location()
            #Assign fire to temporary variable, will be None if no fire.
            a_fire = the_model.fire_at_location(next_loc)
            #Check if next location is a fire object.
            if a_fire:
                self.stop()
                print("Human", self._name.title(), "stopping short of fire", a_fire._name.title())
            else:
                #Else no fire, move to next moving location.
                self.move_to(next_loc)

class Robot(Traveler):
    '''
    A robot in the simulation. Subclass of Traveler.
    '''
    def __init__(self, name, location):
        super().__init__(name, location)
        self._extinguishing_fire = None

    def __str__(self):
        if self._moving:
            return "Robot " + super().__str__() + " moving to " + \
                   ", ".join(str(item) for item in self._destination_list)
        if self._extinguishing_fire:
            return "Robot " + super().__str__() + " extinguishing fire " + self._extinguishing_fire._name.title()
        else:
            return "Robot " + super().__str__()

    def fight_fire(self, fire_object):
        self._extinguishing_fire = fire_object

    def stop_fighting_fire(self, fire_object):
        if self._extinguishing_fire:
            self._extinguishing_fire = None

    def update(self):
        if self._moving:
            self.move_to(self.get_next_moving_location())
        if self._extinguishing_fire:
            self._extinguishing_fire.reduce_strength()
            # If fire strength zero, remove from extinguishing.
            if self._extinguishing_fire.get_strength() == 0:
                self.stop_fighting_fire(self._extinguishing_fire)

    def set_moving(self):
        self._moving = True
        self._extinguishing_fire = None


class Waypoint(SimObject):
    '''
    A waypoint in the simulation. Subclass of SimObject.
    '''
    def __str__(self):
        return "Waypoint " + super().__str__()

class Fire(SimObject):
    '''
    A waypoint in the simulation. Subclass of SimObject.
    '''
    def __init__(self, name, location):
        super().__init__(name, location)
        self._strength = 5

    def __str__(self):
        return "Fire " + super().__str__() + " of strength " + str(self._strength)

    def __del__(self):
        print("Fire", self._name.title(), "has disappeared from the simulation")

    def get_strength(self):
        return self._strength

    def reduce_strength(self):
        if self._strength > 0:
            self._strength -= 1
        if self._strength <= 0:
            the_model.delete_fire(self._name)

    def update(self):
        pass
