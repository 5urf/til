## `.env`파일 로딩

>`.env`파일에 선언된 변수는 Next.js가 자동으로 `process.env`에 주입한다.
>
>별도 설정 없이 Route Handlers나 서버 컴포넌트에서 바로 사용 가능하다.

```txt
# .env
DB_HOST=localhost
DB_USER=myuser
DB_PASS=mypassword
```
```ts
// app/api/route.ts
export async function GET() {
  const db = await myDB.connect({
    host: process.env.DB_HOST,
    username: process.env.DB_USER,
    password: process.env.DB_PASS,
  })
}
```

>[!IMPORTANT]
>`.env`변수는 기본적으로 **서버 전용**이다.
>
>브라우저에서는 접근 불가

>[!WARNING]
>`/src`폴더 구조를 사용한다면 `.env`파일은 `/src`안이 아니라 **프로젝트 루트**에 있어야 한다.

>[!TIP]
>DB 비밀번호, API 시크릿 등 민감 정보는 `.env.local`에 넣고 `.gitignore`에 포함시킬 것.
>
>`create-next-app`템플릿은 기본으로 처리해준다.

---

## `NEXT_PUBLIC_`접두사

>[!IMPORTANT]
>`NEXT_PUBLIC_`접두사를 붙이면 Next.js가 **빌드 타임**에 해당 값을 JS 번들에 인라인(hard-code)한다.
>
>클라이언트(브라우저)에서도 접근 가능해진다.

```txt
# .env
NEXT_PUBLIC_ANALYTICS_ID=abcdefghijk
```
```ts
// 빌드 후 아래 코드는 setupAnalyticsService('abcdefghijk') 로 변환됨
setupAnalyticsService(process.env.NEXT_PUBLIC_ANALYTICS_ID)
```

>[!IMPORTANT]
>빌드 타임에 값이 고정(frozen)되므로, 배포 후 환경 변수를 바꿔도 반영되지 않는다.
>
>값을 바꾸려면 **재빌드** 필요.

>[!WARNING]
>**동적 lookup은 인라인되지 않는다.**
>
>아래 두 패턴은 브라우저에서 `undefined`된다.

```ts
// ❌ 인라인 안 됨
const key = 'NEXT_PUBLIC_ANALYTICS_ID'
process.env[key]

// ❌ 인라인 안 됨
const env = process.env
env.NEXT_PUBLIC_ANALYTICS_ID
```

---

## 서버 / 클라이언트 변수 차이

| 구분                | 접근 가능 환경   | 값 결정 시점     |
| ----------------- | ---------- | ----------- |
| 일반 변수 (`DB_HOST`) | 서버 전용      | 런타임         |
| `NEXT_PUBLIC_`변수  | 서버 + 클라이언트 | 빌드 타임 (인라인) |

- 서버에서는 dynamic rendering 중에도 런타임 환경 변수를 안전하게 읽을 수 있다.

```tsx
// app/page.ts — dynamic rendering에서 런타임 값 읽기
import { connection } from 'next/server'

export default async function Component() {
  await connection() // dynamic rendering으로 opt-in
  const value = process.env.MY_VALUE // 런타임에 평가됨
}
```

>[!NOTE]
>`NEXT_PUBLIC_`없는 서버 변수는 Docker 이미지 하나를 여러 환경에 배포할 때 환경별로 다른 값을 주입할 수 있다.
>
>`NEXT_PUBLIC_`변수는 빌드 때 고정되므로 멀티 환경 배포에 적합하지 않다.

---

## 환경 변수 로드 우선순위

- 같은 변수가 여러파일에 있을 때 아래 순서로 먼저 발견된 값이 사용된다.

```txt
1. process.env
2. .env.[NODE_ENV].local   (예: .env.development.local)
3. .env.local              (test 환경에서는 로드 안 됨)
4. .env.[NODE_ENV]         (예: .env.development)
5. .env
```

>[!WARNING]
>`.env.local`은 `test`환경(`NODE_ENV=test`)에서 **로드되지 않는다.**
>
>테스트 결과의 일관성을 보장하기 위한 의도적인 설계다.

>[!TIP]
>Jest / Cypress 같은 테스트 도구와 함께 쓸 때 Next.js와 동일한 방식으로 env를 로드하려면
>
>`@next/env`패키지의 `loadEnvConfig`를 사용한다.
