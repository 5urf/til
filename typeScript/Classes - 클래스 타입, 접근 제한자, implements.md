## 클래스 필드 타입 선언

>[!IMPORTANT]
>클래스 필드는 타입 어노테이션 또는 초기값으로 타입을 선언한다.
>
>초기값이 있으면 TS가 타입을 추론하고, 없으면 `any`로 추론된다.

```ts
class Post {
  title: string; // 타입 명시 (constructor에서 초기화 필요)
  views = 0; // 초기값 -> number로 추론
  content!: string; // ! : 나중에 반드시 할당됨을 명시 (definite assignment)
}
```

>[!WARNING]
>`strictPropertyInitialization`이 활성화된 상태에서 필드를 constructor 외부에서 초기화하면 에러가 발생한다.
>
>외부 라이브러리 등으로 초기화되는 경우 `!`(definite assignment assertion)를 사용한다.

- `readonly`: constructor 외부에서 재할당 불가.
```ts
class Post {
  readonly id: number;
  constructor(id: number) {
    this.id = id; // OK - constructor 내부는 가능
  }
}
```

---

## 접근 제한자 (public / protected / private)

>[!IMPORTANT]
>클래스 멤버의 외부 접근 범위를 제어하는 키워드.

| 제한자           | 클래스 내부 | 서브클래스 | 외부  |
| ------------- | ------ | ----- | --- |
| `public`(기본값) | ✅      | ✅     | ✅   |
| `protected`   | ✅      | ✅     | ❌   |
| `private`     | ✅      | ❌     | ❌   |

```ts
class User {
  public name: string; // 어디서나 접근 가능
  protected role: string; // 서브클래스까지 접근 가능
  private password: string; // 이 클래스 내부에서만 접근 가능
  
  constructor(name: string, role: string, password: string) {
    this.name = name;
    this.role = role;
    this.password = password;
  }
}
```

>[!WARNING]
>TS의 `private`은 **타입 검사 시에만** 강제된다 (soft private).
>
>JS 런타임에서는 `obj["password"]`나 `console.log`로 접근 가능하다.
>
>런타임까지 완전히 숨기려면 JS의 `#` private field를 사용해야 한다 (hard private).

```ts
class User {
  #password = "secret"; // JS private field - 런타임에도 외부 접근 불가
}
```

- **Parameter Properties**: constructor 파라미터에 접근 제한자를 붙이면 필드 선언 + 할당을 한 번에 처리한다.

```ts
class Post {
  constructor(
    public title: string,
    private authorId: number,
    readonly createdAt: Date
  ) {} // body 불필요
}
```

---

## implements

>[!IMPORTANT]
>`implements`는 클래스가 특정 인터페이스를 만족하는지 **타입 검사**만 수행한다.
>
>클래스 자체의 타입이나 메서드 타입을 변경하지 않는다.

```ts
interface Publishable {
  publish(): void;
  title: string;
}

class Post implements Publishable {
  title: string;
  constructor(title: string) {
    this.title = title;
  }
  publish() {
    console.log(`${this.title} published`);
  }
}
```

- 여러 인터페이스를 동시에 구현할 수 있다: `class C implements A, B { ... }`

>[!WARNING]
>`implements`가 파라미터 타입을 자동으로 추론해주지 않는다.
>
>인터페이스에 `check(name: string): boolean`이 있어도, 구현 메서드의 파라미터는 따로 타입을 명시해야 한다.
>
>명시하지 않으면 `any`로 추론된다.

>[!WARNING]
>인터페이스에 optional 프로퍼티(`y?: number`)가 있어도 구현 클래스에 자동으로 생기지 않는다.
>
>클래스에 직접 선언하지 않으면 접근 시 에러가 발생한다.

---

## extends (상속)

>[!IMPORTANT]
>`extends`로 베이스 클래스의 모든 프로퍼티와 메서드를 상속받는다.
>
>TS는 서브클래스가 항상 베이스 클래스의 서브타입임을 강제한다.

```ts
class Animal {
  move() { console.log("moving"); }
}

class Dog extends Animal {
  bark() { console.log("woof"); }
}
```

- 메서드 오버라이드 시, 서브클래스의 시그니처는 베이스 클래스와 호환되어야 한다.
- 베이스에서 선택적 파라미터인 것을 서브에서 필수로 바꾸면 에러가 발생한다.

>[!WARNING]
>constructor에서 `this`에 접근하기 전에 반드시 `super()`를 먼저 호출해야 한다.

---

## abstract 클래스

>[!IMPORTANT]
>직접 인스턴스화할 수 없고, 서브클래스의 베이스 역할만 한다.
>
>abstract 멤버는 구현 없이 시그니처만 선언하고, 서브클래스에서 반드시 구현해야 한다.

```ts
abstract class Feed {
  abstract getTitle(): string; // 서브클래스에서 구현 필요
  
  display() {
    console.log(this.getTitle()); // 공통 로직
  }
}

class PostFeed extends Feed {
  getTitle() { return "오늘의 포스트"; }
}

new Feed(); // Error: Cannot create an instance of an abstract class
new PostFeed(); // OK
```

>[!TIP]
>`implements`는 인터페이스 계약 준수 여부만 검사하고,
>
>`abstract`는 공통 구현 로직을 공유하면서 일부 동작을 서브클래스에 위임할 때 사용한다.

---

## 클래스의 구조적 타입 검사

>[!NOTE]
>TS는 클래스를 구조적으로 비교한다.
>
>명시적 상속 관계가 없어도 같은 구조면 호환된다.

```ts
class Point1 { x = 0; y = 0; }
class Point2 { x = 0; y = 0; }

const p: Point1 = new Point2(); // OK - 구조가 동일
```
