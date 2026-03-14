## batching
- 이벤트 핸들러 내 모든 코드 실행 후 한 번에 리렌더링
- 의도적 이벤트(클릭 등) 간에는 batch 안함
## 업데이터 함수(updater function)
```js
// 1만 증가 (batching)
setNumber(number + 1)
setNumber(number + 1)
setNumber(number + 1)

// 3 증가 (updater function)
setNumber(n => n + 1)
setNumber(n => n + 1)
setNumber(n => n + 1)
```

## 큐 처리 순서
```js
setNumber(5) // 5로 바꾸기 큐에 추가
setNumber(n => n + 1) // 업데이터 함수 큐에 추가
// 결과 6
```

## 명명규칙
- 업데이터 함수 인수는 state 변수 첫글자 or prev 접두사
`setEnabled(e => !e) / setEnabled(prevEnabled => !prevEnabled)`
---
> [!WARNING]
> 마지막에 값으로 덮으면 이전 큐 계산 다 날아간다.

>[!warning]
>업데이터 함수는 순수 해야한다.
>업데이터 함수 안에서 사이드 이펙트 금지.
> 렌더링 중에 실행되고 Strict Mode에서는 두번 실행됨.

>[!warning]
>비동기 처리할 때 특히 주의
>setPending(pending - 1) -> 클릭 여러 번시 꼬임
>setPending(n => n - 1) -> 안전
