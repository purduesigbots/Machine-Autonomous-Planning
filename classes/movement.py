from classes.converter import Converter as c

class Movement:

    def __init__(self, start, end, line_ref):
        self.start = start
        self.end = end
        self.line_ref = line_ref
        self.options = {
            "speed": 100,
            "flags": {
                "arms::ASYNC": False,
                "arms::ABSOLUTE": False,
                "arms::BACKWARDS": False,
                "arms::THRU": False,
            }
        }

    def clear(self, canvas):
        canvas.delete(self.line_ref)

    def draw(self, canvas):
        self.line_ref = canvas.create_line(self.start[0], self.start[1], self.end[0], self.end[1])
    
    def to_string(self):
        joined_flags = " | ".join([f for f in self.options["flags"] if self.options["flags"][f]])
        return f'chassis::move({{{c.convert_x(self.end[0])} , {c.convert_y(self.end[1])}}}, {self.options["speed"]}{", " + joined_flags if len(joined_flags) > 0 else ""});\n'