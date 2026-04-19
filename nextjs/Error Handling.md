## 에러의 두가지 분류

>[!IMPORTANT]
>Expected Error vs Uncaught Exception
>Next.js에서 에러는 두가지로 나뉜다.
>**예상 가능한 에러**(폼 검증 실패, 요청 실패 등)는 반환값으로 처리하고,
>**예상치 못한 에러**(버그)는 에러 바운더리가 잡아낸다.

---

## 예상 가능한 에러 처리

>[!IMPORTANT]
>useActionState
>Server Function에서 예상 가능한 에러는 `try/catch`로 throw하지 말고,
>에러 메시지를 **반환값으로 모델링**한다.
>`useActionState`훅으로 반환된 `state`를 읽어 UI에 에러를 표시한다.

```tsx
// Server Function - 에러를 throw하지 않고 반환값으로 처리
'use server'
export async function createPost(prevState: any, formData: FormData) {
  const res = await fetch('https://api.vercel.app/posts/', {
    method: 'POST',
    body: { title: formData.get('title') },
  })
  
  if(!res.ok) {
    return { message: 'Failed to create post' } // throw가 아닌 return
  }
}
```
>[!WARNING]
>Server Function에서 예상 가능한 에러에 `try/catch`를 쓰면 에러 바운더리가 잡아 버린다.
>의도한 에러 메시지 표시 대신 fallback UI가 렌더링될 수 있으므로, 반환값 패턴을 사용할 것.

---
## not-found 처리

>[!IMPORTANT]
>notFound() / not-found.tsx
>`notFound()`함수를 호출하면 해당 라우트 세그먼트의 `not-found.tsx`파일이 404 UI로 렌더링 된다.

```tsx
// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation'

export default async function Page({ params } : { params: Promise<{ slug: string}> }) {
  const { slug } = await params;
  const post = getPostBySlug(slug);
  
  if (!post) notFound() // not-found.tsx가 렌더링 됨
  
  return <div>{post.title}</div>
}
```

---

## 예상치 못한 에러 처리 (에러 바운더리)

>[!IMPORTANT]
>error.tsx / 에러 바운더리
>라우트 세그먼트에 `error.tsx`파일을 만들면 해당 세그먼트의 에러 바운더리 역할을 한다.
>에러는 가장 가까운 상위 에러 바운더리로 버블링되므로,
>라우트 계층 구조의 여러 레벨에 배치해 세분화된 에러 처리가 가능하다.

```tsx
// app/dashboard/error.tsx
'use client' // 에러 바운더리는 반드시 Client Component

export default function Errorpage({
  error,
  unstable_retry,
}: {
  error: Error & { digest?: string }
  unstable_retry: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => unstable_retry()}>Try again</button>
    </div>
  )
}
```

>[!WARNING]
>에러 바운더리는 렌더링 중 발생한 에러만 잡는다.
>이벤트 핸들러나 비동기 코드의 에러는 잡지 못하므로, 이경우 직접 `try/catch` + `useState`로 처리해야 한다.

>[!TIP]
>`useTransition`의 `startTransition`안에서 throw된 에러는 에러 바운더리로 버블링 된다.
>이벤트 핸들러 에러와 다르게 동작하는 점에 주목


---

## 전역 에러 처리

>[!IMPORTANT]
>global-error.tsx
>루트 레이아웃의 에러를 잡으려면 `app/global-error.tsx`를 사용한다.
>루트 레이아웃을 대체하므로, 반드시 자체적으로 `<html>`과 `<body>`태그를 포함해야 한다.

```tsx
// app/global-error.tsx
'use client'

export default function GlobalError({ error, unstable_retry }) {
  return (
    <html>
      <body>
        <h2>Something went wrong!</h2>
        <button onClick={() => unstable_retry()}>Try again</button>
      </body>
    </html>
  )
}
```

>[!NOTE]
>`error.tsx`는 같은 세그먼트의 `layout.tsx`에러를 잡지 못한다.
>layout 에러는 상위 세그먼트의 `error.tsx`가 잡는다.
>루트 layout 에러만 `global-error.tsx`가 담당한다.
