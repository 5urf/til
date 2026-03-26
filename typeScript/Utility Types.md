>일반 타입 변환을 쉽게 하기 위해 몇가지 유틸리티 타입을 제공
>전역으로 사용 가능

## Partial`<Type>`

모든 프로퍼티를 선택적(옵셔널)으로 타입을 생성

```ts
interface User {
  name: string;
  age: number;
}


function updateUser(user: User, fields: Partial<User>) {
  return { ...user, ...fields };
  // fields의 결과 타입: Partial<User>
}


const user1 = {
  name: "Lee",
  age: 29
};

const user2 = updateUser(todo1, {
  age: 31
});
```

## Required`<Type>`

>모든 프로퍼티를 필수로 설정한 타입을 생성
>Partial의 반대

```ts
interface Props {
  a?: number;
  b?: string;
}

const obj: Props = { a: 5 };

const obj2: Required<Props> = { a: 5 };
// Property 'b' is missing in type '{ a: number; }' but required in type 'Required<Props>'.
```

>[!TIP]
>`Partial<T>`와 `Required<T>`는 반대 방향의 같은 패턴이다
>`Partial`은 모든 프로퍼티를 선택적(`?`)으로 바꿔 업데이트 함수에 쓰기 좋고,
>`Required`는 반대로 전부 필수로 잠근다.
>PATCH API 처리할 때 `Partial<T>`을 파라미터 타입으로 쓰는 패턴이 자주 나온다.

---
## Readonly`<Type>`

>모든 프로퍼티를 읽기전용(readonly)으로 설정한 타입을 생성
>생성된 타입의 프로퍼티는 재할당할 수 없다.

```ts
interface Todo {
  title: string;
}

const todo: Readonly<Todo> = {
  title: "Delete inactive users",
};

todo.title = "Hello";

// Cannot assign to 'title' because it is a read-only property.
```

## Record`<Keys, Type>`

>`Type`의 프로퍼티 키의 집합으로 타입을 생성
>타입의 프로퍼티를 다른 타입에 매핑 시키는데 사용될 수 있다.
>enum 기반 객체 타입을 안전하게 정의하는 수단

```ts
interface PageInfo {
  title: string;
}

type Page = "home" | "about" | "contact";

const nav: Record<Page, PageInfo> = {
  about: { title: "about" },
  contact: { title: "contact" },
  home: { title: "home" },
};

nav.about; // const nav: Record<Page, PageInfo>
```


## Pick`<Type, Keys>`

`Type`에서 프로퍼티 `Keys`의 집합을 선택해 타입을 생성

```ts
interface Todo {
  title: string;
  description: string;
  completed: boolean;
}

type TodoPreview = Pick<Todo, "title" | "completed">;

const todo: TodoPreview = {
  title: "Clean room",
  completed: false,
};
```

## Omit`<Type, Keys>`

`Type`에서 모든 프로퍼티를 선택하고 키를 제거한 타입을 생성

```ts
interface Todo {
  title: string;
  description: string;
  completed: boolean;
}

type TodoPreview = Omit<Todo, "description">;

const todo: TodoPreview = {
  title: "Clean room",
  completed: false,
};
```

>[!TIP]
>`Pick`과 `Omit`은 방향만 다르다 - 많이 남길 땐 Omit, 적게 쓸 땐 Pick
>프로퍼티가 많은 타입에서 하나만 빼야 할 때 Pick으로 나머지를 다 나열하는 실수를 자주 한다.
>제거할 게 적으면 Omit이 맞다.

---

## Exclude`<Type, ExcludedUnion>`

`ExcludedUnion`에 할당할 수 있는 모든 유니온 멤버를 `Type`에서 제외하여 타입을 생성

```ts
type T0 = Exclude<"a" | "b" | "c", "a">; // type T0 = "b" | "c"

type T1 = Exclude<"a" | "b" | "c", "a" | "b">; // type T1 = "c"

type T2 = Exclude<string | number | (() => void), Function>; // type T2 = string | number
```

## Extract`<Type, Union>`

`Union`에 할당할 수 있는 모든 유니온 멤버를 `Type`에서 가져와서 타입을 생성

```ts
type T0 = Extract<"a" | "b" | "c", "a" | "f">; // type T0 = "a"

type T1 = Extract<string | number | (() => void), Function>; // type T1 = () => void
```

>[!TIP]
>`Exclude`와 `Extract`는 유니온 타입을 필터링한다 -헷갈리면 이름 뜻으로 기억
>Exclude = 빼내다(제거), Extract = 뽑아내다(교집합)
>`Omit`은 객체 키 제거, `Exclude`는 유니온 멤버 제거라는 구분도 중요하다.

---
## NonNullable`<Type>`

`Type`에서 `null`과 `정의되지 않은 것(undefined)`을 제외하고 타입을 생성

```ts
type T0 = NonNullable<string | number | undefined>; // type T0 = string | number

type T1 = NonNullable<string[] | null | undefined>; // type T1 = string[]
```

## Parameters`<Type>`

함수 타입 `Type`의 매개변수에 사용된 타입에서 튜플 타입을 생성

```ts
type T0 = Parameters<() => string>; // type T0 = []

type T1 = Parameters<(s: string) => void>; // type T1 = [s: string]

type T2 = Parameters<<T>(arg: T) => T>; // type T2 = [arg: unknown]

type T6 = Parameters<string>; // Type 'string' does not satisfy the constraint '(...args: any) => any'.
```

>[!TIP]
>`ReturnType`과 세트로 쓰인다. 외부 함수의 파라미터 타입을 재사용할 때
>`typeof`와 함께 쓰면 함수 시그니처 변경에 자동으로 따라간다.

## ReturnType`<Type>`

함수 `Type`의 반환 타입으로 구성된 타입을 생성

```ts
declare function f1(): { a: number; b: string };

type T0 = ReturnType<() => string>; // type T0 = string

type T1 = ReturnType<(s: string) => void>; // type T1 = void

type T2 = ReturnType<<T>() => T>; // type T2 = unknown

type T3 = ReturnType<<T extends U, U extends number[]>() => T>; // type T3 = number[]

type T4 = ReturnType<typeof f1>; // type T4 = { a: number; b: string; }
```

>[!TIP]
>외부 함수의 반환 타입을 그대로 쓸 수 있다
>라이브러리 함수나 팀 내 공통 함수의 반환 타입을 직접 선언하지 않아도 되기 때문에,
>타입이 변경될 때 자동으로 따라간다. `typeof`와 함께 쓰는 패턴을 반드시 숙지해야 한다.
