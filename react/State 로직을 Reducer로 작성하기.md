
> 한 컴포넌트에서 `State` 업데이트가 여러 이벤트 핸들러로 분산되는 경우가 있다.
> 이 경우 컴포넌트를 관리하기 어려워 진다.
> 
> 문제 해결을 위해 `State`를 업데이트하는 모든 로직을 Reducer를 사용해
> 컴포넌트 외부의 단일 함수로 통합 관리가 가능하다.

관리하기 어려운 컴포넌트 예시

```jsx
import { useState } from 'react';
import AddTask from './AddTask.js';
import TaskList from './TaskList.js';

export default function TaskApp() {
  const [tasks, setTasks] = useState(initialTasks);

  function handleAddTask(text) {
    setTasks([...tasks, {
      id: nextId++,
      text: text,
      done: false
    }]);
  }

  function handleChangeTask(task) {
    setTasks(tasks.map(t => {
      if (t.id === task.id) {
        return task;
      } else {
        return t;
      }
    }));
  }

  function handleDeleteTask(taskId) {
    setTasks(
      tasks.filter(t => t.id !== taskId)
    );
  }

  return (
    <>
      <h1>Prague itinerary</h1>
      <AddTask
        onAddTask={handleAddTask}
      />
      <TaskList
        tasks={tasks}
        onChangeTask={handleChangeTask}
        onDeleteTask={handleDeleteTask}
      />
    </>
  );
}

let nextId = 3;
const initialTasks = [
  { id: 0, text: 'Visit Kafka Museum', done: true },
  { id: 1, text: 'Watch a puppet show', done: false },
  { id: 2, text: 'Lennon Wall pic', done: false },
];

```

- `Reducer`는 `State`를 다루는 방법
- `useState` -> `useReducer`로 바꾸는 세가지 단계
	1. `State`를 설정하는 방식 -> `Action`을 `Dispatch`하는 방식으로 전환
	2. `Reducer`함수 작성
	3. 컴포넌트에서 `Reducer`사용

## 1단계 - `State`를 설정하는 방식 -> `Action`을 `Dispatch`하는 방식으로 전환하기

>`State`를 설정하여 `React`에게 *무엇을 할 지* 지시하는 대신
>이벤트 핸들러에서 `Action`을 전달하여 *사용자가 방금 한 일*을 지정


```jsx
function handleAddTask(text) {  
  dispatch({  
    type: 'added',  
    id: nextId++,  
    text: text,  
  });
}  

  
function handleChangeTask(task) {  
  dispatch({  
    type: 'changed',  
    task: task  
  });  
}  

function handleDeleteTask(taskId) {  
  dispatch({
    // "Action" 객체:  
    type: 'deleted',  
    id: taskId  
  });  
}
```

- 이벤트 핸들러를 통해 "`task`를 설정"하는 대신 "`task`를 추가/변경/삭제"하는 `Action`을 전달하는 것
- 이러한 방식이 사용자 의도를 더 명확하게 설명
- `dispatch`함수에 넣어준 객체를 `Action`이라고 한다.

>[!IMPORTANT]
>`Action` 객체는 어떤 형태든 될 수 있다.
>문자열 `type`을 넘겨주고 이외 정보는 다른 필드에 담아 전달하도록 작성하는 것이 일반적
>무슨 일이 일어나는지를 설명할 수 있는 이름을 넣어야함


## 2단계 - `Reducer` 함수 작성하기

`Reducer` 함수는 `State`에 대한 로직을 넣는 곳

`React`는 `Reducer`에서 반환한 값을 `State`에 설정

```js
function yourReducer(state, action) {
  // React가 설정하게 될 다음 State 값을 반환
}
```

- 이벤트 핸들러 `State` 설정, 관련 로직을 `Reducer` 함수로 이동
1. 첫번째 인자에 현재 `State` 선언
2. 두번째 인자에 `action`객체 선언
3. `Reducer`에서 다음 `State` 반환 (`React`가 `State`에 설정하게 될 값)

```js
function tasksReducer(tasks, action) {  
  switch (action.type) {  
    case 'added': {  
      return [...tasks, {  
        id: action.id,  
        text: action.text,  
        done: false  
      }];  
    }  

    case 'changed': {  
      return tasks.map(t => {  
        if (t.id === action.task.id) {  
          return action.task;  
        } else {  
          return t;  
        }  
      });  
    }  

    case 'deleted': {  
      return tasks.filter(t => t.id !== action.id);  
    }  
    default: {  
      throw Error('Unknown action: ' + action.type);  
    }  
  }  
}
```

>[!IMPORTANT]
>`Reducer` 함수 안에서는 `switch문`을 사용하는게 규칙


## 3단계 - 컴포넌트에서 `Reducer` 사용하기

- `useReducer` HOOK은 두 개의 인자를 넘겨 받음
1. `Reducer` 함수
2. 초기 `State` 값

- 아래와 같이 반환
1. `State`를 담을 수 있는 값
2. `Dispatch` 함수 (사용자의 `Action`을 `Reducer` 함수에게 "전달하게 될")

