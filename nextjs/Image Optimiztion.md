## next/image 컴포넌트

>[!IMPORTANT]
>`next/image`
>
>HTML `<img>`를 확장한 컴포넌트로, 사이즈 최적화 / CLS 방지 / lazy loading / 포맷 변환을 자동 처리한다.
>
>(WebP 등 최신 포맷 자동 변환, 뷰포트 진입 시점에 lazy load, 레이아웃 시프트 방지가 내장되어 있다.)

```tsx
import Image from 'next/image'

export default function Page() {
  return <Image src="..." alt="..." />
}
```

---

## 로컬 이미지

>로컬이미지는 static import `public/`폴더 또는 파일을 직접 import해서 사용할 수 있다.

>[!IMPORTANT]
>파일을 `import`로 불러오면 `width`, `height`, `blurDataURL`이 자동 제공된다.
>
>문자열 경로(`"/profile.png"`)를 쓸 경우 `width`와 `height`를 직접 명시해야 한다.

```tsx
// ✅ static import - width/height 자동
import ProfileImage from './profile.png'
return <Image src={ProfileImage} alt="프로필" />

// ✅ 문자열 경로 - width/height 직접 명시 필요
return <Image src="/profile.png" alt="프로필" width={500} height={500} />
```

>[!NOTE]
>static import 방식은 빌드 타임에 파일을 분석해서 크기를 알 수 있어 자동 제공이 가능하다.

---

## 동적 import (Server Component)

>[!IMPORTANT]
>동적 이미지 import 파일명이 런타임에 결정되는 경우 Server Component에서 `dynamic import()`로 자동 메타데이터를 유지할 수 있다.

```tsx
async function PostImage({ imageFilename, alt }: { imageFilename: string; alt: string }) {
  const { default: image } = await import(`../content/blog/images/${imageFilename}`)
  // width, height, blurDataURL 자동 포함
  return <Image src={image} alt={alt} />
}
```

>[!WARNING]
>import 경로에는 반드시 정적 prefix가 있어야 한다 (`../content/blog/images/`).
>
>동적 경로만 사용하면 번들러가 대상 파일을 특정할 수 없다.

---

## 원격 이미지

>[!IMPORTANT]
>원격 이미지
>
>`remotePatterns` 외부 URL 이미지를 사용할 때는 `next.config.ts`에 허용 패턴을 반드시 등록해야 한다.
>
>원격 이미지는 빌드 타임에 크기를 알 수 없어서 `width`와 `height`를 직접 전달해야 한다. 또는 `fill` prop으로 부모 요소를 채우도록 설정할 수 있다.

```ts
// next.config.ts
const config: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 's3.amazonaws.com',
        pathname: '/my-bucket/**',
      },
    ],
  },
}
```

>[!WARNING]
>`remotePatterns`없이 외부 URL을 `src`로 넘기면 에러가 발생한다.
>
>가능한 한 구체적인 패턴을 작성해야 보안상 안전하다.

---

## CLS 방지와 width/height

>[!IMPORTANT]
>CLS (Cumulative Layout Shift)
>
>이미지 로딩 전에 레이아웃이 밀리는 현상으로, `next/image`는 `width` / `height`로 종횡비를 계산해 공간을 미리 확보한다.

>[!TIP]
>`width` / `height`는 실제 렌더 크기가 아니라 **종횡비 계산 기준**이다.
>
>CSS로 실제 크기를 조정해도 CLS방지는 유지 된다.

