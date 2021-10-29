from lexer.lexem import Lexem


class LexerException(Exception):
    pass


class Lexer:
    def __init__(self, file):
        self.file = open(file, 'r')
        self.symbol = self.file.read(1)
        self.res = {"and", "array", "asm", "begin", "case", "const", "constructor", "destructor", "do",
                    "downto", "else", "end", "exports", "file", "for", "function", "goto", "if", "implementation",
                    "in", "inherited", "inline", "interface", "label", "library", "nil", "not", "object",
                    "of", "or", "packed", "procedure", "program", "record", "repeat", "set", "shl", "shr",
                    "string", "then", "to", "type", "unit", "until", "uses", "var", "while", "with", "xor",
                    "abs", "arctan", "boolean", "char", "chr", "cos", "dispose", "eof", "eoln", "exp",
                    "false", "get", "input", "integer", "ln", "maxint", "new", "odd", "ord", "output",
                    "pack", "page", "pred", "put", "read", "readln", "real", "reset", "rewrite", "round",
                    "sin", "sqr", "sqrt", "succ", "text", "true", "trunc", "unpack", "write", "writeln"}
        self.spaces = {'', ' ', '\n', '\t', '\0', '\r'}
        self.operat = {'+', '-', '*', '/', '=', '<', '>', "div", "mod"}
        self.operat_arr = {'+', '-', '*', '/'}
        self.operat_bool = {'>', '<'}
        self.assign = {":=", "+=", "-=", "*=", "/="}
        self.seps = {'.', ',', ':', ';', '(', ')', '[', ']'}

        self.undefined = "undefined"
        self.identifier = "identifier"
        self.integer = "integer"
        self.real = "real"
        self.string = "string"
        self.operation = "operation"
        self.comment_long = "long comment"
        self.comment = "comment"
        self.separator = "separator"
        self.error = "error"
        self.real_e = "real e"
        self.real_sign = "real sign"
        self.real_degree = "real degree"
        self.literal_string_sharp = "literal string sharp"
        self.literal_string_number = "literal string number"
        self.integer16 = "integer16"
        self.integer8 = "integer8"
        self.integer2 = "integer2"

        self.state = self.undefined
        self.buffer = ""
        self.coordinates = {"line": 1, "col": 1}
        self.current_coordinates = 0
        self.lexem = 0
        self.text = ""

    def get_current_lexem(self):
        return self.lexem

    def get_next_lexem(self):
        self.clear_buffer()
        while self.symbol or self.buffer:
            if self.state == self.undefined:
                if self.symbol in self.spaces:
                    if self.symbol == "\n":
                        self.new_line()
                    self.get_next_symbol()
                elif self.symbol.isalpha():
                    self.state = self.identifier
                    self.save_coordinates()
                    self.add_buffer()
                    self.get_next_symbol()
                elif self.symbol.isdigit():
                    self.state = self.integer
                    self.save_coordinates()
                    self.add_buffer()
                    self.get_next_symbol()
                elif self.symbol == "'":
                    self.state = self.string
                    self.save_coordinates()
                    self.add_buffer()
                    self.get_next_symbol()
                elif self.symbol == '#':
                    self.state = self.literal_string_sharp
                    self.save_coordinates()
                    self.add_buffer()
                    self.get_next_symbol()
                elif self.symbol in self.operat:
                    self.state = self.operation
                    self.save_coordinates()
                    self.add_buffer()
                    self.get_next_symbol()
                elif self.symbol in self.seps:
                    self.save_coordinates()
                    self.add_buffer()
                    self.get_next_symbol()
                    self.state = self.separator
                elif self.symbol == '{':
                    self.add_buffer()
                    self.get_next_symbol()
                    self.state = self.comment_long
                elif self.symbol == '$':
                    self.save_coordinates()
                    self.add_buffer()
                    self.get_next_symbol()
                    self.state = self.integer16
                elif self.symbol == '%':
                    self.save_coordinates()
                    self.add_buffer()
                    self.get_next_symbol()
                    self.state = self.integer2
                elif self.symbol == '&':
                    self.save_coordinates()
                    self.add_buffer()
                    self.get_next_symbol()
                    self.state = self.integer8
                else:
                    self.save_coordinates()
                    self.state = self.error
                    self.add_buffer()
                    self.get_next_symbol()
            elif self.state == self.identifier:
                if self.symbol.isalpha() or self.symbol.isdigit() or self.symbol == "_":
                    self.add_buffer()
                    self.get_next_symbol()
                else:
                    self.state = self.undefined
                    if self.buffer.lower() in self.res:
                        self.lexem = Lexem(self.current_coordinates, "reserved var", self.buffer, self.buffer.lower())
                        return self.lexem
                    elif self.buffer.lower() in self.operat:
                        self.lexem = Lexem(self.current_coordinates, "operation", self.buffer, self.buffer.lower())
                        return self.lexem
                    else:
                        self.lexem = Lexem(self.current_coordinates, "variable", self.buffer, self.buffer.lower())
                        return self.lexem
            elif self.state == self.integer:
                if self.symbol.lower() == 'e':
                    self.add_buffer()
                    self.get_next_symbol()
                    self.state = self.real_e
                elif self.symbol == ".":
                    self.state = self.real
                    self.add_buffer()
                    self.get_next_symbol()
                elif self.symbol.isdigit():
                    self.add_buffer()
                    self.get_next_symbol()
                else:
                    self.state = self.undefined
                    self.lexem = Lexem(self.current_coordinates, "integer", self.buffer, int(self.buffer))
                    return self.lexem
            elif self.state == self.real:
                if self.symbol.lower() == 'e':
                    self.add_buffer()
                    self.get_next_symbol()
                    self.state = self.real_e
                elif self.symbol.isdigit():
                    self.add_buffer()
                    self.get_next_symbol()
                elif self.buffer.endswith('.') and not self.symbol.isdigit():
                    self.state = self.error
                    self.add_buffer()
                    self.get_next_symbol()
                else:
                    self.state = self.undefined
                    self.lexem = Lexem(self.current_coordinates, "real", self.buffer, float(self.buffer))
                    return self.lexem
            elif self.state == self.real_e:
                if self.symbol.isdigit():
                    self.state = self.real_degree
                    self.add_buffer()
                    self.get_next_symbol()
                elif self.symbol in {'+', '-'}:
                    self.state = self.real_sign
                    self.add_buffer()
                    self.get_next_symbol()
                else:
                    self.state = self.error
                    self.add_buffer()
                    self.get_next_symbol()
            elif self.state == self.real_sign:
                if self.symbol.isdigit():
                    self.state = self.real_degree
                    self.add_buffer()
                    self.get_next_symbol()
                else:
                    self.state = self.error
                    self.add_buffer()
                    self.get_next_symbol()
            elif self.state == self.real_degree:
                if self.symbol.isdigit():
                    self.add_buffer()
                    self.get_next_symbol()
                else:
                    self.state = self.undefined
                    self.lexem = Lexem(self.current_coordinates, "real", self.buffer, float(self.buffer))
                    return self.lexem
            elif self.state == self.string:
                if self.symbol == "\n" or self.symbol == "":
                    self.state = self.error
                elif self.symbol != "'":
                    self.add_buffer()
                    self.get_next_symbol()
                else:
                    self.state = self.undefined
                    self.add_buffer()
                    self.get_next_symbol()
                    if self.symbol == '#':
                        self.state = self.literal_string_sharp
                        self.add_buffer()
                        self.get_next_symbol()
                    else:
                        self.state = self.undefined
                        self.lexem = Lexem(self.current_coordinates, "string", self.buffer,
                                           self.process_literal(self.buffer))
                        return self.lexem
            elif self.state == self.literal_string_sharp:
                if self.symbol.isdigit():
                    self.state = self.literal_string_number
                    self.add_buffer()
                    self.get_next_symbol()
                else:
                    self.state = self.error
                    self.text = f"error after #:{self.symbol}"
            elif self.state == self.literal_string_number:
                if self.symbol == '#':
                    self.state = self.literal_string_sharp
                    self.add_buffer()
                    self.get_next_symbol()
                elif self.symbol.isdigit():
                    self.add_buffer()
                    self.get_next_symbol()
                elif self.symbol == "'":
                    self.state = self.string
                    self.add_buffer()
                    self.get_next_symbol()
                else:
                    self.state = self.undefined
                    self.lexem = Lexem(self.current_coordinates, "string", self.buffer,
                                       self.process_literal(self.buffer))
                    return self.lexem
            elif self.state == self.operation:
                if self.buffer in self.operat_arr and self.symbol == '=':
                    self.state = self.undefined
                    self.add_buffer()
                    self.get_next_symbol()
                    self.lexem = Lexem(self.current_coordinates, "assigner", self.buffer, self.buffer)
                    return self.lexem
                if self.symbol == '/' and self.buffer == '/':
                    self.get_next_symbol()
                    self.clear_buffer()
                    self.state = self.comment
                elif self.buffer == '*' and self.symbol == '*':
                    self.add_buffer()
                    self.get_next_symbol()
                else:
                    self.state = self.undefined
                    self.lexem = Lexem(self.current_coordinates, "operation", self.buffer, self.buffer)
                    return self.lexem
            elif self.state == self.comment_long:
                if self.symbol == "":
                    self.save_coordinates()
                    raise LexerException(
                        f"{self.current_coordinates['line']}:{self.current_coordinates['col']}        " + "error: } was expected")
                elif self.symbol != '}':
                    if self.symbol == "\n":
                        self.new_line()
                    self.get_next_symbol()
                else:
                    self.clear_buffer()
                    self.state = self.undefined
                    self.get_next_symbol()
            elif self.state == self.comment:
                if self.symbol != "\n":
                    self.get_next_symbol()
                else:
                    self.state = self.undefined
            elif self.state == self.separator:
                self.state = self.undefined
                if self.buffer == ':' and self.symbol == '=':
                    self.add_buffer()
                    self.get_next_symbol()
                    self.lexem = Lexem(self.current_coordinates, "assigner", self.buffer, self.buffer)
                    return self.lexem
                self.lexem = Lexem(self.current_coordinates, "separator", self.buffer, self.buffer)  #
                return self.lexem
            elif self.state == self.integer16:
                if self.symbol.isdigit() or 'a' <= self.symbol.lower() <= 'f':
                    self.add_buffer()
                    self.get_next_symbol()
                else:
                    self.state = self.undefined
                    self.lexem = Lexem(self.current_coordinates, "integer16", self.buffer, int(self.buffer[1:], 16))
                    return self.lexem
            elif self.state == self.integer8:
                if self.symbol.isdigit():
                    if int(self.symbol) >= 0 and int(self.symbol) <= 7:
                        self.add_buffer()
                        self.get_next_symbol()
                    else:
                        self.state = self.error
                else:
                    self.state = self.undefined
                    self.lexem = Lexem(self.current_coordinates, "integer8", self.buffer, int(self.buffer[1:], 8))
                    return self.lexem
            elif self.state == self.integer2:
                if self.symbol.isdigit():
                    if int(self.symbol) == 0 or int(self.symbol) == 1:
                        self.add_buffer()
                        self.get_next_symbol()
                    else:
                        self.state = self.error
                else:
                    self.state = self.undefined
                    self.lexem = Lexem(self.current_coordinates, "integer2", self.buffer, int(self.buffer[1:], 2))
                    return self.lexem
            elif self.state == self.error:
                if self.symbol in self.spaces or self.symbol in self.seps:
                    self.display_error(f"error: {self.buffer}")
                else:
                    self.add_buffer()
                    self.get_next_symbol()
        self.lexem = False
        return False

    def get_next_symbol(self):
        self.symbol = self.file.read(1)
        self.coordinates["col"] += 1

    def new_line(self):
        self.coordinates["line"] += 1
        self.coordinates["col"] = 0

    def add_buffer(self):
        self.buffer += self.symbol

    def clear_buffer(self):
        self.buffer = ""

    def save_coordinates(self):
        self.current_coordinates = self.coordinates.copy()

    def display_error(self, text):
        text = f"{self.current_coordinates['line']}:{self.current_coordinates['col']}        {text}"
        raise LexerException(text)

    def process_literal(self, text):
        isstring = False
        buffer = ""
        output = ""
        for t in text:
            if isstring:
                if t == "'":
                    isstring = False
                else:
                    output += t
            else:
                if t == "'":
                    isstring = True
                    if buffer:
                        output += chr(int(buffer))
                        buffer = ""
                elif t.isdigit():
                    buffer += t
                elif t == "#":
                    if buffer:
                        output += chr(int(buffer))
                        buffer = ""
        if buffer:
            output += chr(int(buffer))
            buffer = ""
        return f"'{output}'"
