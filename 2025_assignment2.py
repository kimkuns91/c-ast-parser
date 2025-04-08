import sys
class CToken:
    """C 언어 토큰 클래스"""
    TYPE = 'TYPE'          # int, float, double, etc.
    IDENTIFIER = 'ID'      # 변수명
    NUMBER = 'NUMBER'      # 숫자 값
    STRING = 'STRING'      # 문자열
    OPERATOR = 'OPERATOR'  # +, -, *, /, =, etc.
    PUNCTUATION = 'PUNCT'  # {, }, (, ), ;, etc.
    KEYWORD = 'KEYWORD'    # if, while, return, etc.
    
    def __init__(self, type, value, line=0):
        self.type = type
        self.value = value
        self.line = line
    
    def __str__(self):
        return f"Token({self.type}, '{self.value}', line={self.line})"

class CLexer:
    """C 언어 렉서 클래스 (외부 라이브러리 없이 구현)"""
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.line = 1
        self.tokens = []
        self.current_char = None
        self.advance()
        
        # 키워드 및 타입 정의
        self.keywords = ['if', 'else', 'while', 'for', 'return', 'include', 'define']
        self.types = ['int', 'float', 'double', 'char', 'void']
        
    def advance(self):
        """다음 문자로 이동"""
        if self.position < len(self.code):
            self.current_char = self.code[self.position]
            self.position += 1
        else:
            self.current_char = None
            
    def peek(self, n=1):
        """현재 위치에서 n개 앞의 문자 확인"""
        peek_pos = self.position
        result = ''
        for _ in range(n):
            if peek_pos < len(self.code):
                result += self.code[peek_pos]
                peek_pos += 1
            else:
                break
        return result
    
    def is_space(self, char):
        """공백 문자인지 확인"""
        return char in ' \t\r'
    
    def is_newline(self, char):
        """줄바꿈 문자인지 확인"""
        return char == '\n'
    
    def is_digit(self, char):
        """숫자인지 확인"""
        return char and char.isdigit()
    
    def is_alpha(self, char):
        """알파벳 또는 언더스코어인지 확인"""
        return char and (char.isalpha() or char == '_')
    
    def is_alnum(self, char):
        """알파벳, 숫자 또는 언더스코어인지 확인"""
        return char and (char.isalnum() or char == '_')
        
    def skip_whitespace(self):
        """공백 건너뛰기"""
        while self.current_char and self.is_space(self.current_char):
            self.advance()
            
    def skip_newline(self):
        """줄바꿈 처리"""
        self.line += 1
        self.advance()
            
    def skip_comment(self):
        """주석 건너뛰기"""
        if self.current_char == '/' and self.peek() == '/':
            # 한 줄 주석
            self.advance()  # /
            self.advance()  # /
            while self.current_char and not self.is_newline(self.current_char):
                self.advance()
            if self.current_char:  # \n
                self.skip_newline()
        elif self.current_char == '/' and self.peek() == '*':
            # 여러 줄 주석
            self.advance()  # /
            self.advance()  # *
            while self.current_char:
                if self.current_char == '*' and self.peek() == '/':
                    self.advance()  # *
                    self.advance()  # /
                    break
                elif self.is_newline(self.current_char):
                    self.skip_newline()
                else:
                    self.advance()
    
    def skip_preprocessor(self):
        """전처리기 지시자 건너뛰기"""
        if self.current_char == '#':
            self.advance()  # #
            while self.current_char and not self.is_newline(self.current_char):
                self.advance()
            if self.current_char:  # \n
                self.skip_newline()
                
    def get_number(self):
        """숫자 토큰 가져오기"""
        result = ''
        is_float = False
        
        # 정수 부분
        while self.current_char and self.is_digit(self.current_char):
            result += self.current_char
            self.advance()
            
        # 소수점 및 소수 부분
        if self.current_char == '.':
            is_float = True
            result += self.current_char
            self.advance()
            
            while self.current_char and self.is_digit(self.current_char):
                result += self.current_char
                self.advance()
        
        if is_float:
            return CToken(CToken.NUMBER, float(result), self.line)
        else:
            return CToken(CToken.NUMBER, int(result), self.line)
            
    def get_identifier(self):
        """식별자 또는 키워드 토큰 가져오기"""
        result = ''
        
        while self.current_char and self.is_alnum(self.current_char):
            result += self.current_char
            self.advance()
            
        if result in self.keywords:
            return CToken(CToken.KEYWORD, result, self.line)
        elif result in self.types:
            return CToken(CToken.TYPE, result, self.line)
        else:
            return CToken(CToken.IDENTIFIER, result, self.line)
            
    def get_string(self):
        """문자열 토큰 가져오기"""
        result = ''
        self.advance()  # 첫 따옴표 건너뛰기
        
        while self.current_char and self.current_char != '"':
            if self.current_char == '\\':
                # 이스케이프 문자 처리
                self.advance()
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == '\\':
                    result += '\\'
                elif self.current_char == '"':
                    result += '"'
                else:
                    result += self.current_char
            else:
                result += self.current_char
            self.advance()
            
        self.advance()  # 마지막 따옴표 건너뛰기
        return CToken(CToken.STRING, result, self.line)
    
    def get_operator(self):
        """연산자 토큰 가져오기"""
        # 두 글자 연산자
        if self.current_char in ['=', '!', '<', '>'] and self.peek() == '=':
            op = self.current_char + self.peek()
            self.advance()
            self.advance()
            return CToken(CToken.OPERATOR, op, self.line)
        # 한 글자 연산자
        elif self.current_char in ['+', '-', '*', '/', '%', '=', '<', '>', '&', '|', '^', '!']:
            op = self.current_char
            self.advance()
            return CToken(CToken.OPERATOR, op, self.line)
        return None
        
    def tokenize(self):
        """코드를 토큰화"""
        while self.current_char:
            if self.is_space(self.current_char):
                self.skip_whitespace()
            elif self.is_newline(self.current_char):
                self.skip_newline()
            elif self.current_char == '/' and (self.peek() == '/' or self.peek() == '*'):
                self.skip_comment()
            elif self.current_char == '#':
                self.skip_preprocessor()
            elif self.is_digit(self.current_char):
                self.tokens.append(self.get_number())
            elif self.is_alpha(self.current_char):
                self.tokens.append(self.get_identifier())
            elif self.current_char == '"':
                self.tokens.append(self.get_string())
            elif self.current_char in ['+', '-', '*', '/', '%', '=', '<', '>', '!', '&', '|', '^']:
                op_token = self.get_operator()
                if op_token:
                    self.tokens.append(op_token)
            elif self.current_char in [';', ',', '(', ')', '{', '}', '[', ']']:
                self.tokens.append(CToken(CToken.PUNCTUATION, self.current_char, self.line))
                self.advance()
            else:
                # 인식할 수 없는 문자는 건너뛰기
                print(f"Warning: Unrecognized character '{self.current_char}' at line {self.line}")
                self.advance()
        
        return self.tokens

