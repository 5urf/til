## Props 전달하기의 문제점

>[!IMPORTANT]
>**Props Drilling**
>
>상위 컴포넌트의 데이터를 하위 컴포넌트까지 전달하기 위해 중간 컴포넌트들이 데이터를 그냥 통과시키는 구조.

>데이터가 필요한 컴포넌트의 공통 조상이 트리 상단에 있을 경우, props를 계단식으로 내려보내야 하는 상황이 발생한다.
>
>이를 Props Drilling이라 부른다.
>
>중간 컴포넌트들은 해당 데이터가 필요 없음에도 props를 받아 아래로 넘기는 역할만 하게 된다.

---

## Context: Props 전달하기의 대안

>Context는 부모가 트리 전체에 데이터를 제공할 수 있도록 한다.
>
>사용하는 컴포넌트는 트리 어디에 있든 가장 가까운 Provider의 값을 읽는다.

- Context 사용은 세 단계로 이루어진다:**생성 -> 사용 -> 제공**

---

## 1단계: Context 생성하기

>[!IMPORTANT]
>**createContext**
>
>Context 객체를 생성하는 함수. 인자로 기본값을 받는다.

```jsx
// LevelContext.js
import { createContext } from 'react';

export const LevelContext = createContext(1);
```

>[!IMPORTANT]
>`createContext(defaultValue)` - Provider가 없을 때 사용되는 기본값이다.
>
>`null`로 설정하지 않고 의미 있는 값을 넣으면 Provider 없이도 동작한다.

---
## 2단계: Context 사용하기

>[!IMPORTANT]
>**useContext** 
>
>가장 가까운 Provider의 값을 읽는 Hook.


```jsx
import { useContext } from 'react';
import { LevelContext } from './LevelContext.js';

export default function Heading({ children }) {
  const level = useContext(LevelContext);
  // ...
}
```

>[!WARNING]
>`useContext`는 다른 Hook과 마찬가지로 컴포넌트 최상위에서만 호출 가능하다.
>
>반복문이나 조건문 내부에서 호출하면 안된다.

>[!NOTE]
>`useContext`를 호출해도 Provider를 아직 제공하지 않으면 `createContext`의 기본값이 사용된다.

---

## 3단계: Context 제공하기

>[!IMPORTANT]
>**Context Provider** 
>
> `<Context value={...}>`로 자식 트리를 감싸 값을 공급하는 컴포넌트.

```jsx
import { LevelContext } from './LevelContext.js';

export default function Section({ level, children }) {
  return (
    <section className="section">
      <LevelContext value={level}>
        {children}
      </LevelContext>
    </section>
  );
}
```
- 컴포넌트는 위 트리에서 가장 가까운 `<LevelContext>`의 값을 읽는다.

>[!IMPORTANT]
>React 19부터 `<LevelContext.Provider value={...}>`대신 `<LevelContext value={...}>`로 축약된 문법을 사용한다.

---

## 같은 컴포넌트에서 Context를 사용하며 제공하기

>[!IMPORTANT]
>**Context 상속 패턴**
>
>컴포넌트가 상위 Context를 읽은 뒤, 가공한 값을 다시 하위에 제공하는 패턴.

```jsx
export default function Section({ children }) {
  const level = useContext(LevelContext);
  return (
    <section className="section">
      <LevelContext value={level + 1}>
        {children}
      </LevelContext>
    </section>
  );
}
```
- `Section`이 중첩될수록 자동으로 레벨이 증가한다.
- `level` prop을 명시적으로 전달할 필요가 없어진다.

>[!TIP]
>이 패턴은 다크모드 테마처럼 "깊이에 따라 누적되는" 값을 다룰 때 유용하다.

---

## Context를 사용하기 전에 고려할 것

>[!WARNING]
>Props를 여러 레벨 내려보내야 한다고 해서 무조건 Context가 정답은 아니다.

- Context 사용 전 먼저 시도할 것:
1. **Props 전달하기** - 데이터 흐름이 명확해 유지보수에 좋다.
2. **children으로 전달하기** - 데이터를 단순히 통과시키는 중간 컴포넌트가 있다면 `children`패턴으로 층수를 줄일 수 있다.

```jsx
// 개선 전
<Layout posts={posts} />

// 개선 후 - Layout은 posts를 몰라도 됨
<Layout>
  <Posts posts={posts} />
</Layout>
```

---

## Context 주요 사용 사례

>[!NOTE]
>Context는 정적인 값으로 제한되지 않는다.
>
>다음 렌더링에서 다른 값을 주면 React가 하위 컴포넌트를 모두 갱신한다.

- 테마 지정: 앱 최상단에 Provider를 두고 다크 모드 등 테마 값을 공급.
- 현재 로그인 계정: 트리 어디서나 유저 정보에 접근 가능.
- 라우팅: 대부분의 라우팅 솔루션이 내부적으로 Context를 사용해 현재 경로를 공유.
- 상태 관리: Reducer와 Context를 함께 사용해 복잡한 전역 state를 관리.

>[!TIP]
>`useReducer` + Context 조합은 규모가 있는 앱에서 전역상태를 관리하는 대표적인 패턴이다.
