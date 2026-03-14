## Keyof Type Operator

`keyof`는 객체 타입의 키를 union으로 추출
```ts
type Point = { x: number; y: number};
type P = keyof Point // "x" | "y"
```

string index signature가 있으면 `string | number` 반환
```ts
type Mapish = { [k: string]: boolean }
type M = keyof Mapish // string | number
// JS에서 obj[0] === obj["0"]이기 때문
```

>[!TIP]
>Mapped Types랑 조합할때 유용

---
## Typeof Type Operator

`typeof`는 타입 문맥에서 값의 타입을 참조한다
```ts
let s = "hello"
let n: typeof s // string
```

함수 반환 타입 추출할 때 유용
```ts
function f() {
  return { x: 10, y: 3}
}
type P = ReturnType<typeof f> // { x: number; y: number}
```

식별자/프로퍼티에만 사용 가능, 표현식은 불가
```ts
// ❌
type Age = typeof msgbox("계속할까요?")

// ✅
type Age = typeof s
```

> [!TIP]
> 함수 이름을 타입으로 쓰고 싶을 때 `ReturnType<typeof f>`패턴 자주 씀

---

## Indexed Access Types

`Type["key"]` 형태로 타입의 특정 프로퍼티 타입을 추출한다
```ts
type Person = { age: number; name: string; alive: boolean }
type Age = Person["age"] // number
```

union, keyof 조합 가능
```ts
type T1 = Person["age" | "name" ] // string | number
type T2 = Person[keyof Person] // string | number | boolean
```

인덱싱엔 반드시 타입 사용, `const` 변수 불가
```ts
const key = "age"
type Age = Person[key] // ❌

type key = "age"
type Age = Person[key] // ✅
```

>[!tip]
>API 응답 타입에서 특정 필드 타입만 뽑을 때 자주 씀

