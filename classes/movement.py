class Movement:

    def __init__(self, start, end, line_ref):
        self.start = start
        self.end = end
        self.line_ref = line_ref

    def clear(self, canvas):
        canvas.delete(self.line_ref)

    def draw(self, canvas):
        self.line_ref = canvas.create_line(self.start[0], self.start[1], self.end[0], self.end[1])