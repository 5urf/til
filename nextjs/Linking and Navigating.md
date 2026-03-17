> Next.js 네비게이션은 기본적으로 서버 렌더링이다.  
> prefetching / streaming / client-side transitions 세 가지가 조합되어 체감 속도를 만든다.

---

## 기본 동작 방식

Layouts와 Pages는 기본적으로 **React Server Components**다.  
초기 방문과 이후 네비게이션 모두 서버에서 RSC Payload를 생성해 클라이언트에 전송한다.  
클라이언트는 서버 응답을 기다리는 대기 시간이 생기고, 아래 세 가지가 이를 해결한다.

```
prefetching         - 클릭 전에 미리 로딩
streaming           - 준비된 부분부터 순차 전송
client-side transitions - 페이지 전체 리로드 없이 부분 교체
```

---

## prefetching - 뷰포트 진입 시 자동 실행

`<Link>`로 연결된 라우트가 뷰포트에 진입하는 순간 백그라운드에서 자동 prefetch한다.  
`<a>` 태그는 클릭 시점에 서버 요청이 시작된다.

```tsx
<Link href="/blog">Blog</Link>  // prefetch 자동 적용
<a href="/contact">Contact</a>  // prefetch 없음
```

라우트 유형별 prefetch 범위:

| 라우트 유형   | loading.tsx 없음 | loading.tsx 있음                         |
| ------------- | ---------------- | ---------------------------------------- |
| static route  | 전체 prefetch    | 전체 prefetch                            |
| dynamic route | skip             | shared layout + skeleton만 부분 prefetch |

> [!TIP]
> dynamic route에 `loading.tsx`가 없으면 prefetch 자체가 skip된다.  
> dynamic route를 쓴다면 `loading.tsx`를 기본값으로 추가하는 습관이 필요하다.

링크가 대량으로 존재하는 경우(무한 스크롤 등) hover 시에만 prefetch하는 패턴으로 리소스를 절약할 수 있다.

```tsx
// 완전 비활성화
<Link prefetch={false} href='/blog'>
  Blog
</Link>;

// hover 시에만 prefetch
function HoverPrefetchLink({ href, children }) {
  const [active, setActive] = useState(false);

  return (
    <Link
      href={href}
      prefetch={active ? null : false}
      onMouseEnter={() => setActive(true)}
    >
      {children}
    </Link>
  );
}
```

---

## streaming - loading.tsx 추가만으로 활성화

서버가 dynamic route의 준비된 부분을 전체 렌더링을 기다리지 않고 순차 전송하는 방식.  
`loading.tsx`를 route 폴더에 추가하면 Next.js가 내부적으로 `page.tsx`를 `<Suspense>` boundary로 자동 감싼다.

```
app/dashboard/
├── loading.tsx   - 이것만 추가하면 streaming 활성화
└── page.tsx
```

```tsx
// loading.tsx
export default function Loading() {
  return <LoadingSkeleton />;
}
```

prefetch된 skeleton이 먼저 표시되고, 실제 콘텐츠가 준비되면 교체된다.  
TTFB / FCP / TTI 등 Core Web Vitals가 개선된다.

---

## client-side transitions - 페이지 부분 교체

|           | `<a>` 태그         | `<Link>` 컴포넌트     |
| --------- | ------------------ | --------------------- |
| 이동 방식 | 전체 페이지 리로드 | 변경된 부분만 교체    |
| 상태 유지 | ❌ 초기화          | ✅ shared layout 유지 |
| 스크롤    | 리셋               | 유지                  |

prefetching + streaming과 결합되면 dynamic route도 즉각적인 전환이 가능해진다.

---

## 네비게이션이 느린 원인 4가지

**1. loading.tsx 누락**

dynamic route에 `loading.tsx`가 없으면 서버 응답 대기 중 아무 피드백이 없어 앱이 멈춘 것처럼 느껴진다.

**2. generateStaticParams 미적용**

`[slug]` 같은 dynamic segment에 `generateStaticParams`를 추가하면 빌드 타임에 정적 생성된다.  
없으면 매 요청마다 dynamic rendering으로 폴백되어 전환이 느려진다.

```tsx
export async function generateStaticParams() {
  const posts = await fetch("https://.../posts").then((res) => res.json());

  return posts.map((post) => ({
    slug: post.slug,
  }));
}
```

**3. 느린 네트워크 - useLinkStatus로 피드백 제공**

느린 네트워크에서는 prefetch가 클릭 전에 완료되지 않아 skeleton조차 즉시 표시되지 않을 수 있다.  
`useLinkStatus`의 `pending`으로 전환 진행 중임을 알릴 수 있다.  
초기 animation delay(예: 100ms)를 주면 빠른 네트워크에서는 인디케이터가 노출되지 않아 UX가 자연스럽다.

```tsx
"use client";

import { useLinkStatus } from "next/link";

export default function LoadingIndicator() {
  const { pending } = useLinkStatus();
  return <span className={`link-hint ${pending ? "is-pending" : ""}`} />;
}
```

**4. Hydration not completed**

`<Link>`는 Client Component이므로 hydration 완료 이후에야 prefetch를 시작할 수 있다.  
JS 번들이 크면 hydration이 지연되어 prefetch 시작 자체가 늦어진다.

> [!TIP]
> `@next/bundle-analyzer`로 번들 크기를 줄이거나, 클라이언트 로직을 서버 컴포넌트로 이동하는 방식으로 개선할 수 있다.
