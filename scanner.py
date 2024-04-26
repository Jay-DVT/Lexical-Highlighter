import re
from enum import Enum


class Scanner:
    def __init__(self) -> None:
        self.source = [str]
        self.line = 1
        self.start = 0
        self.current = 0
        self.tokens = []
        self.variables = []
        self.functions = []


class TokenType(Enum):
    TOKEN_COMMENT = 0
    TOKEN_EOF = 1
    TOKEN_ERROR = 2
    TOKEN_FUNCTION = 3
    TOKEN_IDENTIFIER = 4
    TOKEN_KEYWORD = 5
    TOKEN_LEFT_PAREN = 6
    TOKEN_LITERAL = 7
    TOKEN_OPERATOR = 8
    TOKEN_RIGHT_PAREN = 9
    TOKEN_STRING = 10
    TOKEN_TYPE = 11
    TOKEN_VARIABLE = 12


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, start: int, end: int) -> None:
        self.token_type = token_type
        self.lexeme = lexeme
        self.start = start
        self.end = end


scanner = Scanner()


def peek():
    if scanner.current >= len(scanner.source):
        return '\0'
    return scanner.source[scanner.current]


def peek_skip_whitespace():
    current = scanner.current
    while current < len(scanner.source):
        if scanner.source[current] == ' ' or scanner.source[current] == '\t':
            current += 1
        else:
            break
    return scanner.source[current]


def is_digit(c):
    return c >= '0' and c <= '9'


def is_alpha(c):
    return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_'


def skip_whitespace():
    while True:
        c = peek()
        match c:
            case ' ':
                advance()
            case '\r':
                advance()
            case '\t':
                advance()
            case '\n':
                scanner.line += 1
                advance()
            case _:
                break


def advance():
    scanner.current += 1
    return scanner.source[scanner.current - 1]


def variable():
    word = scanner.source[scanner.start:scanner.current]
    if word in scanner.variables:
        return TokenType.TOKEN_LITERAL
    elif word in scanner.functions:
        return TokenType.TOKEN_FUNCTION

    operator = peek_skip_whitespace()
    if not operator:
        return TokenType.TOKEN_IDENTIFIER

    match operator:
        case '(':
            scanner.functions.append(word)
            return TokenType.TOKEN_LITERAL
        case '=':
            scanner.variables.append(word)
            return TokenType.TOKEN_VARIABLE
        case _:
            pass

    return TokenType.TOKEN_IDENTIFIER


def check_keyword(start, length, rest):
    start += scanner.start
    word = scanner.source[start:start + length]
    if word == rest:
        return TokenType.TOKEN_KEYWORD
    else:
        return variable()


def make_token(token_type):
    scanner.tokens.append(Token(
        token_type, scanner.source[scanner.start:scanner.current], scanner.start, scanner.current))
    return token_type


def is_at_end():
    return scanner.current >= len(scanner.source)


