import os
import sys
from classes.converter import Converter as c
from classes.movement import Movement


class Parser:

    def __init__(self, movements=None):
        self.movements = movements

        # TODO: write code to import an auton script
    def import_script(self):
        pass

    # Export path as cpp script
    def export_script(self):
        # Create the output directory
        if not os.path.exists("output"):
            os.mkdir("output")
        # Create and open the output file

        if not self.movements:
            print("Can't export nothing!")
            return
        
        f = open("output/script.cpp", "w")

        # Reset odom coordinates to first arrow's start point
        f.write(
            f'odom::reset({{{c.convert_x(self.movements[0].start[0])}, {c.convert_y(self.movements[0].start[1])}}});\n')
        # Convert all movements into code
        for m in self.movements:
            f.write(m.toString())
        f.close()

    def import_script(self):

        # Check if the script.cpp file exists
        if not os.path.isfile(os.path.join("output","script.cpp")):
            try:
                os.mkdir("output")
            except:
                pass
            print("Please put script.cpp into the output directory")
            sys.exit()

        # Open the script
        f = open("output/script.cpp","r")

        start = None # Starting point based on odom::reset
        moves=[]
        allLines = f.readlines() # Read the script

        for l in allLines:
            if "odom::reset" in l and start == None:
                # Get the start position with string indexing

                # Remove whitespace and get values between curly brackets
                data = "".join(l[l.index("{") : l.index("}")].split())[1:]
                dsplit = data.split(",")

                # Get start position
                start = (
                    c.convert_x_reverse(float(dsplit[0])), 
                    c.convert_y_reverse(float(dsplit[1]))
                )

            elif "chassis::move" in l:
                # Remove whitespace and get values between parenthesis
                data = "".join(l[l.index("(") : l.index(")")].split())

                # Get endpoint data of odom movement
                pos = data[data.index("{")+1 : data.index("}")].split(",")

                # Remove endpoint part from 'data'
                data = data[data.index("},")+2:]

                # Set the endpoint
                endpoint = (
                    c.convert_x_reverse(float(pos[0])), 
                    c.convert_y_reverse(float(pos[1]))
                )


                speed = 0

                # Check if there are any flags before fetching speed value
                if "," in data:

                    # Get the speed value and remove it from 'data'
                    speed = float(data[:data.index(",")])
                    data = data[data.index(",")+1:]
                else:
                    # Get the speed value and clear data
                    speed = float(data)
                    data = ""

                '''
                Create a new Movement based on:
                - Current number of movements
                - determined endpoint
                - determined startpoint
                - previous movement
                '''
                themove = Movement(
                    name = "Movement " + str(len(moves)+1),
                    endpoint = endpoint,
                    start = start,
                    prev = moves[len(moves)-1] if moves else None
                )

                # Set the movements speed to the parsed speed
                themove.options["speed"] = speed

                # Set the movement's flags to the parsed flags
                for k in themove.options["flags"].keys():
                    if k in data:
                        themove.options["flags"][k] = True
                
                # Add the movement to our list of moves
                moves.append(themove)

        # Return all parsed moves
        return moves