> TypeScript는 타입가드와 할당을 살펴보고, 선언된 타입보다 더 구체적인 타입으로 정제하는 과정을
> *narrowing*이라고 한다.

---
## `typeof`type guards

TypeScript에서 `typeof`가 반환하는 값을 검사하는 것은 type guard

```ts
function padLeft(padding: number | string, input: string): string {
  if (typeof padding === "number") {
    return " ".repeat(padding) + input;
  }
  return padding + input;
}
```

>[!WARNING]
>JS에서 `typeof null`은  `"object"` 이므로 주의하자.

## Truthiness narrowing

falsy 값 필터링에 사용

```ts
function printAll(strs: string | string[] | null) {
  if (strs && typeof strs === "object") {
    for (const s of strs) {
      console.log(s);
    }
  } else if (typeof strs === "string") {
    console.log(strs);
  }
}
```

>[!WARNING]
>원시값에 대한 truthiness 검사는 실수하기 쉽다.
>`""`(빈 문자열), `0`,`NaN`도 falsy라서 의도치 않은 케이스가 걸러질 수 있다.

```ts
// 빈 문자열을 놓치는 실수 예
if (strs) {
  // strs가 ""일때 이 블록 진입 안됨
}
```

## Equality narrowing

TypeScript는 `switch`문과 `===`, `!==`, `==`, `!=`같은 동등 비교 연산을 이용해 타입을 좁힌다.

```ts
function example(x: string | number, y: string | boolean) {
  if (x === y) {
    // `string`이 `x`와 `y` 모두가 가질 수 있는 유일한 공통 타입이므로
    // 이 안에서는 x, y에 'string' 메서드를 모두 사용할 수 있습니다.
    x.toUpperCase(); // (method) String.toUpperCase(): string
    y.toLowerCase(); // (method) String.toLowerCase(): string
  } else {
    console.log(x); // (parameter) x: string | number
    console.log(y); // (parameter) y: string | boolean
  }
}
```

`x === y`가 성립하면 TS는 두 타입이 같아야 한다고 판단해,

공통으로 가질 수 있는 타입(string)으로 좁혀준다.

## `in` operator narrowing

JS에는 객체나 프로토타입 체인에 특정 이름의 프로퍼티가 있는지 확인하는 `in`연산자가 있다

TS는 이것을 잠재적인 타입을 좁히는 방법으로 활용

```ts
type Fish = { swim: () => void };
type Bird = { fly: () => void };
type Human = { swim?: () => void; fly?: () => void };

function move(animal: Fish | Bird | Human) {
  if ("swim" in animal) {
    animal; // (parameter) animal: Fish | Human
  } else {
    animal; // (parameter) animal: Bird | Human
  }
}
```

optional 프로퍼티는 `in` 체크의 *양쪽(true/false)에 모두* 나타난다.

## `instanceof` narrowing

JS에는 값이 다른 값의 "인스턴스"인지 확인하는`instanceof`연산자가 있다

`instanceof`역시 type guard이며, TS는 `instanceof`로 보호된 분기에서 타입을 좁힌다.

```ts
function logValue(x: Date | string) {
  if (x instanceof Date) {
    console.log(x.toUTCString()); // (parameter) x: Date
  } else {
    console.log(x.toUpperCase()); // (parameter) x: string
  }
}
```

## Assignments

변수에 값을 할당할 때 TS는 오른쪽을 보고 왼쪽 타입을 적절히 좁힌다.

```ts
let x = Math.random() < 0.5 ? 10 : "hello world!";
// let x: string | number

x = 1;
console.log(x); // let x: number

x = "goodbye!";
console.log(x); // let x: string
```

>선언된 타입(string | number)은 고정이고, 각 지점에서 관찰되는 타입만 좁혀진다.

## Control flow analysis

도달 가능성(reachability)에 기반한 코드 분석을 *control flow analysis*라고 하며,

TS는 type guard와 할당을 만날 때마다 이 흐름 분석을 사용해 타입을 좁힌다.

변수를 분석할 때 control flow는 여러번 분기하고 합쳐질 수 있으며,

각 지점에서 변수가 다른 타입을 가지는 것으로 관찰 될 수 있다.

```ts
function example() {
  let x: string | number | boolean;

  x = Math.random() < 0.5;
  console.log(x); // let x: boolean

  if (Math.random() < 0.5) {
    x = "hello";
    console.log(x); // let x: string
  } else {
    x = 100;
    console.log(x); // let x: number
  }

  return x; // let x: string | number
}
```

## Using type predicates

사용자 정의 type guard를 정의하려면, 반환 타입이 *type predicate*인 함수를 정의하면 된다.

```ts
function isFish(pet: Fish | Bird): pet is Fish {
  return (pet as Fish).swim !== undefined;
}
```
>`pet is Fish`가 이 예제의 *type predicate*
>`parameterName is Type` 형태를 취하며
>`parameterName`은 현재 함수 시그니처의 파라미터 이름이어야 한다.

```ts
const fishOnly: Fish[] = zoo.filter(isFish); // Fish[]로 추론됨
```
### Assertion functions

타입은 [Assertion functions](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-7.html#assertion-functions)를 사용해 좁힐 수도 있다.

예기치 않은 상황이 발생했을 때 오류를 반환하는 특정 함수 집합.

이러한 함수를 어설션(assertion) 함수라고한다.

## Discriminated unions

```ts
interface Circle {
  kind: "circle";
  radius: number;
}

interface Square {
  kind: "square";
  sideLength: number;
}

type Shape = Circle | Square;


function getArea(shape: Shape) {
  if (shape.kind === "circle") {
    return Math.PI * shape.radius ** 2;
    // (parameter) shape: Circle
  }
}
```

유니온의 모든 타입이 리터럴 타입을 가진 공통 프로퍼티를 포함할 때,

TS는 이를 *discriminated union*으로 간주하고 유니온의 멤버를 좁혀낼 수 있다.

여기서 `kind`가 `Shape`의 *discriminant*프로퍼티

>[!TIPS]
>Discriminated union은
>네트워크를 통해 메시지를 주고 받을 때나,
>상태관리 프레임워크에서 `mutation`을 인코딩할 때와 같은 모든 종류의 메시징 체계를 표현하는데 적합

### `never`타입

타입을 좁히다 보면 유니온의 모든 가능성을 제거해서 아무것도 남지 않을 수 있다.

이련 경우 TS는 존재해서는 안되는 상태를 나타내기위해 `never`타입을 사용

## Exhaustiveness checking

`never`타입은 모든 타입에 할당 가능하지만,

`never`자체를 제외한 어떤 타입도 `never`에 할당할 수 없다.

즉, narrowing과 `never`를 활용해 `switch`문에서 *완전성 검사(exhaustive check)*를 할 수 있다.

```ts
interface Triangle {
  kind: "triangle";
  sideLength: number;
}

type Shape = Circle | Square | Triangle;

function getArea(shape: Shape) {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.sideLength ** 2;
    default:
      const _exhaustiveCheck: never = shape;
      // Error: Type 'Triangle' is not assignable to type 'never'.
      return _exhaustiveCheck;
  }
}
```
