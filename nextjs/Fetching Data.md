
## Server Components Fetching data

### `fetch`API 사용
- 컴포넌트를 비동기 함수로 만들고 `fetch` 호출을 `await`
```tsx
// app/blog/page.tsx
export default async function Page() {
  const data = await fetch('https://api.vercel.app/blog')
  const posts = await data.json()
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```
>[!TIP]
>`fetch`응답은 기본적으로 캐시되지 않는다.
>하지만 Next.js는 라우트를 `pre-render`하고 그결과를 캐시해 성능을 향상
>`dynamic rendering`으로 전환하려면 `{ cache: 'no-store' }` 옵션을 사용
>개발 환경에서는 `fetch`호출을 로그로 확인 가능


### ORM 또는 데이터베이스 사용
- 서버 컴포넌트는 서버에서 렌더링 되므로 ORM이나 데이터베이스 클라이언트를 사용해 쿼리할 수 있다.
- 컴포넌트를 비동기 함수로 만들고 호출을 `await`
```tsx
// app/blog/page.tsx
import { db, posts } from '@/lib/db'

export default async function Page() {
  const allPosts = await db.select().from(posts)
  return (
    <ul>
      {allPosts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

## Client Components Fetching data

### `use`API로 데이터 streaming
- React의 `use`API를 사용해 서버에서 클라이언트로 데이터를 stream
- 서버 컴포넌트에서 데이터를 가져오고 -> promise를 클라이언트 컴포넌트에 prop으로 전달
```tsx
// app/blog/page.tsx
import Posts from '@/app/ui/posts'
import { Suspense } from 'react'

export default function Page() {
  // 데이터 fetching 함수를 await하지 않습니다
  const posts = getPosts()

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Posts posts={posts} />
    </Suspense>
  )
}
```

- 클라이언트 컴포넌트에서 `use`API로 promise 읽기

```tsx
// app/ui/posts.tsx
'use client'
import { use } from 'react'

