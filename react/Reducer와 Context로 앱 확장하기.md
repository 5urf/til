>[!IMPORTANT]
>Reducer + Context 조합
>
>`useReducer`로 state를 관리해도 `tasks`와 `dispatch`는 선언된 컴포넌트에서만 사용 가능하다.
>
>하위 컴포넌트가 이를 필요로 할 때 props로 계속 내려보내야 하는 props drilling이 발생한다
>
>Reducer와 Context를 결합하면 트리 어디서든 state를 읽고 dispatch를 호출할 수 있다.

---

## 1단계: Context 두 개 생성

>[!IMPORTANT]
>state Context / dispatch Context 분리
>
>state와 dispatch는 역할이 달라서 각각 별도의 Context로 만든다.
>
>하나로 합치면 dispatch만 필요한 컴포넌트도 state 변경 시 불필요하게 리렌더링된다.

```tsx
// PostContext.ts
import { createContext } from 'react';

export const PostsContext = createContext(null);
export const PostsDispatchContext = createContext(null);
```

>[!IMPORTANT]
>Context를 두 개로 분리하는 이유는 성능 때문이다.
>
>state를 읽는 컴포넌트와 dispatch만 쓰는 컴포넌트가 각각 자신에게 필요한 Context만 구독하게 된다.

---

## 2단계: State와 dispatch를 Context에 넣기

- `useReducer`의 반환값인 `[state, dispatch]`를 각각의 Context Provider에 value로 전달한다.

```tsx
import { useReducer } from 'react';
import { PostsContext, PostsDispatchContext } from './PostContext';

export default function PostApp() {
  const [posts, dispatch] = useReducer(postsReducer, initialPosts);
  
  return (
    <PostsContext value={posts}>
      <PostsDispatchContext value={dispatch}>
        {/* 하위 트리 */}
      </PostsDispatchContext>
    </PostsContext>
  );
}
```

>[!NOTE]
>React19부터 `<Context.Provider value={...}>`대신 `<Context value={...}>`축약 문법을 사용한다.

---

## 3단계: 트리에서 Context 사용하기

>[!IMPORTANT]
>props 제거 / useContext로 직접 구독
>
>Context를 제공한 후에는 하위 컴포넌트가 props없이 `useContext`로 직접 state나 dispatch를 읽는다.
>
>부모 컴포넌트는 더 이상 이벤트 핸들러를 prop으로 넘기지 않아도 된다.

```tsx
// 읽기 전용 컴포넌트
function PostList() {
  const posts = useContext(PostsContext);
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>;
}

// 쓰기 전용 컴포넌트
function AddPost() {
  const dispatch = useContext(PostsDispatchContext);
  return (
    <button onClick={() => dispatch({ type: 'added', id: 4, title: '새 글' })}>
      추가
    </button>
  );
}
```

---

## 하나의 파일로 합치기

>[!IMPORTANT]
>Provider 컴포넌트 / 커스텀 Hook
>
>Context 생성, Reducer 로직, Provider 컴포넌트를 하나의 파일에 모아두면 컴포넌트들이 데이터 출처가 아닌 화면 표현에만 집중할 수 있다.
>
>커스텀 Hook을 함께 export하면 사용 방식도 추상화 된다.

```tsx
// PostContext.tsx
import { createContext, useContext, useReducer } from 'react';

export const PostsContext = createContext(null);
export const PostsDispatchContext = createContext(null);

export function PostsProvider({ children }) {
  const [posts, dispatch] = useReducer(postsReducer, initialPosts);
  return (
    <PostsContext value={posts}>
      <PostsDispatchContext value={dispatch}>
        {children}
      </PostsDispatchContext>
    </PostsContext>
  );
}

// 커스텀 Hook으로 추상화
export function usePosts() {
  return useContext(PostsContext);
}

export function usePostsDispatch() {
  return useContext(PostsDispatchContext);
}
```

```tsx
// App.tsx - 최상위가 깔끔해진다
export default function App() {
  return (
    <PostsProvider>
      <PostList />
      <AddPost />
    </PostsProvider>
  );
}
```

>[!IMPORTANT]
>`usePosts`, `usePostsDispatch`처럼 `use`로 시작하는 함수를 **커스텀 Hook**이라 한다.
>
>커스텀 Hook 내부에서 `useContext`등 다른 Hook을 자유롭게 사용할 수 있다.

>[!TIP]
>규모가 커질수록 이 패턴을 도메인 단위(auth, cart, modal등)로 반복 적용하게 된다.
>
>각 Context 파일이 Provider + 커스텀 Hook + Reducer를 모두 들고 있으면 도메인 로직이 한 곳에 모인다.

>[!WARNING]
>Context는 전역 state가 아니다.
>
>Provider가 감싸는 트리 범위 안에서만 유효하다.
>
>Provider 밖에서 `useContext`를 호출하면 `createContext`의 기본값(보통`null`)이 반환된다.
