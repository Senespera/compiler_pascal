import os.path
import sys
from parse.parser_expr import ParserException, ParserExpr
from lexer.lexer import Lexer, LexerException
#-l -f lexer/program.txt
#-l -d lexer/tests
#-p -f parse/program.txt
#-p -d parse/tests


def command_handler():
    mode = ""
    process_type = ""
    for i in range (len(sys.argv)):
        if sys.argv[i] == '-l':
            mode = "lexer"
        if sys.argv[i] == '-p':
            mode = "parser"
        if sys.argv[i] == '-f':
            process_type = "file"
        if sys.argv[i] == "-d":
            process_type = "dir"
        if  os.path.isfile(sys.argv[i]) or os.path.isdir(sys.argv[i]):
            path = sys.argv[i]

    if mode == "lexer":
        if process_type == "file":
            if os.path.isfile(path):
                try:
                    lexer = Lexer(path)
                    lex = lexer.get_next_lexem()
                    if lex:
                        print(lex.print())
                    while lex:
                        lex = lexer.get_next_lexem()
                        if lex:
                            print(lex.print())
                except LexerException as e:
                    print(e)
        elif process_type == "dir":
            if os.path.isdir(path):
                tests_total = 0
                tests_failed = 0
                for file in os.listdir(path):
                    abspath = path+"/"+file
                    if abspath.endswith("(code).txt"):
                        tests_total += 1
                        lexer = Lexer(abspath)
                        fileres = open(abspath.replace("(code)",""),'r')
                        fileoutput = open(abspath.replace("code","output"),'w+')
                        fileoutput.seek(0)
                        fileoutput.truncate()
                        try:
                            lex = lexer.get_next_lexem()
                            if lex:
                                fileoutput.write(lex.print()+"\n")
                            while lex:
                                lex = lexer.get_next_lexem()
                                if lex:
                                    fileoutput.write(lex.print()+"\n")
                            if fileoutput.tell() != 0:
                                fileoutput = open(abspath.replace("code", "output"))
                                x=fileoutput.read()
                                fileoutput.close()
                                os.remove(abspath.replace("code", "output"))
                                open(abspath.replace("code", "output"),'w').write(x[:-1])
                        except LexerException as e:
                            fileoutput.write(str(e))
                        fileoutput.close()
                        fileoutput = open(abspath.replace("code", "output"), 'r')
                        output = fileoutput.read()
                        results = fileres.read()
                        if output != results:
                            tests_failed += 1
                            print(f"{file} - failed")
                        else:
                            print (f"{file} - passed")
                print(f"{tests_total} total")
                print(f"{tests_failed} failed")
    elif mode == "parser":
        if process_type == "file":
            if os.path.isfile(path):
                try:
                    lexer = Lexer(path)
                    lexer.get_next_lexem()
                    parser = ParserExpr(lexer).parse_expr()
                    if parser:
                        parser = parser.print()
                    print(parser)
                except ParserException as e:
                    print(e)
                except LexerException as e:
                    print(e)
        if process_type == "dir":
            if os.path.isdir(path):
                tests_total = 0
                tests_failed = 0
                for file in os.listdir(path):
                    abspath = path+"/"+file
                    if abspath.endswith("(code).txt"):
                        tests_total += 1
                        lexer = Lexer(abspath)
                        fileres = open(abspath.replace("(code)",""),'r')
                        fileoutput = open(abspath.replace("code","output"),'w+')
                        fileoutput.seek(0)
                        fileoutput.truncate()
                        try:
                            lexer.get_next_lexem()
                            parser = ParserExpr(lexer).parse_expr()
                            if parser:
                                parser = parser.print()
                            fileoutput.write(parser)
                        except ParserException as e:
                            fileoutput.write(str(e))
                        except LexerException as e:
                            fileoutput.write(str(e))
                        fileoutput.close()
                        fileoutput = open(abspath.replace("code", "output"), 'r')
                        output = fileoutput.read()
                        results = fileres.read()
                        if output != results:
                            tests_failed += 1
                            print(f"{file} - failed")
                        else:
                            print (f"{file} - passed")
                print(f"{tests_total} total")
                print(f"{tests_failed} failed")



if __name__ == '__main__':
    command_handler()