```jsx
// App.js
import { useReducer } from 'react';
import AddTask from './AddTask.js';
import TaskList from './TaskList.js';
import tasksReducer from './tasksReducer.js';

export default function TaskApp() {
  const [tasks, dispatch] = useReducer(
    tasksReducer,
    initialTasks
  );

  function handleAddTask(text) {
    dispatch({
      type: 'added',
      id: nextId++,
      text: text,
    });
  }

  function handleChangeTask(task) {
    dispatch({
      type: 'changed',
      task: task
    });
  }

  function handleDeleteTask(taskId) {
    dispatch({
      type: 'deleted',
      id: taskId
    });
  }

  return (
    <>
      <h1>Prague itinerary</h1>
      <AddTask
        onAddTask={handleAddTask}
      />
      <TaskList
        tasks={tasks}
        onChangeTask={handleChangeTask}
        onDeleteTask={handleDeleteTask}
      />
    </>
  );
}

let nextId = 3;
const initialTasks = [
  { id: 0, text: 'Visit Kafka Museum', done: true },
  { id: 1, text: 'Watch a puppet show', done: false },
  { id: 2, text: 'Lennon Wall pic', done: false },
];

```

```js
// tasksReducer.js
export default function tasksReducer(tasks, action) {
  switch (action.type) {
    case 'added': {
      return [...tasks, {
        id: action.id,
        text: action.text,
        done: false
      }];
    }
    case 'changed': {
      return tasks.map(t => {
        if (t.id === action.task.id) {
          return action.task;
        } else {
          return t;
        }
      });
    }
    case 'deleted': {
      return tasks.filter(t => t.id !== action.id);
    }
    default: {
      throw Error('Unknown action: ' + action.type);
    }
  }
}

```

## `useState` 와 `useReducer` 비교하기

- 코드 크기
	- `useState`를 사용하면, 미리 작성해야 하는 코드가 줄어든다 (보일러 플레이트 ⬇️)
	- 여러 이벤트 핸들러에서 비슷한 방식으로 `State`를 업데이트 하는경우에는 `useReducer`
- 가독성
	- 간단한 `State`를 업데이트 하는 경우에는 `useState`가 가독성이 좋은편
	- 복잡한 구조의 `State`를 다룰 경우 `useReducer`
- 디버깅
	- `useState`를 사용하며 버그를 발견했을 때 찾기 어려울 수 있다.
	- `useReducer`를 사용하면 각 `Action`을 통해 디버깅 가능
		- 하지만 `useState`보다 더 많은 코드를 단계별로 실행해서 디버깅 해야함
- 테스팅
	- `Reducer`를 독립적으로 분리해서 내보내거나 테스트 가능
	- `Reducer`가 특정 초기 `State` 및 `Action`에 대해 특정 `State`를 반환한다고 생각하고 테스트 하는 것이 유용

| 상황                                 | 선택           |
| ---------------------------------- | ------------ |
| state 업데이트가 단순하다                   | `useState`   |
| 여러 이벤트 핸들러가 비슷한 방식으로 `state`를 바꾼다  | `useReducer` |
| 디버깅시 "어느 `action`에서 깨졌는지" 추적이 필요하다 | `useReducer` |
| `Reducer`를 독립적으로 테스트하고 싶다          | `useReducer` |

## `Reducer` 잘 작성하기

>[!IMPORTANT]
>**`Reducer`는 반드시 순수해야 한다**
>`State`업데이트 함수(업데이터 함수)와 비슷하게 `Reducer`는 렌더링 중에 실행된다.
>(`Action`은 다음 렌더링 까지 대기)
>이것은 `Reducer`는 **반드시 순수**해야 한다는 것을 의미.
>비동기, `setTimeout`, API 요청을 수행해서는 안된다.

>[!IMPORTANT]
>**각 `Action`은 데이터 안에서 여러 변경들이 있더라도 하나의 사용자 상호작용을 설명해야 한다.**
>모든 `Action`을 `Reducer`에 기록하면 어떤 상호작용이나 응답이 어떤 순서로 일어났는지
>재구성할 수 있을 만큼 로그가 명확해야함 (디버깅에 도움)


### Immer로 간결한 Reducer 작성하기

객체와 배열을 변경하는 스타일로 Reducer를 작성하려면 `Immer` 라이브러리를 사용

```jsx
import { useImmerReducer } from 'use-immer';
import AddTask from './AddTask.js';
import TaskList from './TaskList.js';

function tasksReducer(draft, action) {
  switch (action.type) {
    case 'added': {
      draft.push({
        id: action.id,
        text: action.text,
        done: false
      });
      break;
    }
    case 'changed': {
      const index = draft.findIndex(t =>
        t.id === action.task.id
      );
      draft[index] = action.task;
      break;
    }
    case 'deleted': {
      return draft.filter(t => t.id !== action.id);
    }
    default: {
      throw Error('Unknown action: ' + action.type);
    }
  }
}

export default function TaskApp() {
  const [tasks, dispatch] = useImmerReducer(
    tasksReducer,
    initialTasks
  );

  function handleAddTask(text) {
    dispatch({
      type: 'added',
      id: nextId++,
      text: text,
    });
  }

  function handleChangeTask(task) {
    dispatch({
      type: 'changed',
      task: task
    });
  }

  function handleDeleteTask(taskId) {
    dispatch({
      type: 'deleted',
      id: taskId
    });
  }

  return (
    <>
      <h1>Prague itinerary</h1>
      <AddTask
        onAddTask={handleAddTask}
      />
      <TaskList
        tasks={tasks}
        onChangeTask={handleChangeTask}
        onDeleteTask={handleDeleteTask}
      />
    </>
  );
}

let nextId = 3;
const initialTasks = [
  { id: 0, text: 'Visit Kafka Museum', done: true },
  { id: 1, text: 'Watch a puppet show', done: false },
  { id: 2, text: 'Lennon Wall pic', done: false },
];

```
