from scanner import scanner, TokenType, scan_token


def create_html(tokens, source):
    html = "<html><head><style>"
    html += "span.reserved { color: red; }"
    html += "span.logical { color: purple; }"
    html += "span.literals { color: blue; }"
    html += "span.comments { color: gray; }"
    html += "span.strings { color: yellow; }"
    html += "span.functions { font-style: italic; }"
    html += "span.variables { font-weight: bold; }"
    html += "</style></head><body>"

    current_position = 0
    for token in tokens:
        html += source[current_position:token.start]
        if token.token_type == TokenType.TOKEN_COMMENT:
            html += f"<span class='comments'>{source[token.start:token.end]}</span>"
        elif token.token_type == TokenType.TOKEN_LITERAL:
            html += f"<span class='literals'>{source[token.start:token.end]}</span>"
        elif token.token_type == TokenType.TOKEN_STRING:
            html += f"<span class='strings'>{source[token.start:token.end]}</span>"
        elif token.token_type == TokenType.TOKEN_FUNCTION:
            html += f"<span class='functions'>{source[token.start:token.end]}</span>"
        elif token.token_type == TokenType.TOKEN_IDENTIFIER:
            html += f"<span class='variables'>{source[token.start:token.end]}</span>"
        elif token.token_type == TokenType.TOKEN_OPERATOR:
            if token.lexeme == '&&' or token.lexeme == '||':
                html += f"<span class='logical'>{source[token.start:token.end]}</span>"
            else:
                html += f"{source[token.start:token.end]}"
        elif token.token_type == TokenType.TOKEN_KEYWORD:
            html += f"<span class='reserved'>{source[token.start:token.end]}</span>"
        else:
            html += f"{source[token.start:token.end]}"
        current_position = token.end

    html += source[current_position:]
    html += "</body></html>"
    return html


def __main__():
    # read code.txt
    with open("code.txt", "r") as file:
        scanner.source = file.read()

    while not scanner.tokens or scanner.tokens[-1].token_type != TokenType.TOKEN_EOF:
        scan_token()
        if scanner.tokens[-1] == TokenType.TOKEN_EOF:
            break

    html_code = create_html(scanner.tokens, scanner.source)
    with open("highlighted_code.html", "w") as html_file:
        html_file.write(html_code)


__main__()
