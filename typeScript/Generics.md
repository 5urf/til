### 제네릭은 타입을 담는 변수다

> 단일 타입이 아닌 다양한 타입에서 작동하는 컴포넌트를 작성할 수 있다. 제네릭(`Type`)은 유저가 준 인수의 타입을 캡처하고, 이 정보를 나중에 사용할 수 있게 한다. `any`를 쓰는 것과는 다르다.

```ts
// ❌ any: 리턴 타입 정보 소실
function identity(arg: any): any { return arg; }

// ✅ generic: 입력 타입 = 출력 타입 보장
function identity<Type>(arg: Type): Type {
  return arg;
}

let output = identity<string>("myString"); // output: string
let output2 = identity("myString");        // output2: string (타입 인수 생략 가능 - 추론됨)
```

---

### 제네릭 타입 변수 작업

제네릭 함수 안에서 `Type`에 특정 프로퍼티가 있다고 가정하면 에러가 난다. `Type`은 어떤 타입이든 될 수 있기 때문이다.

```ts
function loggingIdentity<Type>(arg: Type): Type {
  console.log(arg.length); // ❌ Property 'length' does not exist on type 'Type'
  return arg;
}
```

`number`를 넘기면 `.length`가 없으므로 컴파일러가 막는다. `Type[]`로 바꾸면 배열이 보장되므로 `.length`에 접근할 수 있다.

```ts
function loggingIdentity<Type>(arg: Type[]): Type[] {
  console.log(arg.length); // ✅ 배열이므로 length 보장
  return arg;
}
```

---

### 제네릭 타입

제네릭 함수 타입은 비-제네릭 함수의 타입과 비슷하다. 타입 매개변수를 앞에 나열하는 형태다.

```ts
function identity<Type>(arg: Type): Type {
  return arg;
}

let myIdentity: <Type>(arg: Type) => Type = identity;
```

제네릭 타입 매개변수에 다른 이름을 사용할 수도 있다.

```ts
let myIdentity: <Input>(arg: Input) => Input = identity;
```

제네릭 타입을 객체 리터럴 타입의 함수 호출 시그니처로 작성할 수도 있다.

```ts
let myIdentity: { <Type>(arg: Type): Type } = identity;
```

이 형태에서 인터페이스로 옮기면 인터페이스의 다른 모든 멤버가 타입 매개변수를 볼 수 있다.

```ts
interface GenericIdentityFn<Type> {
  (arg: Type): Type;
}

let myIdentity: GenericIdentityFn<number> = identity; // 이 시점에 Type이 고정됨
```

---

### 제네릭 클래스

제네릭 클래스는 제네릭 인터페이스와 형태가 비슷하다. 클래스 이름 뒤에 `<>` 안에 제네릭 타입 매개변수 목록을 작성한다.

```ts
class Stack<Type> {
  private items: Type[] = [];

  push(item: Type): void {
    this.items.push(item);
  }

  pop(): Type | undefined {
    return this.items.pop();
  }
}

const numberStack = new Stack<number>();
numberStack.push(1);      // ✅
numberStack.push("hello"); // ❌ string은 number에 할당 불가
```

```ts
class Stack<Type> {
  static defaultItem: Type; // ❌ Static members cannot reference class type parameters.
}
```


> [!WARNING]
> 제네릭 클래스는 정적(static) 멤버에는 타입 매개변수를 사용할 수 없다.
> 정적 멤버는 클래스 인스턴스가 아닌 클래스 자체에 속하기 때문이다.

---

### 제네릭 제약조건

특정 프로퍼티가 있는 타입만 받고 싶을 때 `extends`로 제약을 건다.

```ts
function getLength<T extends { length: number }>(arg: T): number {
  return arg.length; // length가 보장되므로 안전하게 접근 가능
}

getLength("hello");     // ✅ string
getLength([1, 2, 3]);   // ✅ Array
getLength(42);          // ❌ number에는 length 없음
```

> [!WARNING]
> 제약에 맞는 객체 리터럴을 `T` 타입으로 직접 반환하면 에러가 난다.
> `T`는 그 제약을 만족하는 임의의 서브타입일 수 있기 때문에,
> 제약 형태와 일치한다고 해서 `T`로 취급되지 않는다.

```ts
function clamp<T extends { length: number }>(arg: T): T {
  return { length: 0 }; // ❌ '{ length: number }'는 'T'에 할당 불가
}
```

---

### 제네릭 남용 - 타입 파라미터가 한 곳에만 쓰인다면 필요 없다

- 타입 파라미터가 두 값 사이의 관계를 표현하지 않는다면 제네릭은 불필요하다.
- 불필요한 타입 파라미터는 추론을 방해하고 호출부를 복잡하게 만든다.

```ts
// ❌ T가 한 곳에만 등장 - 제네릭의 이유가 없음
function log<T>(arg: T): void { console.log(arg); }

// ✅ unknown으로 충분
function log(arg: unknown): void { console.log(arg); }
```

> [!TIP]
> 제네릭을 쓸 때는 "이 타입 파라미터가 최소 두 곳 이상에서 관계를 맺고 있는가"를 확인하면 된다.
