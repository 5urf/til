> 함수 타입을 표현하는 방법은 하나가 아니다.  
> 상황에 따라 타입 표현식 / 호출 시그니처 / 제네릭 / 오버로드를 구분해서 써야 한다.

---

## 함수 타입을 표현하는 세 가지 방법

| 방법              | 문법                                  | 사용 상황                      |
| ----------------- | ------------------------------------- | ------------------------------ |
| **타입 표현식**   | `(a: string) => void`                 | 가장 기본, 일반 함수 타입      |
| **호출 시그니처** | `{ (a: string): void; desc: string }` | 함수가 프로퍼티도 함께 가질 때 |
| **구성 시그니처** | `{ new(a: string): SomeClass }`       | `new`로 호출되는 생성자 함수   |

```ts
// 타입 표현식
type GreetFn = (name: string) => void;

// 호출 시그니처 - => 대신 : 사용
type DescribableFn = {
  description: string;
  (someArg: number): boolean; // 반환 타입을 : 로 표기
};

// 구성 시그니처
type SomeConstructor = {
  new (s: string): SomeObject;
};
```

---

## 제네릭 - 입출력 사이의 타입 관계를 표현하는 도구

"유연한 타입을 받는 방법"이 아니라 **입력과 출력 사이의 관계를 명시하는 것**이 목적이다.

```ts
// ❌ 타입 매개변수가 한 곳에만 등장 - 관계 표현 없음, unknown 쓰는 게 나음
function logValue<T>(val: T): void {
  console.log(val);
}

// ✅ 입력과 출력 사이의 관계가 있을 때 제네릭이 의미 있음
function firstElement<T>(arr: T[]): T | undefined {
  return arr[0];
}
```

잘 작성된 제네릭 체크리스트:

- 타입 매개변수를 **직접 사용(push down)** 하고 있는가
- 타입 매개변수가 **두 번 이상** 등장하는가
- 가능하면 **적게** 쓰고 있는가

> [!TIP]
> 타입 매개변수가 한 곳에만 등장한다면 제네릭을 쓸 이유가 없다.  
> `unknown` 또는 구체적인 타입으로 대체하는 게 더 명확하다.

---

## 함수 오버로드 - 구현 시그니처는 외부에서 보이지 않는다

```ts
function makeDate(timestamp: number): Date; // 오버로드 1
function makeDate(m: number, d: number, y: number): Date; // 오버로드 2
function makeDate(mOrTimestamp: number, d?: number, y?: number): Date {
  // 구현 시그니처 - 외부에서 직접 호출 불가
  if (d !== undefined && y !== undefined) {
    return new Date(y, mOrTimestamp, d);
  }
  return new Date(mOrTimestamp);
}

makeDate(12345678); // ✅ 오버로드 1
makeDate(5, 5, 5); // ✅ 오버로드 2
makeDate(1, 3); // ❌ 매칭되는 오버로드 시그니처 없음
```

`makeDate(1, 3)`이 에러나는 이유: 구현부에 `d?: number`가 있어 내부적으론 처리 가능하지만, **2개 인수와 매칭되는 오버로드 시그니처가 선언된 적 없기** 때문이다.  
2개 인수를 허용하려면 구현부가 아니라 **오버로드 시그니처를 추가**해야 한다.

> [!TIP]
> 입출력 관계가 타입에 따라 명확히 달라지는 경우가 아니라면 유니온 타입이 더 단순하다.  
> 오버로드보다 유니온으로 해결 가능한 경우가 많다.

---

## void, object, unknown, never

### void

`undefined`와 다르다. **타입 별칭**에서 `() => void`는 어떤 값을 반환해도 에러가 나지 않는다.

```ts
type VoidFunc = () => void;

const f1: VoidFunc = () => true; // ✅ 에러 없음
const f2: VoidFunc = () => {
  return true;
}; // ✅ 에러 없음
// forEach 콜백 타입이 () => void 이기 때문에 push 같은 값 반환 함수도 콜백으로 전달 가능
```

반면 **리터럴 함수 정의**에서 `void`를 명시하면 반환값이 있으면 에러다.

```ts
function f3(): void {
  return true; // ❌
}

const f4 = function (): void {
  return true; // ❌
};
```

> [!WARNING]
> 타입 별칭(`type F = () => void`)에 할당하는 경우와  
> 함수를 직접 정의(`function f(): void`)하는 경우의 동작이 다르다.

### object

원시값(`string`, `number`, `boolean`, `bigint`, `symbol`, `null`, `undefined`)이 아닌 모든 값.  
대문자 `Object`, 빈 객체 타입 `{}`과 다르다. 함수도 포함된다.

### unknown vs any

```ts
function processAny(val: any) {
  val.toUpperCase(); // ✅ 타입 검사 포기 - 런타임 에러 가능
}

function processUnknown(val: unknown) {
  val.toUpperCase(); // ❌ 타입 좁히기 전 접근 불가
  if (typeof val === "string") {
    val.toUpperCase(); // ✅
  }
}
```

`any`는 타입 검사를 **포기**, `unknown`은 타입 검사를 **강제**한다.

### never

절대 관찰될 수 없는 값의 타입. 항상 throw하거나 무한루프인 함수의 반환 타입,  
또는 유니온에서 모든 선택지가 소진됐을 때 등장한다.

```ts
function fail(msg: string): never {
  throw new Error(msg); // 반환 자체가 없음
}

function handleShape(shape: "circle" | "square") {
  if (shape === "circle") return;
  if (shape === "square") return;
  const _exhaustive: never = shape; // 모든 케이스 소진 확인용
}
```
