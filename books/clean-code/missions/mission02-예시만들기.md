# MISSION 02

## MISSION: 예시 만들기

본인이 잘 이해했는지 확인하는 가장 정확한 방법은 가르쳐 보는 것!

클린코드 읽으며 뼈맞았던 내용 중 **`3가지 원칙`** 을 고르고, 원칙 따르는 예시 총 3가지를 만들어보세요.

클린코드 읽을 때 분명 참고하라고 적어준 예시인데 자바로 되어있어서 공감이 잘 안됐죠?

이제 본인이 가장 잘하는 언어로(JS, Python 등등) 더러운 코드를 깨끗한 코드로 리팩토링하는 예시를 만들어보세요.

## 원칙 1. 단일 책임 원칙 (SRP)

**Before 😣**

```tsx
const UserCard = ({ userId }: { userId: string }) => {
  const [user, setUser] = useState<User | null>(null);
  const [likeCount, setLikeCount] = useState(0);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await fetch(`/api/users/${userId}`);
        const userData = await response.json();
        setUser(userData);
      } catch (error) {
        console.error("Failed to fetch user:", error);
      }
    };
    fetchUser();
  }, [userId]);

  const handleLike = () => {
    setLikeCount((prev) => prev + 1);
  };

  return (
    <div>
      <button onClick={handleLike}>👍 {likeCount}</button>
      {user && (
        <div>
          <h2>{user.name}</h2>
          <p>{user.email}</p>
        </div>
      )}
    </div>
  );
};
```

**무엇을 고치려고 하는지:** 사용자 정보 표시와 좋아요 기능을 한 컴포넌트가 담당하고 있습니다.

**After 😎**

```tsx
const UserCard = ({ userId }: { userId: string }) => {
  const [user, setUser] = useState<User | null>(null);

  const fetchUser = async () => {
    try {
      const response = await fetch(`/api/users/${userId}`);
      const userData = await response.json();
      setUser(userData);
    } catch (error) {
      console.error("Failed to fetch user:", error);
    }
  };

  useEffect(() => {
    fetchUser();
  }, [userId]);

  if (!user) return <p>사용자를 찾을 수 없습니다.</p>;

  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
};

const LikeButton = () => {
  const [likeCount, setLikeCount] = useState(0);

  const handleLike = () => {
    setLikeCount((prev) => prev + 1);
  };

  return <button onClick={handleLike}>👍 {likeCount}</button>;
};
```

**어떻게 고쳤는지:** 각 컴포넌트가 하나의 책임만 갖도록 분리했습니다. UserCard는 사용자 정보 표시만, LikeButton은 좋아요 기능만 담당합니다.

## 원칙 2. 함수는 한 가지를 해야 한다

**Before 😣**

```js
const handleSubmit = (formData) => {
  if (!formData.email) return alert("이메일을 입력하세요");

  const email = formData.email.toLowerCase().trim();
  const user = { email, createdAt: new Date() };

  localStorage.setItem("user", JSON.stringify(user));
  alert("저장 완료!");
};
```

**무엇을 고치려고 하는지:** 한 함수가 검증, 데이터 변환, 저장, 알림까지 4가지 일을 하고 있습니다.

**After 😎**

```js
const handleSubmit = (formData) => {
  validateEmail(formData.email);
  const user = createUser(formData.email);
  saveUser(user);
  showSuccess();
};

const validateEmail = (email) => {
  if (!email) throw new Error("이메일을 입력하세요");
};

const createUser = (email) => ({
  email: email.toLowerCase().trim(),
  createdAt: new Date(),
});

const saveUser = (user) => {
  localStorage.setItem("user", JSON.stringify(user));
};

const showSuccess = () => alert("저장 완료!");
```

**어떻게 고쳤는지:** 각 함수가 하나의 일만 하도록 분리했습니다. 함수명만 봐도 무엇을 하는지 명확해집니다.

## 원칙 3. Try-Catch-Finally 문부터 작성하라

**Before 😣**

```js
const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("/api/upload", {
    method: "POST",
    body: formData,
  });

  const result = await response.json();
  return result;
};
```

**무엇을 고치려고 하는지:** 업로드 실패 시 에러 처리가 없어서 사용자가 무엇이 잘못됐는지 알 수 없습니다.

**After 😎**

```js
const uploadFile = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/api/upload", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("업로드 실패");

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("업로드 실패:", error);
    throw new Error("파일 업로드에 실패했습니다");
  } finally {
    resetForm();
  }
};
```

**어떻게 고쳤는지:** try-catch-finally 구조로 에러 상황을 먼저 고려해서 설계했습니다. 성공/실패와 관계없이 항상 실행되어야 하는 폼 정리 작업은 finally에 배치했습니다.
