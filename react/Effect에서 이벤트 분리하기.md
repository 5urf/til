## 이벤트 핸들러 vs Effect 선택 기준

>[!IMPORTANT]
>이벤트 핸들러 vs Effect
>"해당 코드가 실행되어야 하는 이유"로 구분한다.
>특정 상호작용(버튼 클릭 등)에 대한 응답 -> 이벤트 핸들러
>동기화 유지가 목적 -> Effect

- **이벤트 핸들러**: 사용자가 같은 상호작용을 반복하지 않는 한 재실행되지 않음. "수동으로"트리거 됨
- **Effect**: 읽은 반응형 값이 마지막 렌더링 때와 다르면 다시 동기화. "자동으로트리거 됨

---

## 반응형 값과 반응형 로직

>[!IMPORTANT]
>반응형(Reactive) / 비반응형
>컴포넌트 본문 내부에 선언된 props, state, 변수는 모두 **반응형 값**이다.
>이벤트 핸들러와 Effect는 반응형 값의 변화에 다르게 반응한다.

- **이벤트 핸들러 내부 로직**: 반응형이 아님. 반응형 값이 변경되어도 재실행되지 않음
- **Effect 내부 로직**: 반응형. 읽는 반응형 값이 바뀌면 React가 새 값으로 Effect를 다시 실행

```jsx
// 이벤트 핸들러 - message가 바뀐다고 재실행되지 않음
function handleSendClick() {
  sendMessage(message); // 클릭할 때만 실행
}

// Effect - roomId가 바뀌면 재동기화
useEffect(() => {
  const connection = createConnection(serverUrl, roomId);
  connection.connect();
  return () => connection.disconnect();
}, [roomId]);
```

---

## useEffectEvent - 비반응형 로직 추출

>[!IMPORTANT]
>useEffectEvent / Effect 이벤트
>Effect 내부에 반응형이어서는 안 되는 로직이 있을 때  `useEffectEvent`로 추출한다.
>Effect 이벤트 내부 로직은 반응형이 아니며 항상 props/state의 **최근 값**을 읽는다.

```jsx
// 문제: theme이 바뀔 때마다 채팅이 재연결됨
useEffect(() => {
  const connection = createConnection(serverUrl, roomId);
  connection.on('connected', () => {
    showNotification('연결됨!', theme); // theme도 의존성이 되어버림
  })
  connection.connect();
  return () => connection.disconnect();
}, [roomId, theme]); // theme 변경 시 불필요한 재연결 발생
```

```jsx
// 해결: useEffectEvent로 비반응형 로직 분리
const onConnected = useEffectEvent(() => {
  showNotification('연결됨!', theme); // 항상 최신 theme를 읽음
});

useEffect(() => {
  const connection = createConnection(serverUrl, roomId);
  connection.on('connected', () => {
    onConnected(); // Effect 이벤트 호출
  })
  connection.connect();
  return () => connection.disconnect();
}, [roomId]); // theme 제거 - onConnected는 의존성에 추가하지 않음
```

>[!IMPORTANT]
>Effect 이벤트는 반응형이 아니므로 의존성 배열에서 제외해야 한다.
>Effect 이벤트는 Effect의 반응성과 반응형이어서는 안 되는 코드 사이의 "연결을 끊어준다".

>[!WARNING]
>Effect 이벤트 사용 제한 2가지:
>1. **Effect 내부에서만 호출**할 것
>2. **다른 컴포넌트나 Hook에 전달하지 말 것** - 자신을 사용하는 Effect 바로 근처에 선언해야 함

---
## Effect 이벤트로 최근 props/state 읽기

>[!IMPORTANT]
>최근 값 읽기 패턴
>Effect는 `url`에 반응하되, `numberOfItems`에는 반응하지 않아야 하는 경우
>`numberOfItems`를 Effect 이벤트 안으로 이동시킨다.

```jsx
const onVisit = useEffectEvent(visitedUrl => {
  logVisit(visitedUrl, numberOfItems); // numberOfItems는 항상 최신값
});

useEffect(() => {
  onVisit(url); // url이 바뀔 때만 실행
}, [url]); // numberOfItems는 의존성 불필요
```

>[!TIP]
>`url`을 Effect 이벤트 내부에서 읽지 말고 인수로 전달하는 것이 좋다.
>명시적으로 전달함으로써 "다른 url로의 방문 = 별도 이벤트"임을 코드로 표현할 수 있고,
>의존성에서 실수로 `url`을 제거하는 것도 방지된다.

>[!WARNING]
>린터를 억제(`eslint-disable-next-line react-hooks/exhaustive-deps`)하는 것은 피할 것.
>린터를 억제하면 오래된 값(stale value)문제가 발생한다.
>`useEffectEvent`가 린터 없이 이 문제를 해결하는 올바른 방법이다.
