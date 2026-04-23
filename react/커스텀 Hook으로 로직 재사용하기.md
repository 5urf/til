## 커스텀 Hook: 컴포넌트 간 로직 공유하기

>두 컴포넌트가 동일한 로직(예: 네트워크 온라인 상태 감지)을 공유해야 할 때,
>
>그 로직을 커스텀 훅으로 추출한다.
>
>컴포넌트 코드는 **how(구현)**가 아닌 **what(의도)**만 표현하게 된다.

```jsx
// 추출 전 - 두 컴포넌트에 동일한 useEffect 반복
function BookmarkStatus() {
  const [isOnline, setIsOnline] = useState(true);
  useEffect(() => {
    function handleOnline() { setIsOnline(true); }
    function handleOffline() { setIsOnline(false); }
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);
  // ...
}

// 추출 후 - 의도만 드러남
function BookmarkStatus() {
  const isOnline = useOnlineStatus();
  // ...
}
```

>[!IMPORTANT]
>React 애플리케이션은 컴포넌트로, 컴포넌트는 훅으로 만들어진다.
>
>커스텀 훅은 브라우저 API나 외부 시스템 처리 세부사항을 숨기고, 인터페이스만 노출한다.

---

## `use`네이밍 컨벤션

>훅 이름은 반드시 `use`로 시작해야 한다.
>
>이 규칙이 없으면 linter가 훅 규칙 위반을 감지할 수 없다.

- `use`로 시작하는 함수 -> React가 훅으로 인식 -> 훅 규칙(최상위 호출 등) 적용
- `use`로 시작하지 않는 함수 -> 훅 규칙 검사 안 함 -> 내부에서 훅 호출 시 버그 감지 불가

```jsx
// 나쁜 예 - linter가 훅 규칙 검사를 건너뜀
function getOnlineStatus() {
  return useOnlineStatus(); // 훅을 호출하고 있지만 감지 안 됨
}

// 좋은 예 - use로 시작하면 linter가 훅 규칙 검사 적용
function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(true);
  // ...
  return isOnline;
}
```

>[!WARNING]
>내부에서 훅을 호출하지 않더라도 이름을 `use`로 시작하게 지어도 된다.
>
>반대로 훅을 호출하는 함수가 `use`로 시작하지 않으면 규칙 위반이 발생해도 감지가 안 된다.

---

## state 저장 로직 공유

>커스텀 훅은 **state 자체**가 아니라 **state 저장 로직**을 공유한다.
>
>같은 훅을 두 컴포넌트에서 호출해도 state는 완전히 독립적이다.

```ts
function BookmarkList() {
  const isOnline = useOnlineStatus(); // 독립된 state
}

function CartBadge() {
  const isOnline = useOnlineStatus(); // 독립된 state - BookmarkList와 공유 안 됨
}
```

- 여러 컴포넌트 간에 **state 자체를 공유**해야 한다면 커스텀 훅이 아니라 **state 끌어올리기**로 해결한다.

>[!IMPORTANT]
>커스텀 훅 = 로직 재사용 / state 공유는 state 끌어올리기(lifting state up)로 해결한다.

---

## 반응형 값 전달

>커스텀 훅 간에 반응형 값(props,state)을 전달할 수 있다.
>
>컴포넌트가 리렌더링될 때마다 훅도 다시 실행되므로, 항상 최신 값을 받는다.

```tsx
function useChatRoom({ serverUrl, roomId }: { serverUrl: string; roomId: string }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
  }, [serverUrl, roomId])
}

function ChatRoom({ roomId }: { roomId: string }) {
  const [serverUrl, setServerUrl] = useState('https://localhost:1234');
  
  // serverUrl이 바뀌면 useChatRoom도 최신 값으로 다시 실행됨
  useChatRoom({ serverUrl, roomId });
}
```

>[!NOTE]
>커스텀 훅은 컴포넌트 본체의 일부처럼 동작한다.
>
>컴포넌트와 함께 리렌더링되기 때문에 항상 최신 props와 state를 받는다.

---

