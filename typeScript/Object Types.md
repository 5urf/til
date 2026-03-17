> 객체 타입을 표현하는 방법은 세 가지, 속성을 제어하는 방법은 optional / readonly / index signature다.

---

## 객체 타입을 표현하는 세 가지 방법

```ts
// 익명 객체 타입 - 함수 파라미터에 인라인으로 작성
function greet(person: { name: string; age: number }) { ... }

// interface - 선언 병합(declaration merging) 가능
interface Person {
  name: string
  age: number
}

// type alias - 더 광범위한 타입 표현에 사용
type Person = {
  name: string
  age: number
}
```

| 기능             | `interface` | `type alias` |
| ---------------- | :---------: | :----------: |
| 선언 병합        |     ✅      |      ❌      |
| 유니온/교차 타입 |     ❌      |      ✅      |
| 확장 문법        |  `extends`  |     `&`      |

---

## optional 속성 - 읽으면 타입이 `T | undefined`가 된다

`?`를 붙인 속성은 TypeScript가 존재 자체를 보장하지 않기 때문에  
바로 사용하면 에러가 발생한다. narrowing이 필요하다.

```ts
interface PaintOptions {
  shape: Shape;
  xPos?: number; // number | undefined
  yPos?: number; // number | undefined
}

function paintShape(opts: PaintOptions) {
  opts.xPos.toFixed(); // ❌ 'number | undefined'
  const x = opts.xPos ?? 0; // ✅ nullish coalescing으로 좁히기
}
```

> [!TIP]
> `?.` 옵셔널 체이닝은 접근만 안전하게 할 뿐, 타입이 `T | undefined`라는 사실은 변하지 않는다.  
> 값을 사용해야 한다면 `??` 또는 `if` 체크로 narrowing해야 한다.

---

## readonly - 속성 재할당만 막고, 내부 구조는 막지 않는다

```ts
interface Home {
  readonly resident: { name: string; age: number };
}

function visitForBirthday(home: Home) {
  home.resident = { name: "Alice", age: 30 }; // ❌ 속성 재할당 불가
  home.resident.age++; // ✅ 내부 속성은 수정 가능
}
```

- **얕은(shallow) 불변성**만 보장한다
- 런타임에는 아무 영향이 없고, 타입 레벨의 제약이다
- 중첩 객체 내부까지 막으려면 내부 타입에도 `readonly`를 붙여야 한다

```ts
interface DeepReadonly {
  readonly resident: { readonly name: string; readonly age: number };
}
```

> [!WARNING]
> `readonly`를 붙였다고 "완전히 변경 불가"라고 착각하기 쉽다.  
> 참조 타입의 내부 값은 여전히 수정 가능하다.

---

## 인덱스 시그니처 - 키 이름을 모를 때 값의 타입을 지정한다

```ts
interface NumberDictionary {
  [index: string]: number;
  length: number; // ✅ 반환 타입(number)과 일치
  name: string; // ❌ 반환 타입 불일치 - 에러
}
```

인덱스 시그니처를 사용하면 **해당 타입이 가진 모든 속성은 시그니처의 반환 타입을 따라야** 한다.  
여러 타입을 허용하려면 유니온을 사용한다.

```ts
interface FlexibleDictionary {
  [index: string]: number | string;
  length: number; // ✅
  name: string; // ✅
}
```
