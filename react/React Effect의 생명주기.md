
## Effect의 생명주기

>[!IMPORTANT]
>Effect의 생명주기
>컴포넌트는 마운트 / 업데이트 / 언마운트의 생명주기를 가지지만,
>**Effect는 동기화 시작과 동기화 중지**, 이 두 가지만 한다.
>Effect를 컴포넌트 생명주기 관점으로 생각하면 복잡해지므로, Effect 자체의 관점으로 생각하는 것이 중요하다.

- Effect 본문 = 동기화 시작 방법
- cleanup 함수 = 동기화 중지 방법
- props/state가 변경되면 cleanup -> 재실행으로 동기화를 여러 번 반복할 수 있음

```jsx
useEffect(() => {
  const connection = createConnection(serverUrl, roomId);
  connection.connect();
  return () => {
    connection.disconnect(); // cleanup: 동기화 중지
  };
}, [roomId]);
```

>[!IMPORTANT]
>동기화 관점으로 이해
>"마운트될 때 실행, 언마운트될 때 정리"가 아니라
>**"동기화를 시작하는 방법과 중지하는 방법을 기술"**하는 것이 Effect다.
>한 번에 하나의 시작/중지 사이클에만 집중할 것.

---

## 반응형 값과 의존성 배열

>[!IMPORTANT]
>반응형 값(Reactive Value)
>컴포넌트 본문 내부에서 선언된 모든 값(props,state, 그로부터 계산된 변수)은 반응형이다.
>렌더링마다 변경될 수 있으므로 Effect에서 사용한다면 반드시 의존성 배열에 포함해야 한다.

- 컴포넌트 외부에 선언된 상수나 Effect 내부에서만 쓰이는 값은 반응형이 아님 -> 의존성 불필요
- `useState`의 setter, `useRef`의 ref 객체는 안정적(stable)이라 의존성에서 생략 가능

```jsx
function ChatRoom({ roomId }) {
  const [serverUrl, setServerUrl] = useState('https://localhost:1234');
  
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId, serverUrl]) // 둘 다 반응형이므로 반드시 포함
}
```
>[!IMPORTANT]
>빈 의존성 배열 `[]`의 의미
>Effect가 어떤 반응형 값도 읽지 않는다는 것을 의미한다.
>컴포넌트 마운트 시 동기화 시작, 언마운트 시 동기화 중지가 한 번씩만 일어난다.

---

## 각 Effect는 독립적인 동기화 프로세스

>[!IMPORTANT]
>Effect 분리 원칙
>서로 관련 없는 로직을 하나의 Effect에 넣지 말 것.
>하나의 Effect = 하나의 독립적인 동기화 프로세스.
>한 Effect를 삭제해도 다른 Effect 로직이 깨지지 않아야 올바르게 분리된 것이다.

```jsx
// ❌ 관련 없는 두 로직을 하나의 Effect에
useEffect(() => {
  logVisit(roomId);
  const connection = createConnection(serverUrl, roomId);
  connection.connect();
  return () => connection.disconnect();
}, [roomId]);

// ✅ 독립적인 두 Effect로 분리
useEffect(() => {
  logVisit(roomId);
}, [roomId])

useEffect(() => {
  const connection = createConnection(serverUrl, roomId);
  connection.connect();
  return () => connection.disconnect();
}, [roomId]);
```

---

## 린터와 의존성

>[!IMPORTANT]
>린터 규칙 준수
>린터가 의존성 오류를 잡아내면 린터를 억제하지 말 것.
>종속성 문제를 해결하는 올바른 방법은
>1. 값을 컴포넌트 외부로 이동.
>2. Effect 내부로 이동.
>3. Effect를 분리하는 것이다.

>종속성은 "선택"하는 것이 아니다.
>Effect에서 읽은 모든 반응형 값이 자동으로 종속성이 된다.