def identifier_type():
    match scanner.source[scanner.start]:
        case 'a':
            return check_keyword(1, 3, "uto")
        case 'b':
            return check_keyword(1, 4, "reak")
        case 'c':
            match scanner.source[scanner.start + 1]:
                case 'a':
                    return check_keyword(2, 2, "se")
                case 'h':
                    return check_keyword(2, 2, "ar")
                case 'o':
                    match scanner.source[scanner.start + 2]:
                        case 'n':
                            match scanner.source[scanner.start + 3]:
                                case 's':
                                    return check_keyword(4, 1, "t")
                                case 't':
                                    return check_keyword(4, 4, "inue")
        case 'd':
            match scanner.source[scanner.start + 1]:
                case 'e':
                    return check_keyword(2, 5, "fault")
                    # do or double
                case 'o':
                    if scanner.source[scanner.start + 2] == 'u':
                        return check_keyword(3, 3, "ble")
                    else:
                        return check_keyword(1, 1, "o")
        case 'e':
            match scanner.source[scanner.start + 1]:
                case 'l':
                    return check_keyword(2, 2, "se")
                case 'n':
                    return check_keyword(2, 2, "um")
                case 'x':
                    return check_keyword(2, 4, "tern")
        case 'f':
            match scanner.source[scanner.start + 1]:
                case 'l':
                    return check_keyword(2, 3, "oat")
                case 'o':
                    return check_keyword(2, 1, "r")
        case 'g':
            return check_keyword(1, 3, "oto")
        case 'i':
            match scanner.source[scanner.start + 1]:
                case 'f':
                    return check_keyword(2, 0, "")
                case 'n':
                    return check_keyword(2, 1, "t")
        case 'l':
            return check_keyword(1, 3, "ong")
        case 'r':
            match scanner.source[scanner.start + 1]:
                case 'e':
                    match scanner.source[scanner.start + 2]:
                        case 'g':
                            return check_keyword(3, 5, "ister")
                        case 't':
                            return check_keyword(3, 3, "urn")
        case 's':
            match scanner.source[scanner.start + 1]:
                case 'h':
                    return check_keyword(2, 3, "ort")
                case 'i':
                    match scanner.source[scanner.start + 2]:
                        case 'g':
                            return check_keyword(3, 3, "ned")
                        case 'z':
                            return check_keyword(3, 3, "eof")
                case 't':
                    match scanner.source[scanner.start + 2]:
                        case 'a':
                            return check_keyword(3, 3, "tic")
                        case 'r':
                            return check_keyword(3, 3, "uct")
                case 'w':
                    return check_keyword(2, 4, "itch")
        case 't':
            return check_keyword(1, 6, "ypedef")
        case 'u':
            match scanner.source[scanner.start + 1]:
                case 'n':
                    match scanner.source[scanner.start + 2]:
                        case 'i':
                            return check_keyword(3, 2, "on")
                        case 's':
                            return check_keyword(3, 5, "igned")
        case 'v':
            match scanner.source[scanner.start + 1]:
                case 'o':
                    match scanner.source[scanner.start + 2]:
                        case 'i':
                            return check_keyword(3, 1, "d")
                        case 'l':
                            return check_keyword(3, 5, "atile")
        case 'w':
            return check_keyword(1, 4, "hile")
    return variable()


def identifier():
    while is_alpha(peek()) or is_digit(peek()):
        advance()
    return make_token(identifier_type())


def number():
    dot = False
    while is_digit(peek()):
        advance()
    if peek() == '.' and not dot:
        dot = True
        advance()
        while is_digit(peek()):
            advance()
    return make_token(TokenType.TOKEN_LITERAL)


def regex_peek():
    if scanner.current >= len(scanner.source):
        return '\0'
    return scanner.source[scanner.current - 1::]


def regex_advance(span):
    scanner.current += span[1] - span[0] - 1


def match_operator():
    result = re.match(r'[-#+*/%|&><=!]+', regex_peek())
    if not result:
        return False
    regex_advance(result.span())
    return make_token(TokenType.TOKEN_OPERATOR)


def match_string():
    result = re.match(r'\".*\"', regex_peek())
    if not result:
        return False
    regex_advance(result.span())
    return make_token(TokenType.TOKEN_STRING)


def match_comment():
    result = re.match(r'//.*', regex_peek())
    if not result:
        return False
    regex_advance(result.span())
    return make_token(TokenType.TOKEN_COMMENT)


def match_paren():
    match peek():
        case '{':
            return make_token(TokenType.TOKEN_LEFT_PAREN)
        case '}':
            return make_token(TokenType.TOKEN_RIGHT_PAREN)


def regex():
    return match_comment() or match_operator() or match_string() or match_paren()


def scan_token() -> TokenType:
    skip_whitespace()
    scanner.start = scanner.current
    if is_at_end():
        return make_token(TokenType.TOKEN_EOF)

    char = advance()
    if is_alpha(char):
        return identifier()
    elif is_digit(char):
        return number()
    return regex()
