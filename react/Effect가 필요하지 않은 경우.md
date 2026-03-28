>외부 시스템이 관여하지 않는 경우, Effect가 필요하지 않다
>불필요한 Effect를 제거하면 코드를 더 쉽게 따라갈 수 있고, 실행 속도가 빨라지며, 에러 발생 가능성이 줄어든다.


## 불필요한 Effect를 제거하는 방법

- 렌더링을 위해 데이터를 변환하는 데 Effect가 필요하지 않다
- 사용자 이벤트를 처리하는 데 Effect가 필요하지 않다.

### props 또는 state에 따라 state 업데이트하기

```jsx
// 🔴 피하세요: 중복된 state 및 불필요한 Effect
const [fullName, setFullName] = useState('');
useEffect(() => {
  setFullName(firstName + ' ' + lastName);
}, [firstName, lastName]);
```

>[!CAUTION]
>오래된 값으로 한 번 렌더링 한 후 -> 업데이트된 값으로 다시 렌더링하기 때문에 비효율적이다.

```jsx
// ✅ 좋습니다: 렌더링 중에 계산됨
const fullName = firstName + ' ' + lastName;
```

>기존 props나 state에서 계산할 수 있다면 그것을 state에 넣지 말고,
>렌더링 중에 계산하게 하라

>[!IMPORTANT]
>`props`나 `state`에서 계산 가능한 값은 `state`로 따로 저장하지 않고,
>렌더링 중에 직접 계산하는 것이 원칙이다.

---
## 비용이 많이 드는 계산 캐싱하기

```jsx
// 🔴 피하세요: 중복된 state 및 불필요한 Effect
const [visibleTodos, setVisibleTodos] = useState([]);
useEffect(() => {
  setVisibleTodos(getFilteredTodos(todos, filter));
}, [todos, filter]);
```

>state와 Effect를 제거하고, `getFilteredTodos()`가 느리다면 `useMemo`로 감쌀 것

```jsx
// ✅ todos나 filter가 변경되지 않는 한 다시 실행되지 않습니다.
const visibleTodos = useMemo(() => getFilteredTodos(todos, filter), [todos, filter]);
```
>[!IMPORTANT]
>렌더링 중 계산이 느릴 수 있다면, Effect + state가 아니라 `useMemo`로 캐싱한다

>[!NOTE]
>React 컴파일러는 비용이 많이 드는 계산을 자동으로 메모이제이션 할 수 있어서,
>대다수의 경우 `useMemo`를 사용할 필요가 없다.

---
### prop 변경 시 모든 state 초기화

```jsx
// 🔴 피하세요: Effect에서 prop 변경 시 state 초기화
useEffect(() => {
  setComment('');
}, [userId]);
```

>대신 `key`를 사용하여 컴포넌트 자체를 재설정

```jsx
// ✅ userId가 바뀔 때마다 Profile 전체가 재생성됩니다.
export default function ProfilePage({ userId }) {
  return <Profile userId={userId} key={userId} />;
}
```
>`Profile` 컴포넌트에 `userId`를 `key`로 전달하면
>React가 `userId`가 다른 두 `Profile` 컴포넌트를 **state를 공유해서는 안 되는 두 개의 다른 컴포넌트**로 취급한다.

>[!IMPORTANT]
>prop이 바뀔 때 state를 Effect로 초기화하는 패턴은 불필요한 렌더링을 유발한다.
>key를 활용하면 React가 자동으로 처리한다.

---
### prop이 변경될 때 일부 state 조정하기

```jsx
// 🔴 피하세요: Effect에서 prop 변경 시 state 조정하기
useEffect(() => {
  setSelection(null);
}, [items]);
```

>더 나은 방법은 렌더링 중에 파생값으로 계산하는 것이다.

```jsx
// ✅ 최고예요: 렌더링 중에 모든 것을 계산
const selection = items.find(item => item.id === selectedId) ?? null;
```

>이렇게 하면 state를 조정할 필요가 없다.

---
### 이벤트 핸들러 간 로직 공유

```jsx
// 🔴 피하세요: Effect 내부의 이벤트별 로직
useEffect(() => {
  if (product.isInCart) {
    showNotification(`Added ${product.name} to the shopping cart!`);
  }
}, [product]);
```

>[!WARNING]
>이 코드는 페이지 리로드 시에도 알림이 다시 표시되는 버그를 유발한다.
>**코드가 Effect에 있어야 하는지 이벤트 핸들러에 있어야 하는지 확실하지 않은 경우,**
>**이 코드가 실행되어야 하는 이유를 자문해 볼 것**

```jsx
// ✅ 좋습니다: 이벤트 핸들러에서 이벤트별 로직이 호출됩니다.
function buyProduct() {
  addToCart(product);
  showNotification(`Added ${product.name} to the shopping cart!`);
}
```

>이렇게하면, 불필요한 Effect가 제거되고 버그가 수정된다.

---
### POST 요청 보내기

```jsx
// ✅ 좋습니다: 컴포넌트가 표시되었으므로 이 로직이 실행됩니다.
useEffect(() => {
  post('/analytics/event', { eventName: 'visit_form' });
}, []);

// 🔴 피하세요: Effect 내부의 이벤트별 로직
useEffect(() => {
  if (jsonToSubmit !== null) {
    post('/api/register', jsonToSubmit);
  }
}, [jsonToSubmit]);
```
>analytics는 Effect가 맞다 (폼이 표시되었기 때문에 실행)
>`/api/register`는 이벤트 핸들러로 옮겨야 한다 (사용자가 버튼을 눌렀기 때문에 실행)

