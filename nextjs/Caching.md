>캐싱은 데이터 패칭과 기타 연산 결과를 저장해두고, 이후 동일한 요청에 대해 작업을 다시 수행하지 않고
>더 빠르게 응답할 수 있도록 하는 기법

---

## Cache Components 활성화

```ts
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

>캐시 컴포넌트가 활성화되면 `GET` 라우트 핸들러도 페이지와 동일한 사전 렌더링 모델을 따른다

---

## 사용법

`use cache`디렉티브는 비동기 함수와 컴포넌트의 반환값을 캐싱

- 데이터 레벨: 데이터를 패칭하거나 계산하는 함수를 캐싱(`getProducts()`, `getUser(id)`)
- UI 레벨: 컴포넌트 전체 또는 페이지를 캐싱 (`async function BlogPosts()`)

>인수와 부모 스코프에서 클로저로 참조된 값은 자동으로 캐시 키의 일부가 된다.
>서로 다른 입력값은 별도의 캐시 항목을 생성
>이를 통해 개인화되거나 파라미터화된 캐시 콘텐츠가 가능

### 데이터 레벨 캐싱

데이터를 패칭하는 비동기 함수를 캐싱하려면, 함수 본문 맨 위에 `use cache`디렉티브를 추가

```ts
// app/lib/data.ts
import { cacheLife } from 'next/cache'

export async function getUsers() {
  'use cache'
  cacheLife('hours')
  return db.query('SELECT * FROM users')
}
```

>동일한 데이터가 여러 컴포넌트에서 사용될때, UI와 독립적으로 데이터를 캐싱하고 싶을때 유용

>[!IMPORTANT]
>`cacheTag`는 `'use cache'`와 함께 사용해야 의미가 있다.
>`fetch`없이 DB 쿼리나 파일 시스템처럼 서버 사이드 연산도 `'use cache'` + `cacheTag()`를 조합하면
>태그 기반 캐싱이 가능하다. `unstable_cache`의 대체재

```ts
import { cacheLife, cacheTag } from 'next/cache'

export async function getProducts() {
  'use cache'
  cacheTag('products')   // 이 태그로 나중에 revalidateTag('products') 호출 가능
  cacheLife('hours')
  return db.query('SELECT * FROM products')
}
```


### UI 레벨 캐싱

전체(컴포넌트, 페이지, 레이아웃)를 캐싱하려면 컴포넌트 또는 본문 맨 위에 `use cache`를 추가

```tsx
// app/page.tsx
import { cacheLife } from 'next/cache'

export default async function Page() {
  'use cache'
  cacheLife('hours')

  const users = await db.query('SELECT * FROM users')

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```
>해당 파일에서 export된 모든 함수가 캐싱

### 캐싱하지 않는 데이터 스트리밍

>요청마다 최신 데이터가 필요한 컴포넌트에는 `use cache`를 사용하지 말것
>대신 `<Suspense>`로 감싸고 폴백 UI를 제공
>폴백 렌더링 -> 비동기 작업이 완료되면 실제 콘텐츠 스트리밍

```tsx
// page.tsx
import { Suspense } from 'react'

async function LatestPosts() {
  const data = await fetch('https://api.example.com/posts')
  const posts = await data.json()
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}

export default function Page() {
  return (
    <>
      <h1>My Blog</h1>
      <Suspense fallback={<p>Loading posts...</p>}>
        <LatestPosts />
      </Suspense>
    </>
  )
}
```

>[!IMPORTANT]
>캐시/재검증 기본: `fetch`의 기본값은 캐시하지 않는다.
>`'use cache'`없이 작성된 비동기 컴포넌트는 매 요청마다 새로 실행된다.

---

## 런타임 API 다루기

- 런타임 API
	- `cookies` - 사용자의 쿠키 데이터
	- `headers` - 요청 헤더
	- `searchParams` - URL 쿼리 파라미터
	- `params` - 동적 라우트 파라미터

런타임 API에 접근하는 컴포넌트는 `<Suspense>`로 감싸야 한다.

```tsx
// page.tsx
import { cookies } from 'next/headers'
import { Suspense } from 'react'

async function UserGreeting() {
  const cookieStore = await cookies()
  const theme = cookieStore.get('theme')?.value || 'light'
  return <p>Your theme: {theme}</p>
}

export default function Page() {
  return (
    <>
      <h1>Dashboard</h1>
      <Suspense fallback={<p>Loading...</p>}>
        <UserGreeting />
      </Suspense>
    </>
  )
}
```

### 캐싱된 함수에 런타임 값 전달하기

런타임 API에서 값을 추출해 캐싱된 함수에 인수로 전달할 수 있다.

```tsx
// app/profile/page.tsx
import { cookies } from 'next/headers'
import { Suspense } from 'react'

export default function Page() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <ProfileContent />
    </Suspense>
  )
}

// 캐싱되지 않은 컴포넌트가 런타임 데이터를 읽음
async function ProfileContent() {
  const session = (await cookies()).get('session')?.value
  return <CachedContent sessionId={session} />
}

