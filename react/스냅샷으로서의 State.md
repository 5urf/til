> `setState`는 현재 값을 바꾸는 게 아니라 **다음 렌더링을 예약**하는 것이다.

---

## setState는 리렌더링을 큐에 추가한다

```tsx
const [isSent, setIsSent] = useState(false)

<form onSubmit={(e) => {
  e.preventDefault()
  setIsSent(true)   // 리렌더링 예약 - 현재 isSent는 여전히 false
  sendMessage(message)
}}>
```

1. `setIsSent(true)` 호출 → 다음 렌더를 큐에 추가
2. React가 `isSent = true`로 컴포넌트를 다시 렌더링
3. JSX가 새 스냅샷으로 교체됨

---

## 렌더링 = 그 시점의 JSX 스냅샷 반환

"렌더링"이란 React가 컴포넌트 함수를 호출하는 것.  
반환된 JSX는 **렌더 당시 state를 기준으로 계산된 스냅샷**이다.  
props, 이벤트 핸들러, 로컬 변수 전부 그 시점 값으로 고정된다.

```
React가 함수 호출
  → 함수가 JSX 스냅샷 반환
    → React가 스냅샷에 맞게 화면 업데이트
```

---

## state는 React 자체에 존재한다

일반 변수는 함수 실행이 끝나면 사라지지만,  
state는 함수 외부 React가 관리하기 때문에 함수 종료 후에도 유지된다.  
React는 컴포넌트를 호출할 때 **해당 렌더에 해당하는 state 스냅샷을 함께 전달**한다.

---

## 같은 렌더 안에서 setState 여러 번 호출 → state는 고정

```js
// number = 0인 렌더에서
setNumber(number + 1); // setNumber(0 + 1)
setNumber(number + 1); // setNumber(0 + 1)
setNumber(number + 1); // setNumber(0 + 1)
// 결과: 1  (3이 아님)
```

같은 렌더 안에서 `number`는 항상 `0`으로 고정된다.  
누적 증가가 필요하면 **함수형 업데이트**를 사용해야 한다.

```js
setNumber((prev) => prev + 1); // 1
setNumber((prev) => prev + 1); // 2
setNumber((prev) => prev + 1); // 결과: 3
```

---

## 비동기 코드에서도 핸들러는 렌더 당시 스냅샷을 본다

```js
setNumber(number + 5);

setTimeout(() => {
  alert(number); // 0 출력 - 3초 후 실행되어도 이 렌더의 스냅샷은 0
}, 3000);
```

이벤트 핸들러는 **생성된 렌더의 state를 클로저로 캡처**한다.  
나중에 실행되더라도 만들어진 렌더 당시 값이 보인다.

> [!TIP]
> 비동기 상황에서 최신 state가 필요하면 `ref`를 쓰거나 함수형 업데이트 `prev => ...`를 사용한다.

> [!WARNING]
> "왜 state가 안 바뀌지?"라고 느껴지는 대부분의 상황은  
> 현재 렌더 스냅샷과 다음 렌더를 혼동하는 데서 온다.  
> 이벤트 핸들러는 자신이 만들어진 렌더의 세계 안에서만 동작한다.
