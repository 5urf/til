## var 키워드로 선언한 변수의 문제점

>`var`의 3가지 문제
>ES5까지 유일한 변수 선언 방법이었던 `var`는 다른 언어와 구별되는 독특한 특징으로 인해
>심각한 문제를 발생시킬 수 있다.

- 변수 중복 선언 허용
	- 같은 스코프에서 같은 이름으로 다시 선언해도 에러 없음
	- 초기화문이 있으면 `var`키워드가 없는 것처럼 동작해 의도치 않은 값 변경 발생

- 함수 레벨 스코프
	- `var`는 오직 함수의 코드 블록만 지역 스코프로 인정
	- `if`,`for`등 블록 안에서 선언해도 전역 변수가 됨 -> 전역 변수 남발로 의도치 않은 중복 선언 발생

```js
var x = 1;
if (true) {
  var x = 10; // 전역 변수 x가 의도치 않게 재할당됨
}
console.log(x); // 10
```
>[!WARNING]
>`for`문의 반복 변수도 전역 변수가 된다.
>반복문 바깥에 같은 이름 변수가 있으면 반복문 이후 값이 덮어씌워짐

- 변수 호이스팅
	- 런타임 이전에 선언 단계와 초기화 단계가 한번에 진행됨
	- 선언문 이전에 참조해도 에러 없이 `undefined` 반환 -> 프로그램 흐름에 맞지 않고 가독성을 떨어뜨림

---

## let 키워드

>[!IMPORTANT]
>블록 레벨 스코프(block-level scope)
>`let`은 모든 코드 블록(함수, `if`, `for`, `while`, `try/catch`등)을 지역 스코프로 인정한다.

- 중복 선언 시 `SyntaxError`발생
- 블록 `{ }`안에서 선언한 변수는 블록 밖에서 참조 불가
- 함수도 코드 블록이므로 스코프를 만든다. 함수 내의 코드 블록은 함수 레벨 스코프에 중첩됨

```js
let foo = 1; // 전역 변수
{
  let foo = 2; // 지역 변수 - 전역 foo와 별개
  let bar = 3; // 지역 변수
}
console.log(foo); // 1
console.log(bar); // ReferenceError : bar is not defined
```

>[!IMPORTANT]
>**일시적 사각지대(TDZ, Temporal Dead Zone)**
>`let`은 선언 단계와 초기화 단계가 분리되어 진행된다.
>스코프의 시작 지점부터 초기화 단계 시작 지점(변수 선언문)까지 변수를 참조할 수 없는 구간을
>**일시적 사각지대(TDZ)**라 부른다.

```js
// 런타임 이전에 선언 단계 실행 - 아직 초기화 안 됨
console.log(foo); // ReferenceError: foo is not defined

let foo; // 변수 선언문에서 초기화 단계 실행
console.log(foo); // undefined

foo = 1; // 할당문에서 할당 단계 진행
console.log(foo); // 1
```

>[!WARNING]
>`let`도 호이스팅이 발생한다.
>아래 예제에서 호이스팅이 없다면 전역 변수 `foo`의 값 1을 출력해야 하지만,
>지역 `foo`가 호이스팅되어 TDZ에 빠지기 때문에 ReferenceError가 발생한다

```js
let foo = 1;
{
  console.log(foo); // ReferenceError: Cannot access 'foo' before initialization
  let foo = 2;
}
```

>[!NOTE]
>자바스크립트는 ES6에서 도입된 `let`, `const`를 포함해 모든 선언
>(`var`,`let`,`const`,`function`,`function*`,`class`등)을 호이스팅한다.
>단 `let`, `const`, `class`를 사용한 선언문은 호이스팅이 발생하지 않는 것처럼 동작한다.

- 전역 객체와 let
	- `var`전역 변수는 `window`의 프로퍼티가 됨
	- `let`전역 변수는 `window`의 프로퍼티가 아님 -> 보이지 않는 개념적인 블록(전역 렉시컬 환경의 선언적 환경 레코드)내에 존재

---

## const 키워드

>[!IMPORTANT]
>const
>`const`는 상수를 선언하기 위해 사용하지만 반드시 상수만을 위해 사용하지는 않는다.
>`let`과 대부분 동일하게 블록 레벨 스코프, TDZ가 적용된다.

- **선언과 동시에 초기화 필수** - 그렇지 않으면 `SyntaxError: Missing initializer in const declaration`
- **재할당 금지** - 재할당 시 `TypeError: Assignment to constant variable.`
- 상수 이름은 대문자 + 스네이크 케이스로 표기: - `const TAX_RATE = 0.1;`

>[!WARNING]
>`const`는 재할당을 금지할 뿐 "불변"을 의미하지 않는다.
>객체를 할당한 경우 프로퍼티의 동적 생성, 삭제, 값 변경은 가능하다.
>객체가 변경되더라도 변수에 할당된 참조 값은 변경되지 않는다.

```js
const person = { name: 'Lee' };
person.name = 'Kim'; // 재할당이 아닌 프로퍼티 변경 - OK
console.log(person); // {name: "Kim"};
```

---

## var vs let vs const

>[!IMPORTANT]
>변수 선언 권장 기준
>기본적으로 `const`를 사용하고,
>재할당이 필요한 경우에만 `let`을 사용한다.
>ES6부터는 `var`를 사용하지 않는다.

- ES6를 사용한다면 `var`는 사용하지 않는다
- 재할당이 필요한 경우에 한정해 `let`을 사용하고 스코프는 최대한 좁게 만든다
- 변경이 발생하지 않고 읽기 전용으로 사용하는 원시 값과 객체에는 `const`를 사용한다

>[!TIP]
>변수를 선언하는 시점에는 재할당이 필요할지 잘 모르는 경우가 많다.
>일단 `const`로 선언하고, 반드시 재할당이 필요하다면 그때 `let`으로 변경해도 결코 늦지 않다.


