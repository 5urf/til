기본적으로 레이아웃과 페이지는 Server Compnents다.

상호작용이나 브라우저 API가 필요한 경우에는 Client components를 사용

## Use Client Components
- 상태 및 이벤트 핸들러 (`onClick`, `onChange`)
- 라이프사이클 로직 (`useEffect`)
- 브라우저 전용 API(`localStorage`, `window`,`Navigator.geolocation`)
- 커스텀 훅

## Use Server Components
- 소스에 가까운 데이터베이스나 API에서 데이터 가져오기
- API 키, 토큰 등 민감한 정보를 클라이언트에 노출하지 않고 사용하기
- 브라우저로 전송되는 JavaScript 양 줄이기
- 첫번째 콘텐츠 페인트(FCP) 개선 및 콘텐츠 점진적 스트리밍

## Next.js에서 서버 및 클라이언트 컴포넌트는 어떻게 동작할까?
### Server Components
- **React Server Component Payload(RSC Payload)** 라는 특수 데이터 형식으로 렌더링된다.

### Client Components 와 RSC Payload
- HTML을 사전 렌더링하는데 사용된다.

## React Server Component Payload(RSC)란?

RSC Payload는 렌더링된 React 서버 컴포넌트 트리의 압축된 바이너리 표현

클라이언트에서 React가 브라우저의 DOM을 업데이트하는 데 사용

RSC Payload에는 다음이 포함된다.

- 서버 컴포넌트의 렌더링 결과
- 클라이언트 컴포넌트가 렌더링될 위치의 플레이스홀더 및 해당 JavaScript 파일 참조
- 서버 컴포넌트에서 클라이언트 컴포넌트로 전달된 모든 props

## 클라이언트 첫 로드 흐름
1. HTML -> 빠른 비인터렉티브 미리보기
2. RSC Payload -> 서버/클라이언트 컴포넌트 트리 조정
3. JavaScript -> 클라이언트 컴포넌트 하이드레이션, 인터렉티브 하게

>[!TIP]
>하이드레이션이란?
>하이드레이션은 React가 정적 HTML을 인터렉티브하게 만들기 위해 이벤트 헨들러를 DOM에 연결하는 과정

### 이후 탐색
- RSC Payload가 프리페치 및 캐시되어 즉각적인 탐색이 가능
- 클라이언트 컴포넌트는 서버 렌더링 HTML 없이 완전히 클라이언트에서 렌더링 된다.


## JS 번들 크기 줄이기

특정 인터렉티브 컴포넌트에만 `use client`를 추가

```ts
// Client Component
import Search from './search'
// Server Component
import Logo from './logo'
 
// Layout is a Server Component by default
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <nav>
        <Logo />
        <Search />
      </nav>
      <main>{children}</main>
    </>
  )
}
```

## 서버에서 클라이언트 컴포넌트로 데이터 전달하기

props를 사용하여 서버 컴포넌트 -> 클라이언트 컴포넌트로 데이터 전달 가능

```ts
import LikeButton from '@/app/ui/like-button'
import { getPost } from '@/lib/data'

export default async function Page({ params }) {
  const { id } = await params
  const post = await getPost(id)
  return <LikeButton likes={post.likes} />
```

또는 `use`API를 사용하여 서버 컴포넌트 -> 클라이언트 컴포넌트로 데이터 스트리밍도 가능

>[!TIP]
>클라이언트 컴포넌트에 전달되는 Props는 React에 의해 [직렬화](https://ko.react.dev/reference/rsc/use-server#serializable-parameters-and-return-values) 가능해야 한다

### 서버 컴포넌트와 클라이언트 컴포넌트 혼합 사용

서버 컴포넌트 -> 클라이언트 컴포넌트의 prop으로 전달 가능

일반적인 패턴은 `children`을 사용하여 `<ClientComponent>` 내에 슬롯을 만드는 것

```ts
'use client'
 
export default function Modal({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>
}
```

서버에서 데이터를 가져오는 `<Cart>` 컴포넌트를 클라이언트 상태로 가시성을 토글하는 `<Modal>` 컴포넌트 내에 배치 가능

```ts
import Modal from './ui/modal'
import Cart from './ui/cart'
 
export default function Page() {
  return (
    <Modal>
      <Cart />
    </Modal>
  )
}
```


## 컨텍스트 프로바이더

React Context는 서버 컴포넌트에서 지원되지 않는다.

컨텍스트 프로바이더를 `use client`로 만들고 서버 컴포넌트인 `layout`에서 감싸는 패턴을 사용

```ts
'use client'
 
import { createContext } from 'react'
 
export const ThemeContext = createContext({})
 
export default function ThemeProvider({
  children,
}: {
  children: React.ReactNode
}) {
  return <ThemeContext.Provider value="dark">{children}</ThemeContext.Provider>
}
```

`ThemeProvider`가 전체 `<html>` 문서 대신 `{children}`만 감싸는 것에 주목

```ts
import ThemeProvider from './theme-provider'
 
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  )
}
```

이렇게 하면 Next.js가 서버 컴포넌트의 정적 부분을 더 쉽게 최적화할 수 있다.

>[!TIP] 
>프로바이더는 트리에서 가능한 깊은 곳에 두는게 최적화에 유리하다.

## environment poisoning 방지

서버 전용 코드가 클라이언트로 새는 것을 막으려면 `server-only` 패키지를 import

```ts
import 'server-only'
 
export async function getData() {
  const res = await fetch('https://external-service.com/data', {
    headers: {
      authorization: process.env.API_KEY,
    },
  })
 
  return res.json()
}
```

`NEXT_PUBLIC`접두사 없는 환경변수는 클라이언트에서 빈 문자열로 대체된다.