class ASTNode:
    """AST 노드 기본 클래스"""
    def __init__(self):
        pass
    
    def show(self, indent=0):
        """노드를 들여쓰기로 표시"""
        print(' ' * indent + str(self))

class Program(ASTNode):
    """프로그램 전체 노드"""
    def __init__(self, declarations=None):
        super().__init__()
        self.declarations = declarations or []
    
    def __str__(self):
        return f"Program"
    
    def show(self, indent=0):
        super().show(indent)
        for decl in self.declarations:
            decl.show(indent + 2)

class FunctionDecl(ASTNode):
    """함수 선언 노드"""
    def __init__(self, return_type, name, params, body):
        super().__init__()
        self.return_type = return_type
        self.name = name
        self.params = params or []
        self.body = body
    
    def __str__(self):
        return f"FunctionDecl: {self.return_type} {self.name}"
    
    def show(self, indent=0):
        super().show(indent)
        print(' ' * (indent + 2) + f"Params: {', '.join(str(p) for p in self.params)}")
        self.body.show(indent + 2)

class CompoundStmt(ASTNode):
    """복합 구문 노드 (블록)"""
    def __init__(self, block_items=None):
        super().__init__()
        self.block_items = block_items or []
    
    def __str__(self):
        return f"CompoundStmt"
    
    def show(self, indent=0):
        super().show(indent)
        for item in self.block_items:
            item.show(indent + 2)