## 이벤트 핸들러 전달

>커스텀 훅이 이벤트 핸들러를 prop으로 받을 때,
>
>`useEffectEvent`로 감싸야 의존성 배열 문제를 피할 수 있다.

- Effect 안에서 외부로부터 받은 이벤트 핸들러를 직접 의존성으로 넣으면, 함수 참조가 매번 바뀌어 Effect가 불필요하게 재실행된다.

```tsx
function useChatRoom({
  serverUrl,
  roomId,
  onReceiveMessage, // 외부에서 받은 이벤트 핸들러
}: ChatOptions) {
  // onReceiveMessage를 Effect Event로 감싸 의존성에서 제외
  const onMessage = useEffectEvent(onReceiveMessage);
  
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.on('message', (msg) => onMessage(msg));
    connection.connect();
    return () => connection.disconnect();
  }, [serverUrl, roomId]); // onMessage는 의존성 배열에 없어도 됨
}
```

>[!WARNING]
>커스텀 훅이 받은 이벤트 핸들러를 Effect 의존성에 그냥 넣으면 무한 루프나 불필요한 재연결이 생긴다.
>
>`useEffectEvent`로 감싸서 반응형 값에서 분리해야 한다.

---

## 언제 커스텀 훅을 써야 하나

>모든 코드 중복에 커스텀 훅이 필요한 건 아니다.
>
>Effect가 필요할 때, 그 Effect를 커스텀 훅으로 감싸는 것이 맞다.

- 추출을 고려할 때
	- 같은 Effect 로직이 두 곳이상에 반복될 때
	- 복잡한 Effect를 단순한 인터페이스 뒤로 숨길 수 있을 때
	- 커스텀 훅 이름이 명확하게 떠오를 때 (이름이 안 떠오르면 아직 추출 시점이 아닐 수 있음)

- 추출하지 않아도 될 때
	- 단순한 `useEffect` 하나짜리 로직
	- 이름이 `useMount`, `useEffectOnce`같이 라이프사이클 관점에 머무를 때

```tsx
// 나쁜 추상화 - 라이프사이클 관점
function useMount(fn: () => void) {
  useEffect(() => { fn(); }, []); // React가 권장하지 않는 패턴
}

// 좋은 추상화 - 동기화 대상이 명확
function usePostAnalytics(postId: string) {
  useEffect(() => {
    logViewEvent(postId);
  }, [postId]);
}
```

>[!WARNING]
>`useMount`같은 훅은 만들지 말 것.
>
>React는 "마운트 시 1회 실행"이 아니라 "외부와의 동기화"를 기준으로 Effect를 설계한다.
>
>Strict Mode에서는 의도적으로 Effect를 두 번 실행해 버그를 찾는데, `useMount`는 이를 방해한다.

---

## 더 나은 패턴으로의 마이그레이션

>커스텀 훅 안에 Effect를 캡슐화하면, React 생태계가 발전할 때 컴포넌트를 건드리지 않고 내부 구현만 교체할 수 있다.

- 예를 들어 `useData`가 현재는 `useEffect + fetch`로 구현되어 있어도, 나중에 React의 데이터 페칭 메커니즘(Suspense 기반 등)으로 내부를 바꾸더라도 컴포넌트 코드는 그대로다.
```tsx
// 컴포넌트는 변경 없음
const post = useData(`/api/posts/${postId}`);

// useData 내부 구현만 교체
function useData(url: string) {
  // 현재: useEffect + fetch
  // 미래: React 공식 데이터 페칭 API로 교체 가능
}
```

>시간이 지나면 앱의 Effect 대부분은 커스텀 훅 안에 있게 된다.
>
>커스텀 훅을 쓰면 Effect를 직접 노출하지 않아도 되기 때문에, 컴포넌트는 데이터 흐름 의도에만 집중할 수 있다.

>[!TIP]
>커스텀 훅은 단순한 코드 재사용이 아니라 **추상화 경계**다.
>
>내부 구현이 바뀌어도 인터페이스가 유지되면 컴포넌트는 수정이 필요 없다.
