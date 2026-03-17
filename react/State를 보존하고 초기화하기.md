React는 UI 트리에서의 위치를 통해 각 state가 어떤 컴포넌트에 속하는지 추적한다.

## State는 렌더트리의 위치에 연결된다

state는 컴포넌트 안에 살고있는게 아니라, React 안에 있다.

React는 UI 트리에서의 위치를 기준으로 각 state를 컴포넌트와 연결한다.

**React는 컴포넌트가 UI 트리에서 그 자리에 렌더링되는 한 state를 유지한다.**

컴포넌트가 제거되거나 같은 자리에 다른 컴포넌트가 렌더링되면 state도 함께 사라진다.

```
div
├── Counter (score: 0)  ← 첫 번째 위치
└── Counter (score: 3)  ← 두 번째 위치, 각자 독립된 state
```
```
div
├── Counter 제거됨 💥
└── (비어있음)        ← state도 함께 사라짐
```

## 같은 자리의 같은 컴포넌트는 state를 보존한다

props가 바뀌어도 같은 위치에 같은 컴포넌트면 React는 동일한 컴포넌트로 본다.

>[!WARNING]
>React는 JSX 마크업에서가 아닌 UI 트리에서의 위치에 관심이 있다.
>React는 당신이 반환하는 트리만 본다.

## 같은 위치의 다른 컴포넌트는 state를 초기화한다

같은 위치에 다른 컴포넌트를 렌더링할 때 컴포넌트는 그의 전체 서브 트리의 state를 초기화한다.

**리렌더링할 때 State를 유지하고 싶다면, 트리 구조가 같아야한다.** 

>[!WARNING]
>만약 구조가 다르다면 React가 트리에서 컴포넌트를 지울 때 State로 지우기 때문에 State가 유지되지 않는다.
>이것이 컴포넌트 함수를 중첩해서 정의하면 안되는 이유
>**항상 컴포넌트를 중첩해서 정의하지 않고 최상위 범위에서 정의해야 한다.**

## 같은 위치에서 state를 초기화하기

### 다른 위치에 컴포넌트를 렌더링하기

```jsx
import { useState } from 'react';

export default function Scoreboard() {
  const [isPlayerA, setIsPlayerA] = useState(true);
  return (
    <div>
      {isPlayerA &&
        <Counter person="Taylor" />
      }
      {!isPlayerA &&
        <Counter person="Sarah" />
      }
      <button onClick={() => {
        setIsPlayerA(!isPlayerA);
      }}>
        Next player!
      </button>
    </div>
  );
}

function Counter({ person }) {
  const [score, setScore] = useState(0);
  const [hover, setHover] = useState(false);

  let className = 'counter';
  if (hover) {
    className += ' hover';
  }

  return (
    <div
      className={className}
      onPointerEnter={() => setHover(true)}
      onPointerLeave={() => setHover(false)}
    >
      <h1>{person}'s score: {score}</h1>
      <button onClick={() => setScore(score + 1)}>
        Add one
      </button>
    </div>
  );
}

```

각 `Counter`의 state는 DOM에서 지워질 때마다 제거된다. 이것이 버튼을 누를 때마다 초기화되는 이유

### key를 이용해 state를 초기화하기

React가 컴포넌트를 구별할 수 있도록 key를 사용할 수도 있다.

```jsx
import { useState } from 'react';

export default function Scoreboard() {
  const [isPlayerA, setIsPlayerA] = useState(true);
  return (
    <div>
      {isPlayerA ? (
        <Counter key="Taylor" person="Taylor" />
      ) : (
        <Counter key="Sarah" person="Sarah" />
      )}
      <button onClick={() => {
        setIsPlayerA(!isPlayerA);
      }}>
        Next player!
      </button>
    </div>
  );
}

function Counter({ person }) {
  const [score, setScore] = useState(0);
  const [hover, setHover] = useState(false);

  let className = 'counter';
  if (hover) {
    className += ' hover';
  }

  return (
    <div
      className={className}
      onPointerEnter={() => setHover(true)}
      onPointerLeave={() => setHover(false)}
    >
      <h1>{person}'s score: {score}</h1>
      <button onClick={() => setScore(score + 1)}>
        Add one
      </button>
    </div>
  );
}

```

key가 전역적으로 유일하지 않다는 것을 기억해야 한다. key는 오직 부모 안에서만 자리를 명시한다.

### key를 이용해 폼을 초기화하기

key로 state를 초기화하는 것은 특히 폼을 다룰 때 유용하다.

```jsx
import { useState } from 'react';
import Chat from './Chat.js';
import ContactList from './ContactList.js';

export default function Messenger() {
  const [to, setTo] = useState(contacts[0]);
  return (
    <div>
      <ContactList
        contacts={contacts}
        selectedContact={to}
        onSelect={contact => setTo(contact)}
      />
      <Chat key={to.id} contact={to} />
    </div>
  )
}

const contacts = [
  { id: 0, name: 'Taylor', email: 'taylor@mail.com' },
  { id: 1, name: 'Alice', email: 'alice@mail.com' },
  { id: 2, name: 'Bob', email: 'bob@mail.com' }
];

```

>[!TIP]
>**제거된 컴포넌트의 state를 보존하기**
>1. CSS - 이 방법은 간단한 UI에서 잘 작동하지만, 숨겨진 트리가 크고 많은 DOM노드를 가지고 있다면 매우 느려짐
>2. state를 상위로 올리기
>3. React state 이외의 다른 저장소를 이용 (localStorage, 전역상태관리)
>
>하지만 어떤 방법을 선택하더라도 `<Chat>` 트리에 `key`를 주는 것이 타당하다.