---
### 연쇄 계산

```jsx
// 🔴 피하세요: 서로를 트리거하기 위해서만 state를 조정하는 Effect 체인
useEffect(() => { if (card?.gold) setGoldCardCount(c => c + 1); }, [card]);
useEffect(() => { if (goldCardCount > 3) { setRound(r => r + 1); setGoldCardCount(0); } }, [goldCardCount]);
useEffect(() => { if (round > 5) setIsGameOver(true); }, [round]);
```
>[!WARNING]
>최악의 경우 `setCard → 렌더링 → setGoldCardCount → 렌더링 → setRound → 렌더링 → setIsGameOver → 렌더링`, 불필요한 리렌더링이 3번 발생한다

```jsx
// ✅ 이벤트 핸들러에서 다음 state를 모두 계산합니다.
function handlePlaceCard(nextCard) {
  setCard(nextCard);
  if (nextCard.gold) {
    if (goldCardCount <= 3) {
      setGoldCardCount(goldCardCount + 1);
    } else {
      setGoldCardCount(0);
      setRound(round + 1);
      if (round === 5) alert('Good game!');
    }
  }
}
```

>[!IMPORTANT]
>Effect를 체이닝하면 렌더링이 여러 번 발생하고 코드가 취약해진다.
>이벤트 핸들러 안에서 다음 state를 한 번에 계산해야 한다.

---
### 애플리케이션 초기화

```jsx
// 🔴 피하세요: 한 번만 실행되어야 하는 로직이 포함된 Effect
useEffect(() => {
  loadDataFromLocalStorage();
  checkAuthToken();
}, []);
```
>[!WARNING]
>개발 중 Strict Mode에서 두 번 실행될 수 있어, 인증 토큰 무효화 등의 문제가 생긴다.

```jsx
// ✅ 앱 로드당 한 번만 실행
let didInit = false;
function App() {
  useEffect(() => {
    if (!didInit) {
      didInit = true;
      loadDataFromLocalStorage();
      checkAuthToken();
    }
  }, []);
}
```
>앱 로드당 한 번 실행되어야 한다면, 최상위 변수를 추가하여 이미 실행되었는지를 추적할 것

---

## state 변경을 부모 컴포넌트에게 알리기

```jsx
// 🔴 피하세요: onChange 핸들러가 너무 늦게 실행됨
useEffect(() => {
  onChange(isOn);
}, [isOn, onChange]);
```
```jsx
// ✅ 좋습니다: 업데이트를 유발한 이벤트가 발생한 동안 모든 업데이트를 수행합니다.
function updateToggle(nextIsOn) {
  setIsOn(nextIsOn);
  onChange(nextIsOn);
}
```

>React는 서로 다른 컴포넌트의 **업데이트를 일괄 처리**하므로 렌더링 패스는 한번만 발생한다.
>두개의 다른 state 변수를 동기화하려고 할때마다 대신 **state 끌어올리기**를 사용할 것

---

## 부모에게 데이터 전달하기

```jsx
// 🔴 피하세요: Effect에서 부모에게 데이터 전달하기
useEffect(() => {
  if (data) onFetched(data);
}, [onFetched, data]);
```
>[!WARNING]
>React에서 데이터는 부모 -> 자식 방향으로 흐른다.
>자식이 Effect에서 부모 state를 업데이트하면 데이터 흐름 추적이 매우 어려워 진다.

```jsx
// ✅ 좋습니다: 부모가 직접 데이터를 가져와서 자식에게 내려줍니다.
function Parent() {
  const data = useSomeAPI();
  return <Child data={data} />;
}
```

---

### 외부 저장소 구독하기

```jsx
// 이상적이지 않습니다: Effect에서 저장소를 수동으로 구독
useEffect(() => {
  window.addEventListener('online', updateState);
  window.addEventListener('offline', updateState);
  return () => { /* cleanup */ };
}, []);
```

>React에는 외부 저장소 구독을 위한 Hook이 있다.

```jsx
// ✅ 좋습니다: 내장 Hook으로 외부 스토어 구독하기
return useSyncExternalStore(
  subscribe,
  () => navigator.onLine,  // 클라이언트
  () => true               // 서버
);
```

---

### 데이터 가져오기

```jsx
// 🔴 피하세요: 정리 로직 없이 가져오기
useEffect(() => {
  fetchResults(query, page).then(json => {
    setResults(json);
  });
}, [query, page]);
```

>[!WARNING]
>`"hello"`를 빠르게 입력하면 `"hell"` 응답이 `"hello"` 응답보다 나중에 도착할 수 있다 → 잘못된 검색 결과 표시(경쟁 조건)
>
>경쟁 조건: 서로 다른 두 요청이 서로 경쟁하여 예상과 다른 순서로 도착하는 것을 말한다.

>경쟁 조건을 수정하려면 오래된 응답을 무시하는 **정리 함수를 추가**해야 한다.

```jsx
// ✅ cleanup으로 오래된 응답 무시
useEffect(() => {
  let ignore = false;
  fetchResults(query, page).then(json => {
    if (!ignore) setResults(json);
  });
  return () => { ignore = true; };
}, [query, page]);
```

>[!NOTE]
>이 방법만으론 프레임워크에 내장된 데이터 가져오기 메커니즘을 사용하는 것만큼 효율적이지는 않지만,
>데이터 가져오기 로직을 사용자 정의 Hook으로 옮기면 나중에 효율적인 데이터 가져오기 전략을 취하기가
>더 쉬워진다.
