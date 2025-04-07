#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2025_assignment2.py
C 코드의 AST를 생성하고 printf() 함수의 결과를 계산하는 프로그램
"""

import sys
from pycparser import parse_file, c_ast

class ASTEvaluator(c_ast.NodeVisitor):
    """AST를 순회하며 printf() 함수의 결과를 계산하는 클래스"""
    def __init__(self):
        self.env = {}  # 변수 저장소: {변수이름: 값}
        self.print_results = []  # printf 결과 저장
        self.var_types = {}  # 변수 타입 저장: {변수이름: 타입}

    def visit_Decl(self, node):
        """변수 선언 처리 (예: int a = 2;)"""
        if node.init is not None:
            var_name = node.name
            
            # 변수 타입 저장
            if hasattr(node.type, 'type') and hasattr(node.type.type, 'names'):
                self.var_types[var_name] = node.type.type.names[0]  # int, float, double 등
            
            if isinstance(node.init, c_ast.Constant):
                # 변수 타입에 따라 값 저장
                var_type = self.var_types.get(var_name)
                if var_type in ['float', 'double']:
                    # float나 double이면 소수점 처리
                    try:
                        self.env[var_name] = float(node.init.value)
                    except ValueError:
                        # 정수가 들어왔다면 float로 변환
                        self.env[var_name] = float(int(node.init.value))
                else:
                    # 정수형이면 int로 처리
                    self.env[var_name] = int(node.init.value)
            elif isinstance(node.init, c_ast.BinaryOp):
                value = self.eval_binary_op(node.init)
                var_type = self.var_types.get(var_name)
                # 결과 값을 변수 타입에 맞게 저장
                if var_type in ['float', 'double']:
                    self.env[var_name] = float(value)
                else:
                    self.env[var_name] = int(value) if isinstance(value, float) and value.is_integer() else value
            elif isinstance(node.init, c_ast.ID):
                self.env[var_name] = self.env.get(node.init.name, 0)

    def visit_Assignment(self, node):
        """대입 연산 처리 (예: a = b + c)"""
        var_name = node.lvalue.name
        
        if isinstance(node.rvalue, c_ast.BinaryOp):
            value = self.eval_binary_op(node.rvalue)
            var_type = self.var_types.get(var_name)
            # 결과 값을 변수 타입에 맞게 저장
            if var_type in ['float', 'double']:
                self.env[var_name] = float(value)
            else:
                self.env[var_name] = int(value) if isinstance(value, float) and value.is_integer() else value
        elif isinstance(node.rvalue, c_ast.Constant):
            var_type = self.var_types.get(var_name)
            if var_type in ['float', 'double']:
                try:
                    self.env[var_name] = float(node.rvalue.value)
                except ValueError:
                    self.env[var_name] = float(int(node.rvalue.value))
            else:
                self.env[var_name] = int(node.rvalue.value)
        elif isinstance(node.rvalue, c_ast.ID):
            self.env[var_name] = self.env.get(node.rvalue.name, 0)

    def visit_FuncCall(self, node):
        """printf() 함수 호출 처리"""
        if node.name.name == 'printf':
            args = node.args.exprs
            if len(args) >= 2 and isinstance(args[1], c_ast.ID):
                var_name = args[1].name
                value = self.env.get(var_name, 0)
                
                # 포맷 문자열에 따라 값 형식 조정
                if isinstance(args[0], c_ast.Constant) and args[0].value.startswith('"') and args[0].value.endswith('"'):
                    format_str = args[0].value.strip('"')
                    if '%d' in format_str:
                        # 정수 포맷이면 정수로 변환
                        value = int(value) if isinstance(value, float) and value.is_integer() else value
                    elif '%f' in format_str or '%lf' in format_str:
                        # 실수 포맷이면 실수로 유지
                        value = float(value)
                
                self.print_results.append(value)
        else:
            # 사용자 정의 함수는 결과에 영향을 미치지 않음
            pass
    def eval_binary_op(self, node):
        """이항 연산 처리 (예: a + b)"""
        left = self.eval_operand(node.left)
        right = self.eval_operand(node.right)
        op = node.op
        
        # 연산 수행
        if op == '+': return left + right
        if op == '-': return left - right
        if op == '*': return left * right
        if op == '/': 
            # 나눗셈 수행 (타입에 따라 다르게 처리)
            if isinstance(left, float) or isinstance(right, float):
                return float(left) / float(right)  # 적어도 하나가 float면 float 나눗셈
            else:
                # 정수 나눗셈이면 C 언어 규칙에 따라 처리 (Python과 다름)
                return int(left) // int(right)
        if op == '&': return int(left) & int(right)
        if op == '|': return int(left) | int(right)
        if op == '^': return int(left) ^ int(right)
        return 0

    def eval_operand(self, operand):
        """연산자 피연산자 평가"""
        if isinstance(operand, c_ast.Constant):
            if operand.type == 'int':
                return int(operand.value)
            elif operand.type in ['float', 'double']:
                return float(operand.value)
            else:
                # 타입 추론
                try:
                    if '.' in operand.value:
                        return float(operand.value)
                    else:
                        return int(operand.value)
                except ValueError:
                    return int(operand.value)
        elif isinstance(operand, c_ast.ID):
            return self.env.get(operand.name, 0)
        elif isinstance(operand, c_ast.BinaryOp):
            return self.eval_binary_op(operand)
        return 0

def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("Usage: python 2025_assignment2.py <c_file_path>")
        sys.exit(1)

    # C 파일 파싱 및 AST 생성
    try:
        ast = parse_file(sys.argv[1], use_cpp=True)
        
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
