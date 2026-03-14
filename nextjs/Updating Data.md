Server Function은 서버에서 실행되는 비동기 함수

form/mutation 맥락에서 쓰이면 Server Action이라 부름

내부적으로 `POST`메서드만 사용한다

## 선언

파일 상단에 `'use server'` -> 전체 export가 서버함수

```ts
`use server`
export async function createPost(formData: FormData) {
  const title = formData.get('title);
  // DB 업데이트
  revalidatePath('posts');
}
```

Server component 안에 인라인 선언도 가능

```ts
export default function Page() {
  async function createPost(formData: FormData) {
    'use server'
    // ...
  }
  return <form action={createPost}>...</form>
}
```

## 호출 - Form

form의 action prop에 서버 함수를 직접 전달

```ts
import { createPost } from '@/app/actions'

export function Form() {
  return (
    <form action={createPost}>
      <input type="text" name="title" />
      <input type="text" name="content" />
      <button type="submit">생성</button>
    </form>
  )
}
```

## 호출 - Event Handler

onClick 같은 이벤트 핸들러에서도 호출 가능

```ts
'use client'

import { incrementLike } from './actions'
import { useState } from 'react'

export default function LikeButton({ initialLikes }: { initialLikes: number }) {
  const [likes, setLikes] = useState(initialLikes)

  return (
    <button
      onClick={async () => {
        const updatedLikes = await incrementLike()
        setLikes(updatedLikes)
      }}
    >
      좋아요 {likes}
    </button>
  )
}
```

## revalidation 흐름

데이터 변경 후 캐시 무효화 -> 최신 데이터 반영

```ts
'use server'

import { revalidatePath, revalidateTag } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  // DB 업데이트
  revalidatePath('/posts')   // 경로 기반 캐시 무효화
  revalidateTag('posts')     // 태그 기반 캐시 무효화
  redirect('/posts')         // 반드시 revalidate 후에 호출
}
```

>[!warning]
>`redirect()`는 호출 즉시 throw됨 - 이후 코드 실행 안 됨
>`revalidatePath` / `revaildateTag`를 반드시 먼저 호출 할 것


## pending 상태

`useActionState`의 세번째 반환값 `pending`으로 로딩 UI처리

```ts
'use client'

import { useActionState } from 'react'
import { createPost } from '@/app/actions'

export function Button() {
  const [state, action, pending] = useActionState(createPost, false)

  return (
    <button onClick={() => action()}>
      {pending ? '저장 중...' : '게시물 작성'}
    </button>
  )
}
```

>[!tip]
>`useActionState`는 pending 상태뿐 아니라 action 결과(state)도 반환함
