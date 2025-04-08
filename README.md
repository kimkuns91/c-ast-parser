# C 코드 AST 파서 및 printf 계산기

이 프로젝트는 C 언어 코드를 파싱하여 추상 구문 트리(AST)를 생성하고, 코드 내의 printf() 함수 호출 결과를 계산하는 프로그램입니다.

## 개요

`2025_assignment2.py`는 다음과 같은 기능을 제공합니다:

1. C 코드 파일을 입력으로 받아 직접 구현된 렉서와 파서를 사용하여 파싱합니다.
2. 코드의 AST(Abstract Syntax Tree)를 생성하고 출력합니다.
3. 코드 내 변수 선언, 할당 및 연산을 시뮬레이션합니다.
4. printf() 함수 호출의 결과를 계산하고 출력합니다.

## 구현 세부사항

이 프로젝트는 어떠한 외부 라이브러리에도 의존하지 않고 순수 Python으로 직접 구현된 컴파일러 프론트엔드 구성요소를 포함합니다:

1. **렉서 (CLexer)**: C 코드를 문자 단위로 분석하여 토큰 스트림으로 변환합니다.
2. **파서 (CParser)**: 토큰 스트림을 AST로 변환합니다.
3. **평가기 (ASTEvaluator)**: AST를 순회하며 printf 결과를 계산합니다.

## 필요 조건

- Python 3.x
- 외부 라이브러리 필요 없음 (sys 모듈만 사용)

## 사용 방법

```bash
python 2025_assignment2.py <c_file_path>
```

- `<c_file_path>`: 분석할 C 코드 파일의 경로

## 작동 방식

### 1. 렉싱 (어휘 분석)

`CLexer` 클래스는 문자 단위로 C 코드를 분석하여 토큰으로 분류합니다:
- 키워드 (if, while, return 등)
- 식별자 (변수명, 함수명)
- 숫자 (정수 및 실수)
- 문자열 리터럴
- 연산자와 구두점
- 주석 및 공백은 무시됩니다

정규표현식을 사용하지 않고 문자별 순회 방식으로 토큰을 추출합니다.

### 2. 파싱 (구문 분석)

`CParser` 클래스는 재귀 하향 파싱 방식으로 토큰 스트림을 AST로 변환합니다:
- 함수 선언
- 변수 선언 및 초기화
- 복합 구문 (코드 블록)
- 표현식 (이항 연산, 함수 호출, 상수, 식별자 등)
- 반환 구문

### 3. 컴퓨테이션 모델

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

#### 이항 연산 처리 (`visit_BinaryOp`)
- 기본 산술 연산 (+, -, *, /)을 지원합니다.
- 비트 연산 (&, |, ^)을 지원합니다.
- C 언어의 타입 규칙에 따라 나눗셈 연산을 처리합니다.

### 4. 결과 출력

프로그램은 다음 정보를 출력합니다:
- 생성된 AST 구조
- 코드에서 발견된 모든 printf() 호출의 계산 결과

## 한계점 및 참고사항

1. 현재 버전은 다음 C 언어 기능을 지원합니다:
   - 기본 변수 선언 및 초기화
   - 산술 및 비트 연산
   - 단순한 printf() 호출 (`printf("%d", var)` 형태)
   - main() 함수 인식

2. 다음 기능은 현재 지원되지 않습니다:
   - 조건문 (if-else) 처리
   - 반복문 (for, while) 처리
   - 포인터 연산
   - 구조체 및 배열
   - 복잡한 함수 정의

3. 간단한 C 프로그램만 분석 가능하며, 완전한 C 문법을 지원하지 않습니다.

## 특별 구현 사항

이 프로젝트는 다음과 같은 특별한 제약사항으로 구현되었습니다:
- **순수 Python**: 외부 라이브러리 없이 구현
- **정규표현식 사용 없음**: re 모듈 대신 문자 단위 처리
- **최소 의존성**: Python 기본 라이브러리 중 sys 모듈만 사용

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
