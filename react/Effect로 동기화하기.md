>`Effect`를 사용하면 렌더링 후 특정 코드를 실행하여,
>외부 시스템과 컴포넌트를 동기화 할 수 있다.

## `Effect`란 무엇이고 이벤트와는 어떻게 다른가

`Effect`에 대해 알아보기 전 컴포넌트 내부 2가지 로직 유형에 대해 알아야 한다.

- **렌더링 코드**를 주관하는 로직은 컴포넌트 최상단에 위치,
	- `props`와`state`를 적절히 변형해 결과적으로 JSX를 반환
	- **렌더링 코드 로직은 순수해야 한다.**
- **이벤트 핸들러**는 단순한 계산 용도가 아닌 무언가를 하는 컴포넌트 내부 중첩 함수
	- 특정 사용자 작업(버튼 클릭, 입력)으로 인한 발생하는 **부수 효과**를 포함한다

>가끔은 이것으로 충분하지 않다,
>서버에 접속하는 것은 순수한 계산이 아니며 부수 효과를 발생시키기 때문에
>렌더링 중에는 할 수 없다.


>[!NOTE]
>`Effect`는 렌더링 자체에 의해 발생하는 부수 효과를 특정하는 것
>특정 이벤트가 아닌 렌더링에 의해 직접 발생
>`Effect`는 **커밋**이 끝난 후에 화면 업데이트가 이루어지고 나서 실행
>이 시점이 `React` 컴포넌트를 외부 시스템(네트워크, 서드파티 라이브러리)과 동기화 하기 좋은 타이밍

>[!CAUTION]
>**Effect가 단순히 다른 state를 조정하는 용도라면, Effect가 필요하지 않을 수 있다.**
>`Effect`는 주로 외부 시스템과 동기화 하기 위해 사용된다.(브라우저 API, 서드파티, 네트워크)

## `Effect`를 작성하는 법

1. **`Effect`선언**. - `Effect`는 모든 `commit`이후에 실행된다.
2. **`Effect` 의존성 지정**. - `Effect`는 모든 렌더링 후가 아닌 필요할 때만 다시 실행되어야 한다.
3. **필요한 경우 클린업 함수 추가**. - 일부 `Effect`는 수행 중이던 작업을 중지, 취소 또는 정리하는 방법을 지정해야 할 수 있다.

### `Effect` 선언하기
```jsx
import { useEffect } from 'react';

function MyComponent() {  
  useEffect(() => {  
   // 이곳의 코드는 *모든* 렌더링 후에 실행됩니다  
  });  
  return <div />;  
}
```

**`useEffect`는 화면에 렌더링이 반영될 때까지 코드 실행을 지연**시킨다

### `Effect`의 의존성 지정하기

```jsx
import { useState, useRef, useEffect } from 'react';

function VideoPlayer({ src, isPlaying }) {
  const ref = useRef(null);

  useEffect(() => {
    if (isPlaying) {
      console.log('video.play() 호출');
      ref.current.play();
    } else {
      console.log('video.pause() 호출');
      ref.current.pause();
    }
  }, [isPlaying]);

  return <video ref={ref} src={src} loop playsInline />;
}

export default function App() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [text, setText] = useState('');
  return (
    <>
      <input value={text} onChange={e => setText(e.target.value)} />
      <button onClick={() => setIsPlaying(!isPlaying)}>
        {isPlaying ? '일시 정지' : '재생'}
      </button>
      <VideoPlayer
        isPlaying={isPlaying}
        src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
      />
    </>
  );
}
```

- 의존성 배열에는 여러 개의 종속성을 포함할 수 있다.
- `React`는 `Object.is`비교를 사용하여 종속성 값을 비교한다.
- **의존성을"선택"할 수 없다는 점을 유의**
- 코드가 다시 실행되길 원하지 않는 경우
	- **`Effect` 내부를 수정하여 그 종속성이 필요하지 않도록 만들어야함**


>[!WARNING]
>의존성 배열이 없는 경우와 _빈_ `[]` 의존성 배열이 있는 경우의 동작이 다르다.

```jsx
useEffect(() => {  
  // 모든 렌더링 후에 실행됩니다  
});  

useEffect(() => {  
  // 마운트될 때만 실행됩니다 (컴포넌트가 나타날 때)  
}, []);  

useEffect(() => {  
  // 마운트될 때 실행되며, *또한* 렌더링 이후에 a 또는 b 중 하나라도 변경된 경우에도 실행됩니다  
}, [a, b]);
```

### `ref`는 의존성 배열에서 생략해도 되는 이유

>[!TIP]
>`ref`객체는 안정된 식별성(stable identity)을 가지기 때문.
>`React`는 동일한  `useRef`호출에서 항상 **같은 객체를 얻을 수 있음을 보장**
>`ref`는 의존성 배열에 포함하든 포함하지 않든 상관 없다.
>
>안정된 식별성을 가진 의존성을 생략하는 것은 린터가 해당 객체가 안정적임을 알 수 있는 경우에만 작동
>`ref`가 부모 컴포넌트에서 전달되었다면, 의존성 배열에 명시해야 한다.
>왜냐하면 부모 컴포넌트가 항상 동일한 `ref`를 전달하는지 또는 여러 `ref`중 하나를 조건부로 전달하는지 알 수 없기 때문

