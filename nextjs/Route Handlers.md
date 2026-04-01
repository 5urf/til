## Route Handlers

Route Handler는 Web Request와 Response API를 사용하여 주어진 라우트에 대한 커스텀 요청 핸들러를 생성할 수 있게 해준다.

>[!NOTE]
>Route Handler는 `app`디렉토리 내에서만 사용할 수 있다.

>[!IMPORTANT]
>Route Handler - Web Request/Response API를 사용해 특정 라우트에 대한 커스텀 요청 핸들러를 생성하는 기능

---

### 컨벤션

Route Handler는 `app`디렉토리 내의 `route.js|ts`파일에서 정의된다.

```ts
// app/api/route.ts
export async function GET(request: Request) {}
```

>Route Handler는 `page.js`나 `layout.js`와 마찬가지로 `app`디렉토리 내 어디에나 중첩될 수 있다.
>단, 같은 라우트 세그먼트 레벨에 `route.js`파일과 `page.js`파일이 함께 존재할 수 없다.

>[!IMPORTANT]
>`route.js|ts` - Route Handler를 정의하는 특수 파일이며, `app` 디렉토리 어디에나 중첩 가능하지만
>같은 세그먼트에 `page.js`와 공존할 수 없다.

---

### 지원되는 HTTP 메서드

>[!IMPORTANT]
>HTTP Methods `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS` 메서드를 지원하며, 미지원 메서드 호출 시 405 응답을 반환한다.

---

### 확장된 NextRequest와 NextResponse API

>[!IMPORTANT]
>NextRequest/NextResponse - 네이티브 Request/Response API를 확장한 Next.js 전용 API로,
>고급 사용 사례를 위한 편의 헬퍼를 제공한다.

---

### 캐싱

>Route Handler는 기본적으로 캐시되지 않는다. 그러나 `GET`메서드에 대해서는 캐싱을 선택적으로 활성화 할수 있다.
>다른 지원되는 HTTP 메서드는 캐시되지 않는다.
>`GET`메서드를 캐시하려면 Route Handler 파일에서 
>`export const dynamic = 'force-static'`과 같은 라우트 설정 옵션을 사용한다.

```ts
// app/items/route.ts
export const dynamic = 'force-static'
 
export async function GET() {
  const res = await fetch('https://data.mongodb-api.com/...', {
    headers: {
      'Content-Type': 'application/json',
      'API-Key': process.env.DATA_API_KEY,
    },
  })
  const data = await res.json()
 
  return Response.json({ data })
}
```

>[!NOTE]
>다른 지원되는 HTTP 메서드는 같은 파일에 캐시된 `GET` 메서드와 함께 배치되어 있더라도 캐시되지 않는다.

>[!IMPORTANT]
>Route Handler 캐싱 - Route Handler는 기본적으로 캐시되지 않으며,
>`GET`메서드에서만 `force-static` 옵션으로 캐싱을 활성화할 수 있다.

---

### Cache Components와 함께 사용하기

>[!IMPORTANT]
>use cache - Cache Components가 활성화되면 `GET` Route Handler는 일반 UI라우트와 동일한 모델을 따르며, `use cache` 지시어로 캐시되지 않는 데이터를 정적 응답에 포함시킬 수 있다.

#### Static 예제

캐시되지 않거나 런타임 데이터에 접근하지 않으므로 빌드 시점에 사전 렌더링된다.

```ts
// app/api/project-info/route.ts
export async function GET() {
  return Response.json({
    projectName: 'Next.js',
  })
}
```

#### Dynamic 예제

비결정적 연산에 접근한다. 빌드 중 `Math.random()`이 호출되면 사전 렌더링이 중단되고 요청 시점 렌더링으로 지연된다.

```ts
// app/api/random-number/route.ts
export async function GET() {
  return Response.json({
    randomNumber: Math.random(),
  })
}
```

#### 런타임 데이터 예제

요청별 데이터에 접근한다. `headers()`와 같은 런타임 API가 호출되면 사전 렌더링이 종료된다.

```ts
// app/api/user-agent/route.ts
import { headers } from 'next/headers'
 
export async function GET() {
  const headersList = await headers()
  const userAgent = headersList.get('user-agent')
 
  return Response.json({ userAgent })
}
```

>[!NOTE]
>`GET`핸들러가 네트워크 요청, 데이터베이스 쿼리, 비동기 파일 시스템 작업,
>요청 객체 속성(`req.url`, `request.headers`,`request.body`등), `cookies()`,`headers()`과 같은 런타임 API, 또는 비결정적 연산에 접근하면 사전 렌더링이 중단된다.

#### 캐시된 예제

캐시되지 않는 데이터(데이터베이스 쿼리)에 접근하지만 `use cache`로 캐시하여 사전 렌더링된 응답에 포함시킬 수 있다.

```ts
// app/api/products/route.ts
import { cacheLife } from 'next/cache'
 
export async function GET() {
  const products = await getProducts()
  return Response.json(products)
}
 
async function getProducts() {
  'use cache'
  cacheLife('hours')
 
  return await db.query('SELECT * FROM products')
}
```

>[!NOTE]
>`use cache`는 Route Handler 본문 내에서 직접 사용할 수 없다.
>헬퍼 함수로 추출해야한다. 캐시된 응답은 새 요청이 도착할 때 `cacheLife`에 따라 재검증된다.

---

### 특수 Route Handler

>`sitemap.ts`, `opengraph-image.tsx`, `icon.tsx`와 같은 특수 Route Handler 및
>기타 메타데이터 파일은 요청 시점 API나 동적 설정 옵션을 사용하지 않는 한 기본적으로 정적으로 유지된다.

---

### 라우트 해석

>[!IMPORTANT]
>Route Resolution (라우트 충돌) - `route.js`는 가장 낮은 수준의 라우팅 기본 요소이며,
>같은 라우트에 `page.js`와 함께 존재할 수 없다.

| page                 | Route              | 결과  |
| -------------------- | ------------------ | --- |
| `app/page.js`        | `app/route.js`     | 충돌  |
| `app/page.js`        | `app/api/route.js` | 유효  |
| `app/[user]/page.js` | `app/api/route.js` | 유효  |

각 `route.js` 또는 `page.js` 파일은 해당 라우트의 모든 HTTP 동사를 처리한다.

```ts
// app/page.ts
export default function Page() {
  return <h1>Hello, Next.js!</h1>
}
 
// 충돌
// `app/route.ts`
export async function POST(request: Request) {}
```

---

### 라우트 컨텍스트 헬퍼

>[!IMPORTANT]
>RouteContext - TypeScript에서 Route Handler의 `context` 매개변수 타입을 지정하는 전역 헬퍼이다.

```ts
// app/users/[id]/route.ts
import type { NextRequest } from 'next/server'
 
export async function GET(_req: NextRequest, ctx: RouteContext<'/users/[id]'>) {
  const { id } = await ctx.params
  return Response.json({ id })
}
```

>[!NOTE]
>타입은 `next dev`, `next build` 또는 `next typegen` 중에 생성된다.