class Decl(ASTNode):
    """변수 선언 노드"""
    def __init__(self, name, type_name, init=None):
        super().__init__()
        self.name = name
        self.type = type_name
        self.init = init
    
    def __str__(self):
        init_str = f" = {self.init}" if self.init else ""
        return f"Decl: {self.type} {self.name}{init_str}"
    
    def show(self, indent=0):
        super().show(indent)
        if self.init and isinstance(self.init, ASTNode):
            self.init.show(indent + 2)

class Constant(ASTNode):
    """상수 노드"""
    def __init__(self, type, value):
        super().__init__()
        self.type = type
        self.value = value
    
    def __str__(self):
        return f"Constant[{self.type}]: {self.value}"

class ID(ASTNode):
    """식별자 노드"""
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def __str__(self):
        return f"ID: {self.name}"

class BinaryOp(ASTNode):
    """이항 연산 노드"""
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right
    
    def __str__(self):
        return f"BinaryOp: {self.op}"
    
    def show(self, indent=0):
        super().show(indent)
        self.left.show(indent + 2)
        self.right.show(indent + 2)

class Assignment(ASTNode):
    """대입 연산 노드"""
    def __init__(self, op, lvalue, rvalue):
        super().__init__()
        self.op = op
        self.lvalue = lvalue
        self.rvalue = rvalue
    
    def __str__(self):
        return f"Assignment: {self.op}"
    
    def show(self, indent=0):
        super().show(indent)
        self.lvalue.show(indent + 2)
        self.rvalue.show(indent + 2)

class FuncCall(ASTNode):
    """함수 호출 노드"""
    def __init__(self, name, args=None):
        super().__init__()
        self.name = name
        self.args = args or []
    
    def __str__(self):
        return f"FuncCall: {self.name}"
    
    def show(self, indent=0):
        super().show(indent)
        for arg in self.args:
            arg.show(indent + 2)

class Return(ASTNode):
    """반환 구문 노드"""
    def __init__(self, expr=None):
        super().__init__()
        self.expr = expr
    
    def __str__(self):
        return f"Return"
    
    def show(self, indent=0):
        super().show(indent)
        if self.expr:
            self.expr.show(indent + 2)

