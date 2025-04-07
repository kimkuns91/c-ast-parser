# C 코드 AST 파서 및 printf 계산기

이 프로젝트는 C 언어 코드를 파싱하여 추상 구문 트리(AST)를 생성하고, 코드 내의 printf() 함수 호출 결과를 계산하는 프로그램입니다.

## 개요

`2025_assignment2.py`는 다음과 같은 기능을 제공합니다:

1. C 코드 파일을 입력으로 받아 파싱합니다.
2. 코드의 AST(Abstract Syntax Tree)를 생성하고 출력합니다.
3. 코드 내 변수 선언, 할당 및 연산을 시뮬레이션합니다.
4. printf() 함수 호출의 결과를 계산하고 출력합니다.

## 필요 조건

- Python 3.x
- pycparser 라이브러리 (C 코드 파싱을 위해 필요)

## 사용 방법

```bash
python 2025_assignment2.py <c_file_path>
```

- `<c_file_path>`: 분석할 C 코드 파일의 경로

## 작동 방식

### 1. AST 생성

프로그램은 pycparser를 사용하여 C 코드 파일을 파싱하고 AST를 생성합니다. AST는 코드의 구문 구조를 트리 형태로 표현한 것입니다.

### 2. 컴퓨테이션 모델

`ASTEvaluator` 클래스는 AST를 순회하며 다음과 같은 C 코드 요소를 처리합니다:

#### 변수 선언 및 초기화 (`visit_Decl`)
- 변수 타입(int, float, double 등)을 추적합니다.
- 초기값을 변수 타입에 맞게 저장합니다.
- 상수, 이항 연산식, 다른 변수를 통한 초기화를 지원합니다.

#### 변수 할당 (`visit_Assignment`)
- 대입 연산을 처리합니다 (예: a = b + c).
- 상수, 이항 연산식, 다른 변수를 통한 할당을 지원합니다.
- 변수 타입에 맞게 값을 변환하여 저장합니다.

#### 함수 호출 처리 (`visit_FuncCall`)
- printf() 함수 호출을 인식합니다.
- 포맷 문자열(%d, %f, %lf)에 따라 출력 값의 형식을 조정합니다.
- 각 printf() 호출의 결과를 수집합니다.

#### 이항 연산 처리 (`eval_binary_op`)
- 기본 산술 연산 (+, -, *, /)을 지원합니다.
- 비트 연산 (&, |, ^)을 지원합니다.
- C 언어의 타입 규칙에 따라 나눗셈 연산을 처리합니다.

#### 피연산자 평가 (`eval_operand`)
- 상수, 변수, 중첩된 이항 연산을 평가합니다.
- 타입에 따라 적절한 값으로 변환합니다.

### 3. 결과 출력

프로그램은 다음 정보를 출력합니다:
- 생성된 AST 구조
- 코드에서 발견된 모든 printf() 호출의 계산 결과

## 한계점 및 참고사항

1. 현재 버전은 다음 C 언어 기능을 지원합니다:
   - 기본 변수 선언 및 초기화
   - 산술 및 비트 연산
   - 단순한 printf() 호출 (`printf("%d", var)` 형태)

2. 다음 기능은 현재 지원되지 않습니다:
   - 조건문 (if-else)
   - 반복문 (for, while)
   - 복잡한 포인터 연산
   - 구조체 및 배열
   - 함수 정의 및 호출 (printf 외)

3. printf() 함수는 단순한 형태(`printf(format, var)`)만 지원하며, 복잡한 형식 지정자나 여러 변수를 사용한 호출은 제한적으로 지원합니다.

## 예제

```c
// sample.c
#include <stdio.h>

int main() {
    int a = 5;
    int b = 10;
    int c = a + b;
    printf("%d", c);
    return 0;
}
```

실행:
```bash
python 2025_assignment2.py test.c
```

출력:
```
[AST 출력 내용]
Computation Result: 5
Computation Result: -1
Computation Result: 6
Computation Result: 1.5
```
