## 메타데이터

>[!IMPORTANT]
>metadata / generateMetadata
>Next.js는 `metadata`객체(정적)와 `generateMetadata`함수(동적) 두 가지 방식으로 메타데이터를 정의한다.
>모두 **Server Components에서만 지원**되며, Next.js가 자동으로 `<head>` 태그를 생성한다.

- 라우트가 메타데이터를 정의하지 않아도 항상 추가되는 기본 태그 두가지:
	- `<meta charset="utf-8" />` - 문자 인코딩
	- `<meta name="viewport" content="width=device-width, initial-scale=1" />` - 뷰포트

**정적 메타데이터** - `layout.tsx`또는 `page.tsx`에서 `metadata`객체 export

```tsx
// app/blog/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My Blog',
  description: '...',
}
```

**동적 메타데이터** - 데이터 fetch가 필요할 때 `generateMetadata`함수 사용

```tsx
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const slug = (await params).slug;
  const post = await fetch(`https://api.vercel.app/blog/${slug}`).then(res => res.json());
  
  return {
    title: post.title,
    description: post.description,
  }
}
```

>[!TIP]
>메타데이터와 페이지 본문에서 같은 데이터를 fetch해야 한다면,
>React의 `cache`함수로 메모이제이션하면 요청이 한 번만 실행된다.

>[!NOTE]
>동적 렌더링 페이지에서 Next.js는 메타데이터를 별도로 스트리밍한다.
>`generateMetadata`가 resolve되면 `<head>`에 주입하며, UI 렌더링을 블로킹하지 않는다.
>단, 봇/크롤러(`Twitterbot`, `Slackbot`등)에는 스트리밍 메타데이터가 비활성화된다.

---

## 파일 기반 메타데이터

>[!IMPORTANT]
>파일 기반 메타데이터 컨벤션
>특수 파일명을 `app`폴더에 배치하는 것만으로 메타데이터가 자동 적용된다.

- `favicon.ico` - 브라우저 탭/북마크 아이콘
- `opengraph-image.jpg`/`twitter-image.jpg` - SNS 공유 이미지
- `robots.txt` - 크롤러 접근 제어
- `sitemap.xml` - 검색엔진 사이트맵

>더 하위 폴더에 배치한 이미지가 우선순위를 가진다.
>예 `/blog/opengraph-image.jpg`는 루트의 OG이미지보다 `/blog`경로에서 우선 적용됨

---

## 동적 OG 이미지 생성

>[!IMPORTANT]
>ImageResponse / opengraph-image.tsx
>`ImageResponse`생성자를 사용하면 JSX와 CSS로 동적 OG 이미지를 생성할 수 있다.
>데이터에 따라 달라지는 OG 이미지(예 블로그 포스트마다 다른 제목)에 유용하다.

```tsx
// app/blog/[slug]/opengraph-image.tsx
import { ImageResponse } from 'next/og'
import { getPost } from '@/app/lib/data'

export const size = { width: 1200, height: 630 }
export const contentType = 'image/png'

export default async function Image({ params } : { params: { slug: string }}) {
  const post = await getPost(params.slug);
  
  return new ImageResponse(
    <div style={{ fontSize: 128, background: 'white', width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
    {post.title}
    </div>
  )
}
```
