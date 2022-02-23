import os
from classes.converter import Converter as c


class Parser:

    def __init__(self, movements):
        self.movements = movements

        # TODO: write code to import an auton script
    def import_script(self):
        pass

    # Export path as cpp script
    def export_script(self):
        if not os.path.exists("output"):
            os.mkdir("output")
        f = open("output/script.cpp", "w")
        f.write(
            f'odom::reset({{{c.convert_x(self.movements[0].start[0])}, {c.convert_y(self.movements[0].start[1])}}});\n')
        for m in self.movements:
            f.write(m.toString())
        f.close()