// 캐싱된 컴포넌트는 추출된 값을 prop으로 받음
async function CachedContent({ sessionId }: { sessionId: string }) {
  'use cache'
  // sessionId가 캐시 키의 일부가 됨
  const data = await fetchUserData(sessionId)
  return <div>{data}</div>
}
```

>요청 시점에 일치하는 캐시 항목이 없으면 `CachedContent`가 실행되고, 동일한 `sessionId`를 가진 이후 요청을 위해 결과가 저장된다.

---

## 비결정적 연산 다루기

>캐시 컴포넌트는  같은 연산은 실행할 때마다 다른 값을 생성 하는 연산을 명시적으로 처리하도록 요구한다.
>(ex: `Math.random()`, `Date.now()`, `crypto.randomUUID()`)
>**요청마다 고유한 값을 생성하려면**, 연산 전에 `connection()`을 호출하고 컴포넌트를 `<Suspense>`로 감싸야한다.


```tsx
// page.tsx
import { connection } from 'next/server'
import { Suspense } from 'react'

async function UniqueContent() {
  await connection()
  const uuid = crypto.randomUUID()
  return <p>Request ID: {uuid}</p>
}

export default function Page() {
  return (
    <Suspense fallback={<p>Loading...</p>}>
      <UniqueContent />
    </Suspense>
  )
}
```

반대로 모든 사용자가 재검증 전까지 동일한 값을 보도록 결과를 캐싱할 수 있다

```tsx
export default async function Page() {
  'use cache'
  const buildId = crypto.randomUUID()
  return <p>Build ID: {buildId}</p>
}
```

---

## 결정적 연산 다루기

>동기 I/O, 모듈 임포트, 순수 계산 같은 연산은 사전 렌더링 중에 완료될 수 있다.
>이러한 연산만 사용하는 컴포넌트의 렌더링 결과는 자동으로 정적 HTML 셸에 포함된다.

```tsx
// page.tsx
import fs from 'node:fs'

export default async function Page() {
  const content = fs.readFileSync('./config.json', 'utf-8')
  const constants = await import('./constants.json')
  const processed = JSON.parse(content).items.map((item) => item.value * 2)

  return (
    <div>
      <h1>{constants.appName}</h1>
      <ul>
        {processed.map((value, i) => (
          <li key={i}>{value}</li>
        ))}
      </ul>
    </div>
  )
}
```

---

## 렌더링 동작 방식

>빌드 시점에 Next.js는 라우트의 컴포넌트 트리를 렌더링한다.
>각 컴포넌트의 처리 방식은 사용하는 API에 따라 달라진다.

- `use cache`: 결과가 캐싱되고 정적 셸에 포함됨
- `<Suspense>`: 폴백 UI가 정적 셸에 포함되고, 콘텐츠는 요청 시점에 스트리밍됨
- 결정적 연산: 순수 계산, 모듈 임포트 등은 자동으로 정적 셸에 포함됨

>이를 통해 정적 셸이 생성되는데, 초기 페이지 로드를 위한 HTML과 클라이언트 사이드 내비게이션을 위해 직렬화된 RSC Payload로 구성된다.
>사용자가 URL에 직접 접근하든 다른 페이지에서 전환하든 브라우저는 즉시 완전히 렌더링된 콘텐츠를 받는다.
>이 렌더링 방식을 **Partial Prerendering(PPR)**이라고 하며, 캐시 컴포넌트의 기본 동작이다.

### 정적 셸 비활성화하기

루트 레이아웃 문서 본문 위에 폴백이 빈 `<Suspense>`경계를 배치하면, 앱 전체가 요청 시점으로 지연된다.

```tsx
// app/layout.tsx
import { Suspense } from 'react'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html>
      <Suspense fallback={null}>
        <body>{children}</body>
      </Suspense>
    </html>
  )
}
```

>특정 라우트에만 이를 적용하려면 여러 루트 레이아웃을 사용할 것

### 모든 것을 합쳐보면

>[!IMPORTANT]
>`cacheTag`로 태그를 붙이고, `updateTag`(Server Action) 또는 `revalidateTag`(Route Handler / Server Action)로 무효화 한다. `revalidatePath`는 태그대신 경로 단위로 재검증 한다.

```tsx
import { cacheLife, cacheTag, updateTag } from 'next/cache'

// 모든 사용자가 동일한 블로그 글을 봄 (매 시간 재검증)
async function BlogPosts() {
  'use cache'
  cacheLife('hours')
  cacheTag('posts')       // ← cacheTag: 이 캐시에 'posts' 태그 부착

  const res = await fetch('https://api.vercel.app/blog')
  const posts = await res.json()
  return (
    <ul>
      {posts.slice(0, 5).map((post: any) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}

// 관리자 전용 - 게시글 생성 후 캐시 즉시 만료
async function CreatePost() {
  async function createPost(formData: FormData) {
    'use server'
    await db.post.create({ data: { title: formData.get('title') } })
    updateTag('posts')    // ← updateTag: Server Action에서만, 'posts' 태그 즉시 만료
    // revalidatePath('/blog')  ← revalidatePath: 경로 단위로 재검증할 때 사용
  }

  return (
    <form action={createPost}>
      <input name="title" placeholder="Post title" required />
      <button type="submit">Publish</button>
    </form>
  )
}
```

>관리자가 새 게시글을 발행하면 `updateTag('posts')` 호출이 `cacheTag('posts')`가 붙어있는 캐시를 즉시 만료시켜, 다음 방문자가 최신 글을 볼 수 있게 된다.
