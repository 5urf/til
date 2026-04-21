## 조건부 타입

>[!IMPORTANT]
>Conditional Types (조건부 타입)
>
>타입 시스템에서 `if/else`처럼 동작하는 타입 분기 로직이다.
>
>`SomeType extends OtherType ? TrueType : FalseType` 형태로 작성하며,
>
>왼쪽 타입이 오른쪽 타입에 할당 가능하면 TrueType, 아니면 FalseType이 된다.

- 단독으로는 유용성이 제한적이고, **제네릭과 함께 사용할 때 진짜 힘이 나온다**

```ts
type NameOrId<T extends number | string> = T extends number ? IdLabel : NameLabel;
// IdLabel | NameLabel

// 오버로드 3개 대신 단일 함수로 표현 가능
function createLabel<T extends number | string>(idOrName: T): NameOrId<T> { ... }

let a = createLabel("typescript"); // NameLabel
let b = createLabel(2.8); // IdLabel
let c = createLabel(Math.random() ? "hi" : 42); // NameLabel | IdLabel
```

---

## 조건부 타입 제약과 infer

>[!IMPORTANT]
>infer 키워드
>
>조건부 타입의 true 브랜치 안에서 `infer`로 새로운 타입 변수를 선언해 타입을 추출할 수 있다.
>
>구조를 직접 파고들지 않고 선언적으로 타입을 뽑아낼 수 있다.

```ts
// infer 없이 - 직접 인덱스 접근으로 추출
type Flatten<T> = T extends any[] ? T[number] : T;

// infer 사용 - 선언적으로 추출
type Flatten<Type> = Type extends Array<infer Item> ? Item: Type;
// string[] -> string, number -> number

// 함수 반환 타입 추출 패턴
type GetReturnType<Type> = Type extends (...args: never[]) => infer Return ? Return : never;

type Num = GetReturnType<() => number>; // number
type Str = GetReturnType<(x: string) => string>; // string
```

>[!TIP]
>유틸리티 타입 `ReturnType<T>`, `Parameters<T>`등이 내부적으로 `infer`로 구현되어 있다.
>
>직접 구현해보면 유틸리티 타입 동작 원리를 이해하는 데 도움이 된다.

---

## 분산 조건부 타입

>[!IMPORTANT]
>Distributive Conditional Types (분산 조건부 타입)
>
>제네릭에 유니온 타입을 넘기면 조건부 타입이 유니온의 각 멤버에 개별적으로 적용된다.

```ts
type ToArray<Type> = Type extends any ? Type[] : never;

type StrArrOrNumArr = ToArray<string | number>;
// string[] | number[] <- 분산 적용됨
// ToArray<string> | ToArray<number> 와 동일
```

>[!WARNING]
>분산을 원하지 않는 경우, `extends` 양쪽을 대괄호로 감싸면 분산을 막을 수 있다.

```ts
type ToArrayNonDist<Type> = [Type] extends [any] ? Type[] : never;

type ArrOfStrOrNum = ToArrayNonDist<string | number>;
// (string | number)[] <- 분산 없이 하나의 배열 타입
```
