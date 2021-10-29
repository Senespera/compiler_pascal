class Lexem:
    def __init__(self, coordinates, type_lexem, code, value):
        self.coordinates = coordinates
        self.type_lexem = type_lexem
        self.code = code
        self.value = value

    def print(self):
        return f"{self.coordinates['line']}:{self.coordinates['col']}        {self.type_lexem}        {self.code}        {self.value}"

    def get_type(self):
        return self.type_lexem

    def get_value(self):
        return self.value

    def get_coordinates(self):
        return f"{self.coordinates['line']}:{self.coordinates['col']}"

    def get_code(self):
        return self.code