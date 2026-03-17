> Next.js 라우팅은 파일 시스템 기반이다.  
> 폴더가 URL 세그먼트를 정의하고, `page.tsx`가 있어야 비로소 외부에 공개된다.

---

## 파일 시스템 기반 라우팅

```
app/
├── layout.tsx           → 루트 레이아웃 (필수, <html> / <body> 포함)
├── page.tsx             → /
├── blog/
│   ├── layout.tsx       → /blog 전용 레이아웃
│   ├── page.tsx         → /blog
│   └── [slug]/
│       └── page.tsx     → /blog/:slug
```

폴더만 있고 `page.tsx`가 없으면 라우트로 공개되지 않는다.

---

## page.tsx vs layout.tsx

| 파일         | 역할                      | 네비게이션 시     |
| ------------ | ------------------------- | ----------------- |
| `page.tsx`   | 특정 라우트에서만 렌더링  | 매번 렌더링       |
| `layout.tsx` | 여러 페이지가 공유하는 UI | **리렌더링 없음** |

레이아웃은 네비게이션 시 리렌더링되지 않는다. 상태와 인터랙션을 유지한 채 자식 페이지만 교체된다.

레이아웃 중첩 구조:

```
app/layout.tsx           → 루트 레이아웃
└── app/blog/layout.tsx  → 블로그 레이아웃
    └── app/blog/page.tsx
```

---

## 동적 세그먼트 - `[slug]`

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPostPage({
  params,
}: {
  params: Promise<{ slug: string }>; // params는 Promise
}) {
  const { slug } = await params; // 반드시 await 필요
  // ...
}
```

> [!WARNING]
> `params`는 Promise다. `await` 없이 구조 분해하면 타입 에러가 발생한다.

---

## searchParams - 상황에 따라 다르게 읽는다

| 상황                | 방법                                          | 주의                   |
| ------------------- | --------------------------------------------- | ---------------------- |
| 서버 컴포넌트       | `searchParams` prop                           | 동적 렌더링으로 전환됨 |
| 클라이언트 컴포넌트 | `useSearchParams()`                           | -                      |
| 이벤트 핸들러 내부  | `new URLSearchParams(window.location.search)` | 리렌더링 없이 읽기     |

```tsx
// 서버 컴포넌트 - searchParams 사용 시 동적 렌더링 전환
export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ query?: string }>;
}) {
  const { query } = await searchParams;
  // ...
}
```

> [!WARNING]
> 서버 컴포넌트에서 `searchParams`를 쓰는 순간 해당 페이지는 동적 렌더링으로 전환된다.  
> 요청 시점의 URL을 읽어야 하므로 빌드 시점 정적 생성이 불가능하다.  
> 필터링 UI 같은 경우 성능 영향을 고려해야 한다.

---

## Link 컴포넌트

`<a>` 태그를 확장한 Next.js 내장 컴포넌트. prefetching과 클라이언트 사이드 네비게이션을 기본으로 제공한다.

```tsx
import Link from 'next/link'

<Link href="/blog">블로그</Link>         // 기본 이동
<Link href={`/blog/${slug}`}>포스트</Link> // 동적 경로
```

고급 네비게이션(조건부 이동, 이벤트 후 이동)이 필요할 때는 `useRouter`를 사용한다.