### 필요하다면 클린업 함수를 추가

서버와 연결해야하는 컴포넌트의 경우 예시

>의존성이 바뀔 때마다 React는 이전 cleanup → 새 setup 순서로 실행. cleanup 없으면 구 연결이 끊기지 않고 계속 쌓인다.
>이 문제를 해결하려면 `Effect`에서 클린업 함수를 반환하면 된다.

```jsx
// App.js
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

export default function ChatRoom() {
  useEffect(() => {
    const connection = createConnection();
    connection.connect();
    return () => connection.disconnect();
  }, []);
  return <h1>채팅에 오신걸 환영합니다!</h1>;
}
```

```js
export function createConnection() {
  // 실제 구현은 정말로 채팅 서버에 연결하는 것이 되어야 합니다.
  return {
    connect() {
      console.log('✅ 연결 중...');
    },
    disconnect() {
      console.log('❌ 연결 해제됨');
    }
  };
}
```

>[!NOTE]
>개발 모드(Strict Mode)에서 세 개의 콘솔 로그를 확인할 수 있다.
>1. `"✅ 연결 중..."`
>2. `"❌ 연결 해제됨"`
>3. `"✅ 연결 중..."`
>
>이것은  개발 모드에서 올바른 동작.
>클린업을 잘 구현하면 Effect를 한 번 실행하는 것과 실행, 클린업, 이후 다시 실행하는 것 사이에 사용자에게 보이는 차이가 없어야 한다.
>**배포 환경에서는 `"✅ 연결 중..."`이 한 번만 출력된다.**
>컴포넌트를 다시 마운트하는 것은 개발 중에만 발생하며 클린업이 필요한 Effect를 찾아주는 데 도움을 준다

#### 개발 중에 Effect가 두 번 실행되는 경우를 다루는 방법

>React는 마지막 예시와 같은 버그를 찾기 위해 개발 중에 컴포넌트를 명시적으로 다시 마운트한다
>**“Effect를 한 번 실행하는 방법”이 아니라 “어떻게 Effect가 다시 마운트된 후에도 작동하도록 고칠 것인가”라는 것이 옳은 질문**
>일반적인 정답은 클린업 함수를 구현 하는것.
>클린업 함수는 `Effect`가 수행하던 작업을 중단하거나 되돌리는 역할을 한다.
>사용자가 `Effect`가 한 번 실행되는 것처럼 (배포 환경 같이)설정 -> 클린업 -> 설정 순서 간에 차이를 느끼지 못해야 한다.

#### `Effect`가 두 번 실행되는 것을 막기위해 `ref`를 사용하지 말것

>[!CAUTION]
>`ref`를 사용해 `Effect`가 한 번만 실행되도록 하는 것은
>`Effect`가 개발 모드에서 두 번 실행되는 것을 막으려다 흔히 빠지는 함정이다.

```jsx
const connectionRef = useRef(null);  
useEffect(() => {  
  // 🚩 버그를 수정하지 않습니다!!!  
  if (!connectionRef.current) {  
    connectionRef.current = createConnection();  
    connectionRef.current.connect();  
  }  
}, []);
```

>이렇게 하면 개발 모드에서 `"✅ 연결 중..."`이 한 번만 보이지만 버그가 수정된 건 아니다.
>사용자가 다른 페이지로 이동해도 연결은 여전히 닫히지 않고, 다시 돌아오면 새 연결이 생성됩니다. 사용자가 앱을 탐색할수록 연결이 계속 쌓이게 되는데, 이는 수정 전과 동일하다.
>버그를 수정하기 위해선 Effect를 단순히 한 번만 실행되도록 만드는 것으로는 부족하다. Effect는 위에 있는 예시가 연결을 클린업 한것처럼 다시 마운트된 이후에도 제대로 동작해야 한다.

### 데이터 페칭

`Effect`가 어떤 데이터를 가져온다면, 클린업 함수에서는 **`fetch`를 중단**하거나 결과를 무시해야 한다.

>[!NOTE]
>비동기 fetch가 두 번 실행될 때 응답 순서가 보장되지 않아 stale 데이터가 표시될 수 있다.
>`ignore` 플래그 패턴으로 cleanup에서 `ignore = true` 처리하면 방지된다.
>실무에선 TanStack Query 같은 라이브러리가 이걸 내부에서 처리해주는 것.

```jsx
useEffect(() => {  
  let ignore = false;  
  
  async function startFetching() {  
    const json = await fetchTodos(userId);  
    if (!ignore) {  
      setTodos(json);  
    }  
  }  


startFetching();  

  return () => {  
    ignore = true;  
  };  
}, [userId]);
```

>이미 발생한 네트워크 요청을 취소 할 수는 없지만,
>클린업 함수는 더 이상 관련이 없는 `fetch`가 애플리케이션에 계속 영향을 미치지 않도록 보장해야 한다.