export default function Posts({
  posts,
}: {
  posts: Promise<{ id: string; title: string }[]>
}) {
  const allPosts = use(posts)

  return (
    <ul>
      {allPosts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

> 위 예제에 `<Posts>`컴포넌트는 `<Suspense>`boundary로 감싸져 있으며,
> promise가 resolve 되는 동안 fallback이 표시된다.


### 커뮤니티 라이브러리

- `SWR`이나 `React Query`같은 커뮤니티 라이브러리를 사용할 수 있다.
- 캐싱, streaming등 다양한 기능에 대한 자체적인 semantics를 가지고 있다.

```tsx
// app/blog/page.tsx
'use client'
import useSWR from 'swr'

const fetcher = (url) => fetch(url).then((r) => r.json())

export default function BlogPage() {
  const { data, error, isLoading } = useSWR(
    'https://api.vercel.app/blog',
    fetcher
  )

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <ul>
      {data.map((post: { id: string; title: string }) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

## 요청 중복 제거 및 데이터 캐싱

*Request memoization* - `fetch`요청을 중복 제거하는 한가지 방법

- 단일 렌더 패스 내에 동일한 URL과 옵션으로 이루어진 `GET` 또는 `HEAD` `fetch` 호출이 하나의 요청으로 합쳐진다.
- 자동으로 적용되며, `fetch`에 Abort signal을 전달하면 *opt out*할 수 있다.
- Request memoization의 유효 범위는 해당 요청의 수명으로 한정
- Next.js의 *Data Cache*를 사용해 `fetch`요청을 중복 제거할 수 있다.(Data Cache는 현재 렌더 패스와 이후 요청간에 데이터를 공유)

`fetch`를 사용하지 않고 ORM이나 데이터베이스를 직접 사용하는 경우,

데이터 접근 로직을 React `cache`함수로 감쌀 수 있다.

```ts
// app/lib/data.ts
import { cache } from 'react'
import { db, posts, eq } from '@/lib/db'

export const getPost = cache(async (id: string) => {
  const post = await db.query.posts.findFirst({
    where: eq(posts.id, parseInt(id)),
  })
})
```


## Streaming

초기 로드 시간과 사용자 경험을 개선하기 위해 streaming을 사용할 수 있다.

페이지의 HTML을 더 작은 청크로 분할해 서버에서 클라이언트로 점진적으로 전송하는 방식

### `loading.js`사용

```tsx
// app/blog/loading.tsx
export default function Loading() {
  // 여기에 Loading UI를 정의합니다
  return <div>Loading...</div>
}
```

> 내부적으로 `loading.js`는 `layout.js`안에 중첩되며, 
> `page.js`파일과 그 하위 자식들을 자동으로 `<Suspense> boundary로 감싼다`

>[!TIP]
>더 세분화된 streaming이 필요하다면 `<Suspense>`를 사용할 것


### `<Suspense>`사용

```tsx
// app/blog/page.tsx
import { Suspense } from 'react'
import BlogList from '@/components/BlogList'
import BlogListSkeleton from '@/components/BlogListSkeleton'

export default function BlogPage() {
  return (
    <div>
      {/* 이 콘텐츠는 즉시 클라이언트로 전송됩니다 */}
      <header>
        <h1>Welcome to the Blog</h1>
        <p>Read the latest posts below.</p>
      </header>
      <main>
        {/* 이 boundary 안에 dynamic 콘텐츠가 있으면 stream으로 불러옵니다 */}
        <Suspense fallback={<BlogListSkeleton />}>
          <BlogList />
        </Suspense>
      </main>
    </div>
  )
}
```

>어떤 부분을 stream할지 더 세밀하게 제어 가능

>[!TIP]
>최상의 사용자 경험을 위해 사용자가 이해할 수 있는 의미 있는 로딩 상태를 설계하는 것을 권장 (ex: skeleton, spinner)


## 순차적 데이터 가져오기 (Sequential data fetching)

한 요청의 결과가 다음 요청에 필요할 때 순차적으로 패칭

```tsx
// app/artist/[username]/page.tsx
export default async function Page({ params }) {
  const { username } = await params
  const artist = await getArtist(username)

  return (
    <>
      <h1>{artist.name}</h1>
      {/* artist 데이터 로드 후 Playlists 스트리밍 */}
      <Suspense fallback={<div>Loading...</div>}>
        <Playlists artistID={artist.id} />
      </Suspense>
    </>
  )
}

async function Playlists({ artistID }: { artistID: string }) {
  const playlists = await getArtistPlaylists(artistID)
  return (
    <ul>
      {playlists.map((playlist) => (
        <li key={playlist.id}>{playlist.name}</li>
      ))}
    </ul>
  )
}
```

> `<Suspense>`로 감싸면 artist 데이터를 기다리는 동안 fallback을 보여주고, playlists는 이후에 스트리밍으로 받아올 수 있다.

## 병렬 데이터 가져오기 (Parallel data fetching)

의존 관계가 없는 요청은 동시에 시작해 시간을 단축

```tsx
// ❌ 순차 - getAlbums는 getArtist가 끝날 때까지 블로킹
const artist = await getArtist(username)
const albums = await getAlbums(username)

// ✅ 병렬 - await 없이 먼저 호출, Promise.all로 동시에 resolve
const artistData = getArtist(username)
const albumsData = getAlbums(username)
const [artist, albums] = await Promise.all([artistData, albumsData])
```

> [!WARNING]
>  `Promise.all`은 하나라도 실패하면 전체 실패. 개별 실패를 허용하려면 `Promise.allSettled` 사용

## 데이터 미리 가져오기 (Preloading data)

블로킹 요청보다 먼저 데이터를 미리 시작시키는 패턴

```tsx
// app/item/[id]/page.tsx
export default async function Page({ params }) {
  const { id } = await params

  preload(id) // 데이터 로딩 먼저 시작
  const isAvailable = await checkIsAvailable() // 다른 비동기 작업 수행

  return isAvailable ? <Item id={id} /> : null
}

const preload = (id: string) => {
  void getItem(id) // void: 반환값을 무시하고 즉시 실행
}
```

`server-only` + React `cache`로 재사용 가능한 유틸 함수 만들기

```ts
// utils/get-item.ts
import { cache } from 'react'
import 'server-only'
import { getItem } from '@/lib/data'

export const preload = (id: string) => {
  void getItem(id)
}

export const getItem = cache(async (id: string) => {
  // 동일한 id로 여러번 호출해도 한번만 실행됨
})
```

> `server-only`: 클라이언트 번들에 포함되지 않도록 보장
> `cache`: 동일한 인자로 중복 호출 시 재실행 없이 캐시된 결과 반환
