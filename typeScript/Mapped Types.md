## Mapped Types 기본

>[!IMPORTANT]
>Mapped Types (매핑된 타입)
>`keyof`로 생성한 키의 조합을 순회하여 기존 타입을 기반으로 새로운 타입을 만드는 제네릭 타입이다.
>중복 없이 타입을 변환할 수 있다.

```ts
type OptionsFlags<Type> = {
  [Property in keyof Type]: boolean;
  // Type의 모든 프로퍼티를 순회해 값을 boolean으로 변환
};

type FeatureFlags = {
  darkMode: () => void;
  newUserProfile: () => void;
};

type FeatureOptions = OptionsFlags<FeatureFlags>;
// { darkMode: boolean; newUserProfile: boolean }
```

---

## Mapping Modifiers

>[!IMPORTANT]
>Mapping Modifiers(`-readonly`,`-?`)
>매핑 중 `readonly`와 `?`를 추가하거나 제거할 수 있다.
>`-`접두사로 제거, `+`접두사(기본값)로 추가한다.

```ts
// readonly 제거
type CreateMutable<Type> = {
  -readonly [Property in keyof Type]: Type[Property];
};

type LockedAccount = { readonly id: string; readonly name: string};
type UnlockedAccount = CreateMutable<LockedAccount>;
// { id: string; name: string }
```

```ts
// optional 제거
type Concrete<Type> = {
 [Property in keyof Type]-?: Type[Property];
};

type MaybeUser = { id: string; name?: string; age?: number };
type User = Concrete<MaybeUser>;
// { id: string; name: string; age: number }
```

>[!TIP]
>유틸리티 타입 `Required<T>`와`Readonly<T>`가 내부적으로 이 방식으로 구현되어 있다.
>직접 구현해보면 유틸리티 타입 동작 원리를 이해하는 데 도움이 된다.

---

## Key Remapping (as)

>[!IMPORTANT]
>Key Remapping via `as`
>TypeScript 4.1 이상에서 `as`절로 매핑된 타입의 키 이름을 변환할 수 있다.
>템플릿 리터럴 타입과 조합해 새로운 키 이름을 생성하는 것이 대표적인 패턴이다.

```ts
type Getters<Type> = {
  [Property in keyof Type as `get${Capitalize<string & Property>}`]: () => Type[Property];
};

interface Person { name: string; age: number; location: string }

type LazyPerson = Getters<Person>;
// { getName: () => string; getAge: () => number; getLocation: () => string }
```

조건부 타입과 결합해 특정 키를 필터링하는 것도 가능하다.

```ts
// 'kind' 프로퍼티 제거
type RemoveKindField<Type> = {
  [Property in keyof Type as Exclude<Property, "kind">]: Type[Property];
};

interface Circle { kind: "circle"; radius: number }
type KindlessCircle = RemoveKindField<Circle>;
// { radius: number }
```

>[!NOTE]
>Mapped Types는 조건부 타입, 템플릿 리터럴 타입 등 다른 타입 조작 기능과 조합해 더 강력하게 활용할 수 있다.
>예: 특정 프로퍼티가 `{ pii: true }`를 가지는지 여부에 따라 `true | false`를 반환하는 타입 등
