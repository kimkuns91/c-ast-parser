# 과제 2: C 코드 AST 생성 및 printf() 결과 계산

## 📌 과제 목표
1. C 소스 코드로부터 AST(Abstract Syntax Tree) 생성
   - Python을 사용해 C 코드의 AST를 생성
2. 생성한 AST 순회 및 출력 결과 계산
   - 생성된 AST를 순회하며 printf() 함수의 결과를 계산하고 출력

## 📝 해야 할 일

### 1. Python 프로그램 작성
- 프로그램은 명령행 인자로 C 코드 파일 경로를 받음
- pycparser 라이브러리를 사용해서 C 코드의 AST 생성
- AST는 반드시 `pycparser.c_ast.FileAST.show()` 형식으로 출력
- AST 출력 후, printf() 함수의 인자를 계산하여 "Computation Result: [값]" 형식으로 출력

#### 예시 C 코드
```c
int main() {
  int a = 2;
  int b = 3;
  int c = a + b;
  printf("%d", c);
  return 0;
}
```

#### 예시 출력
```
<AST 출력>
Computation Result: 5
```

### 2. 제약 조건

#### C 코드 관련 제약
- `int`, `float`, `double` 타입만 사용 가능
- 반복문 (`for`, `while`) 사용 금지
- 조건문 (`if`, `switch`) 사용 금지
- `printf()`만 존재, 한 번에 변수 하나만 출력
- escape sequence 사용 금지 (`\n`, `\t` 등)

#### 코드 작성 제약
- 외부 라이브러리 사용 금지 (단, pycparser는 허용)
- 코드에 충분한 주석 필수
- 표절, 코드 공유, Chat-GPT 사용 금지

### 3. 제출 양식
- **제출 파일**:
  - 코드: `{학번}_assignment2.py`
  - 보고서: `{학번}_report.pdf` (3페이지 이내로 코드 로직 설명)
- 두 파일을 하나의 zip 파일로 압축해서 제출

