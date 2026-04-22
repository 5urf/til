## fetch 캐싱

>[!IMPORTANT]
>fetch 캐시 옵션
>
>기본적으로 `fetch` 요청은 캐시되지 않는다.
>
>`cache: 'force-cache'`를 설정하면 해당 요청의 결과를 캐시한다.

```tsx
// 캐시 적용
const data = await fetch('https://...', { cache: 'force-cache'})

// 캐시 비적용 (기본값)
const data = await fetch('https://...', { cache: 'no-store' })
```

- `fetch`를 사용하지 않는 DB쿼리 등은 `unstable_cache`로 캐시할 수 있다.

```tsx
import { unstable_cache } from 'next/cache'

export const getCachedUser = unstable_cache(
  async (id: string) => {
    return db.select().from(users).where(eq(users.id, id))
  },
  ['user'], // 캐시 키 프리픽스
  { tags: ['user'], revalidate: 3600}
)
```

---

## Route Segment Config

>[!IMPORTANT]
>dynamic / revalidate
>
>라우트 레벨에서 캐시 동작을 제어하는 설정값이다.
>
>`dynamic`은 렌더링 방식을, `revalidate`는 재검증 주기(초)를 지정한다.

```tsx
// layout.tsx | page.tsx | route.ts
export const dynamic = 'auto'
// 'auto' | 'force-dynamic' | 'error' | 'force-static'

export const revalidate = 3600 // 1시간마다 재검증
```

- `'auto'`(기본값): 가능한 많이 캐시하되, 동적 동작을 막지 않음
- `'force-dynamic'`: 매 요청마다 동적 렌더링 강제
- `'force-static'`: 정적 렌더링 강제, `cookies()`/ `headers()`등은 빈 값 반환

>[!WARNING]
>같은 라우트의 여러 세그먼트에 `revalidate`를 설정하면 **가장 낮은 값**이 라우트 전체에 적용된다.
>
>개별 `fetch`에 더 낮은 `revalidate`를 설정하면 라우트 전체의 재검증 주기도 그에 맞춰진다.

---

## 온디맨드 재검증

>[!IMPORTANT]
>revalidateTag / revalidatePath
>
>이벤트 발생 후 캐시를 즉시 무효화하는 두 가지 방법이다.
>
>`revalidateTag`는 태그 기반으로 여러 페이지에 걸쳐 무효화하고,
>
>`revalidatePath`는 특정 경로의 캐시를 무효화한다.

```tsx
// fetch에 태그 부여
const data = await fetch('https://...', { next: { tags: ['user'] } })

// Server Action 또는 Route Handler에서 무효화
import { revalidateTag } from 'next/cache'
revalidateTag('user') // 'user' 태그가 붙은 모든 캐시 무효화

import { revalidatePath } from 'next/cache'
revalidatePath('/profile') // /profile 경로 캐시 무효화
```

>[!TIP]
>태그 기반 무효화(`revalidateTag`)가 더 정밀하다.
>
>`revalidatePath`는 어떤 태그가 연관됐는지 모를 때 경로 전체를 무효화하는 수단으로 사용한다.

---

## 중복 요청 제거

>`fetch`는 렌더링 중 자동으로 메모이제이션된다.
>
>`fetch`를 사용하지 않는 경우 React의 `cache`함수로 중복 요청을 제거할 수 있다.

```tsx
import { cache } from 'react'

export const getPost = cache(async (id: string) => {
  return db.query.posts.findFirst({ where: eq(posts.id, parseInt(id)) })
})
// 같은 렌더링 패스에서 getPost(id)를 여러 번 호출해도 DB 요청은 1번만 실행
```
