## tsconfig.json이란

>[!IMPORTANT]
>`tsconfig.json`
>디렉토리에 `tsconfig.json`이 존재하면 해당 디렉토리가 TypeScript 프로젝트의 루트임을 나타낸다.
>컴파일에 포함할 루트 파일과 컴파일러 옵션을 지정하는 설정 파일이다.

- `tsc`를 입력파일 없이 실행하면, 현재 디렉토리부터 상위로 올라가며 `tsconfig.json`을 탐색
- CLI에 입력 파일을 직접 지정하면 `tsconfig.json`은 무시됨

```json
{
  "compilerOptions": {
    "module": "nodenext",
    "target": "esnext",
    "strict": true
  },
  "include": ["src/**/*"],
  "exclude": ["**/*.spec.ts"]
}
```

---

## 루트 필드

>[!IMPORTANT]
>files / include / exclude / extends
>컴파일 대상 파일을 결정하는 필드들이다.

- `files`: 포함할 파일을 명시적으로 나열. 파일 수가 적을 때 사용
- `include`: glob 패턴으로 포함할 파일 지정 (`*`,`?`,`**`지원)
- `exclude`: `include`에서 제외할 패턴 지정. 단, `import`로 참조되는 파일까지 제외하진 않음
- `extends`: 다른 tsconfig 파일을 상속. base 설정을 먼저 로드한 뒤 현재 파일이 덮어씀

```json
{
  "extends": "@tsconfig/node18/tsconfig.json",
  "compilerOptions": {
    "strict": true
  },
  "include": ["src/**/*"]
}
```

---

## strict 옵션

>[!IMPORTANT]
>strict
>`strict: true`는 엄격한 타입 체크 옵션들을 한꺼번에 활성화 하는 플래그다.
>개별 옵션을 따로 끌 수 있으므로, 먼저 `strict: true`로 설정한 뒤 필요한 것만 `false`로 조정하는 방식이 권장된다.

`strict`가 활성화하는 주요 옵션:

- `noImplicitAny`: 타입 추론이 `any`로 떨어지면 에러
- `strictNullChecks`: `null`/`undefined`를 별도 타입으로 엄격히 구분
- `strictFunctionTypes`: 함수 파라미터 타입을 더 정확하게 체크
- `strictBindCallApply`: `call`,`bind`,`apply`의 인수 타입 체크
- `strictPropertyInitialization`: 클래스 프로퍼티 초기화 강제
- `noImplicitThis`: `this`가 `any`로 추론되면 에러
- `alwaysStrict`: 모든 파일에 `"use strict"`적용
- `useUnknownInCatchVariables`: `catch`변수 타입을 `unknown`으로

---

## module 옵션

>[!IMPORTANT]
>module
>출력 코드가 사용할 모듈 시스템을 지정한다.
>프로젝트 환경에 따라 적절한 값이 달라진다.

- `"nodenext"`: 모던 Node.js 프로젝트에 권장. `package.json`의 `type`필드에 따라 ESM/CJS 자동 결정
- `"esnext"`/ `"preserve"`: 번들러를 사용하는 프로젝트에 적합
- `"commonjs"`: CommonJS 출력이 필요한 레거시 환경
- `module`값은 `moduleResolution`설정에도 영향을 줌

---

## target 옵션

>[!IMPORTANT]
>target
>TypeScript가 출력할 JavaScript의 ECMAScript 버전을 지정한다.
>최신 문법을 해당 버전에 맞게 다운그레이드한다.

- `"esnext"`: 최신 ECMAScript 기능을 그대로 출력 (번들러 사용시 권장)
- `"es2015"`~`"es2022"`: 해당 버전까지의 문법만 출력
- `target`은 `lib`의 기본값에도 영향 - 예 `target: "es2015"`이면 `lib`에 ES2015 API가 포함됨
- TS 6.0부터 `target: "es5"`는 deprecated - 최소 `"es2015"` 사용
