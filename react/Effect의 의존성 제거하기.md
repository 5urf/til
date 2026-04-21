## 의존성은 코드와 일치해야 한다

>[!IMPORTANT]
>의존성 = 코드의 반영
>의존성 목록은 개발자가 "선택"하는 것이 아니다.
>Effect 코드에서 읽는 모든 반응형 값이 자동으로 의존성이 된다.
>의존성을 바꾸려면 먼저 코드를 바꿔야 한다.

- 의존성을 제거하고 싶다면 해당 값이 반응형이 아님을 린터에 "증명"해야 함
- 컴포넌트 외부로 이동 -> 재렌더링으로 변경될 수 없으므로 의존성 불필요

>[!WARNING]
>린터를 억제(`eslint-disable-next-line react-hooks/exhaustive-deps`)하는 것은 피할 것.
>Effect가 의존하는 값에 대해 React에 "거짓말"을 하게 되어 오래된 값(stale value)버그가 발생한다.

---

## 불필요한 의존성 제거 패턴

>[!IMPORTANT]
>이벤트 핸들러로 이동
>특정 상호 작용(버튼 클릭 등)에 대한 응답으로만 실행되어야 하는 코드가 Effect 안에 있다면,
>그건 Effect가 아니라 이벤트 핸들러에 있어야 한다.

```jsx
// ❌ submitted 변경에 반응하는 Effect - theme이 바뀔 때도 다시 실행됨
useEffect(() => {
  if (submitted) {
    post('/api/register');
    showNotification('등록 완료!', theme);
  }
}, [submitted, theme]);

// ✅ 폼 제출이라는 특정 상호작용에 대한 응답 -> 이벤트 핸들러로
function handleSubmit() {
  post('/api/register');
  showNotification('등록 완료!', theme);
}
```

>[!IMPORTANT]
>Effect 분리
>하나의 Effect가 서로 관련 없는 여러 작업을 동기화하고 있다면 독립적인 여러 Effect로 분리한다.
>한 Effect를 삭제해도 다른 Effect 로직이 깨지지 않아야 올바른 분리다.

>[!IMPORTANT]
>업데이터 함수로 State 의존성 제거
>이전 State 기반으로 State를 업데이트 할 때 State 값을 Effect에서 직접 읽으면 그 State가 의존성이 된다.
>업데이터 함수를 사용하면 의존성 없이 최신 값을 참조할 수 있다.

```jsx
// ❌ messages가 의존성이 되어 메시지 수신 때마다 재연결
connection.on('message', (msg) => {
  setMessages([...messages, msg]); // messages를 읽음
});

// ✅ 업데이터 함수로 messages 의존성 제거
connection.on('message', (msg) => {
  setMessages(prev => [...prev, msg]); // messages를 읽지 않음
})
```

---

## 객체•함수 의존성 문제

>[!IMPORTANT]
>객체/함수는 매 렌더링마다 새로 생성된다
>자바스크립트에서 객체와 함수는 내용이 같아도 다른 시간에 생성되면 서로 다른 것으로 간주된다(`Object.is`비교).
>컴포넌트 본문에서 객체/함수를 생성하고 Effect 의존성으로 사용하면 매 렌더링마다 Effect가 재실행된다.

```jsx
// 문제: 매 렌더링마다 새로운 options 객체 생성 -> Effect 재실행
const options = { serverUrl, roomId }; // 렌더링마다 새 객체
useEffect(() => {
  const connection = createConnection(options);
  // ...
}, [options]); // options가 매번 달라짐
```
- 해결 방법 3가지

1. **컴포넌트 외부로 이동** - props/state에 의존하지 않는 경우

```jsx
const options = { serverUrl: 'https://...', roomId: 'music' }; // 컴포넌트 외부

function ChatRoom() {
  useEffect(() => { /* options 사용 */}, []);
}
```

2. **Effect 내부로 이동** - 반응형 값에 의존 하는 경우

```jsx
useEffect(() => {
  const options = { serverUrl, roomId }; // Effect 내부에서 생성
  const connection = createConnection(options);
  // ...
}, [roomId]); // 원시값만 의존성으로
```

3. **객체/함수에서 원시값 추출** - props로 객체를 받는 경우

```jsx
function ChatRoom({ options }) {
  const { roomId, serverUrl } = options; // 렌더링 중 원시값 추출
  useEffect(() => { /* roomId, serverUrl 사용 */}, [roomId, serverUrl]);
}
```

>[!TIP]
>가능하면 객체와 함수를 Effect의 의존성으로 사용하지 말 것.
>컴포넌트 외부 또는 Effect 내부로 이동하거나, 원시값을 추출해서 사용하는 것이 좋다.
