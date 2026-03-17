> React는 컴포넌트 관계를 트리 구조로 모델링한다.  
> 렌더 트리(런타임)와 모듈 의존성 트리(빌드타임)는 서로 다른 기준을 가진다.

---

## 렌더 트리 (Render Tree)

런타임에 컴포넌트가 어떻게 중첩되는지를 나타내는 트리.

```
App                          ← 최상위(root) 컴포넌트
├── Layout
│   ├── Header
│   └── Nav
│       └── NavItem          ← 리프 컴포넌트 (자식 없음)
└── Page
    ├── PostList
    │   └── PostCard         ← 리프 컴포넌트
    └── Sidebar
        └── TagList          ← 리프 컴포넌트
```

- **최상위 컴포넌트**: 트리 루트에 가까울수록 하위 전체 렌더링에 영향
- **리프 컴포넌트**: 자식이 없어 상태 변화에 가장 자주 리렌더링됨

> [!WARNING]
> 무거운 연산(heavy computation)을 리프 컴포넌트에 두면 리렌더링 비용이 높아진다.  
> `useMemo` / `React.memo` 등으로 메모이제이션하거나, 연산을 상위로 올리는 걸 고려할 것.

> [!WARNING]
> 반대로 상태를 최상위에 몰아두면 하위 전체가 리렌더링된다.  
> **상태 위치(state colocation)** 가 성능과 직결된다.

---

## 모듈 의존성 트리 (Module Dependency Tree)

빌드타임에 `import` 관계를 기반으로 만들어지는 트리.  
번들러는 이 트리를 보고 필요한 모듈만 골라 번들링한다.

```
App.tsx
├── Layout.tsx
│   └── Header.tsx
├── Page.tsx
│   ├── PostList.tsx
│   │   └── PostCard.tsx
│   └── Sidebar.tsx
│       └── TagList.tsx
└── utils/format.ts          ← 컴포넌트가 아닌 모듈도 포함
```

> [!TIP]
> 앱이 커질수록 번들 크기도 커진다.  
> 의존성 트리를 파악하면 번들 비대화 원인을 디버깅하기 쉽다.  
> `webpack-bundle-analyzer` 또는 `vite-plugin-visualizer` 활용을 추천.

---

## 렌더 트리 vs 의존성 트리 — `children` props 케이스

`children`으로 컴포넌트를 주입하면 두 트리의 구조가 달라진다.

```tsx
// Parent.tsx — children을 직접 import하지 않음
const Parent = ({ children }: { children: React.ReactNode }) => (
  <div>{children}</div>
);

// App.tsx
import Parent from "./Parent";
import Child from "./Child"; // Child를 import하는 건 App

const App = () => (
  <Parent>
    <Child /> // 런타임엔 Parent 아래에 렌더링됨
  </Parent>
);
```

```
# 렌더 트리 (런타임 기준)       # 의존성 트리 (import 기준)
App                             App
└── Parent                      ├── Parent   ← Child 의존 없음
    └── Child                   └── Child
```

| 기준        | 트리        | Child의 부모 |
| ----------- | ----------- | ------------ |
| 런타임 중첩 | 렌더 트리   | Parent       |
| import 관계 | 의존성 트리 | App          |

> [!TIP]
> `children` 패턴은 의존성 역전(dependency inversion)처럼 동작한다.  
> Parent가 Child를 모르기 때문에, Parent 변경이 Child 번들에 영향을 주지 않는다.