class CParser:
    """C 언어 파서 클래스"""
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def peek(self):
        """현재 토큰 확인"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def consume(self):
        """토큰 소비"""
        token = self.peek()
        if token:
            self.pos += 1
        return token
    
    def match(self, token_type, value=None):
        """예상 토큰과 일치하는지 확인"""
        token = self.peek()
        if token and token.type == token_type and (value is None or token.value == value):
            return self.consume()
        return None
    
    def expect(self, token_type, value=None):
        """예상 토큰 소비, 없으면 오류"""
        token = self.match(token_type, value)
        if not token:
            current = self.peek()
            expected = f"{token_type}" + (f" '{value}'" if value else "")
            actual = f"{current.type} '{current.value}'" if current else "end of file"
            raise SyntaxError(f"Expected {expected}, found {actual} at line {current.line if current else 'EOF'}")
        return token
    
    def parse_program(self):
        """프로그램 파싱"""
        declarations = []
        
        while self.peek():
            # 함수 또는 변수 선언 파싱
            if self.match(CToken.TYPE) or self.match(CToken.KEYWORD, 'int') or self.match(CToken.KEYWORD, 'void'):
                self.pos -= 1  # 토큰 되돌리기
                declarations.append(self.parse_function_decl())
            else:
                # 다른 글로벌 선언
                self.consume()  # 일단 스킵
        
        return Program(declarations)
    
    def parse_function_decl(self):
        """함수 선언 파싱"""
        return_type = self.consume().value
        name_token = self.expect(CToken.IDENTIFIER)
        self.expect(CToken.PUNCTUATION, '(')
        params = []  # 매개변수 파싱 생략
        self.expect(CToken.PUNCTUATION, ')')
        
        body = self.parse_compound_stmt()
        return FunctionDecl(return_type, name_token.value, params, body)
    
    def parse_compound_stmt(self):
        """복합 구문 (블록) 파싱"""
        self.expect(CToken.PUNCTUATION, '{')
        block_items = []
        
        while not self.match(CToken.PUNCTUATION, '}'):
            if not self.peek():
                raise SyntaxError("Unexpected end of file while parsing compound statement")
            
            # 선언문 또는 구문 파싱
            if self.match(CToken.TYPE) or self.match(CToken.KEYWORD, 'int') or self.match(CToken.KEYWORD, 'float'):
                self.pos -= 1  # 토큰 되돌리기
                block_items.append(self.parse_declaration())
            else:
                block_items.append(self.parse_statement())
        
        return CompoundStmt(block_items)
    
    def parse_declaration(self):
        """변수 선언 파싱"""
        type_token = self.consume()
        name_token = self.expect(CToken.IDENTIFIER)
        init = None
        
        if self.match(CToken.OPERATOR, '='):
            init = self.parse_expression()
        
        self.expect(CToken.PUNCTUATION, ';')
        return Decl(name_token.value, type_token.value, init)
    
    def parse_statement(self):
        """구문 파싱"""
        if self.match(CToken.KEYWORD, 'return'):
            expr = None
            if not self.peek() or self.peek().value != ';':
                expr = self.parse_expression()
            self.expect(CToken.PUNCTUATION, ';')
            return Return(expr)
        else:
            # 식 구문
            expr = self.parse_expression()
            self.expect(CToken.PUNCTUATION, ';')
            return expr
    
    def parse_expression(self):
        """식 파싱"""
        return self.parse_assignment()
    
    def parse_assignment(self):
        """대입 식 파싱"""
        left = self.parse_binary_op()
        
        if self.match(CToken.OPERATOR, '='):
            right = self.parse_expression()
            return Assignment('=', left, right)
        
        return left
    
    def parse_binary_op(self, min_precedence=0):
        """이항 연산 식 파싱 (우선순위 고려)"""
        precedence = {
            '+': 1, '-': 1,
            '*': 2, '/': 2, '%': 2,
            '<': 0, '>': 0, '<=': 0, '>=': 0, '==': 0, '!=': 0,
            '&': 3, '|': 3, '^': 3
        }
        
        left = self.parse_primary()
        
        while True:
            token = self.peek()
            if not token or token.type != CToken.OPERATOR or token.value not in precedence or precedence[token.value] < min_precedence:
                break
            
            op = self.consume().value
            right = self.parse_binary_op(precedence[op] + 1)
            left = BinaryOp(op, left, right)
        
        return left
    
    def parse_primary(self):
        """기본 식 파싱"""
        token = self.peek()
        
        if self.match(CToken.NUMBER):
            return Constant('int' if isinstance(token.value, int) else 'float', token.value)
        
        if self.match(CToken.IDENTIFIER):
            if self.peek() and self.peek().value == '(':
                self.pos -= 1  # 토큰 되돌리기
                return self.parse_function_call()
            return ID(token.value)
        
        if self.match(CToken.STRING):
            return Constant('string', token.value)
        
        if self.match(CToken.PUNCTUATION, '('):
            expr = self.parse_expression()
            self.expect(CToken.PUNCTUATION, ')')
            return expr
        
        raise SyntaxError(f"Unexpected token {token} in expression")
    
    def parse_function_call(self):
        """함수 호출 파싱"""
        name_token = self.expect(CToken.IDENTIFIER)
        self.expect(CToken.PUNCTUATION, '(')
        args = []
        
        if not self.match(CToken.PUNCTUATION, ')'):
            args.append(self.parse_expression())
            
            while self.match(CToken.PUNCTUATION, ','):
                args.append(self.parse_expression())
            
            self.expect(CToken.PUNCTUATION, ')')
        
        return FuncCall(name_token.value, args)

class ASTEvaluator:
    """AST를 순회하며 printf() 함수의 결과를 계산하는 클래스"""
    def __init__(self):
        self.env = {}  # 변수 저장소: {변수이름: 값}
        self.print_results = []  # printf 결과 저장
        self.var_types = {}  # 변수 타입 저장: {변수이름: 타입}
    
    def visit(self, node):
        """노드 방문"""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """기본 방문 메소드"""
        print(f"No visit method for {type(node).__name__}")
    
    def visit_Program(self, node):
        """프로그램 노드 방문"""
        for decl in node.declarations:
            self.visit(decl)
    
    def visit_FunctionDecl(self, node):
        """함수 선언 노드 방문"""
        if node.name == 'main':
            self.visit(node.body)
    
    def visit_CompoundStmt(self, node):
        """복합 구문 노드 방문"""
        for item in node.block_items:
            self.visit(item)
    
    def visit_Decl(self, node):
        """변수 선언 노드 방문"""
        self.var_types[node.name] = node.type
        if node.init:
            value = self.visit(node.init)
            # 타입에 따라 값 변환
            if node.type in ['float', 'double']:
                self.env[node.name] = float(value)
            else:
                # 정수형으로 변환 (소수점이 없는 실수는 정수로)
                if isinstance(value, float) and value.is_integer():
                    self.env[node.name] = int(value)
                else:
                    self.env[node.name] = value
        else:
            # 초기값 없으면 기본값 0
            self.env[node.name] = 0
    
    def visit_Constant(self, node):
        """상수 노드 방문"""
        return node.value
    
    def visit_ID(self, node):
        """식별자 노드 방문"""
        return self.env.get(node.name, 0)
    
    def visit_BinaryOp(self, node):
        """이항 연산 노드 방문"""
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        # 연산 수행
        if node.op == '+': return left + right
        if node.op == '-': return left - right
        if node.op == '*': return left * right
        if node.op == '/':
            # 나눗셈 수행 (타입에 따라 다르게 처리)
            if isinstance(left, float) or isinstance(right, float):
                return float(left) / float(right)  # 적어도 하나가 float면 float 나눗셈
            else:
                # 정수 나눗셈이면 C 언어 규칙에 따라 처리 (Python과 다름)
                return int(left) // int(right)
        if node.op == '&': return int(left) & int(right)
        if node.op == '|': return int(left) | int(right)
        if node.op == '^': return int(left) ^ int(right)
        return 0
    
    def visit_Assignment(self, node):
        """대입 연산 노드 방문"""
        if isinstance(node.lvalue, ID):
            var_name = node.lvalue.name
            value = self.visit(node.rvalue)
            var_type = self.var_types.get(var_name)
            # 값을 변수 타입에 맞게 변환하여 저장
            if var_type in ['float', 'double']:
                self.env[var_name] = float(value)
            else:
                if isinstance(value, float) and value.is_integer():
                    self.env[var_name] = int(value)
                else:
                    self.env[var_name] = value
            return self.env[var_name]
        return 0
    
    def visit_FuncCall(self, node):
        """함수 호출 노드 방문"""
        if node.name == 'printf':
            args = node.args
            if len(args) >= 2 and isinstance(args[1], ID):
                var_name = args[1].name
                value = self.env.get(var_name, 0)
                
                # 포맷 문자열에 따라 값 형식 조정
                if isinstance(args[0], Constant) and args[0].type == 'string':
                    format_str = args[0].value
                    if '%d' in format_str:
                        # 정수 포맷이면 정수로 변환
                        if isinstance(value, float) and value.is_integer():
                            value = int(value)
                    elif '%f' in format_str or '%lf' in format_str:
                        # 실수 포맷이면 실수로 유지
                        value = float(value)
                
                self.print_results.append(value)
                return value
        return 0
    
    def visit_Return(self, node):
        """반환 구문 노드 방문"""
        if node.expr:
            return self.visit(node.expr)
        return 0

def parse_c_file(filepath):
    """C 파일 파싱"""
    with open(filepath, 'r') as f:
        code = f.read()
    
    # 렉싱
    lexer = CLexer(code)
    tokens = lexer.tokenize()
    
    # 파싱
    parser = CParser(tokens)
    ast = parser.parse_program()
    
    return ast

def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("Usage: python 2025_assignment2.py <c_file_path>")
        sys.exit(1)

    # C 파일 파싱 및 AST 생성
    try:
        ast = parse_c_file(sys.argv[1])
        
        # AST 출력
        ast.show()
        
        # AST 평가 및 printf() 결과 계산
        evaluator = ASTEvaluator()
        evaluator.visit(ast)
        
        # 모든 printf 결과 출력
        for result in evaluator.print_results:
            print(f'Computation Result: {result}')
    except Exception as e:
        print(f"Error: {e}")
        # 디버깅 정보 출력
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
