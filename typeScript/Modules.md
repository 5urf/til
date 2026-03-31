## JavaScript 모듈이 정의되는 방식

- TypeScript에서 최상위 레벨 `import` 또는 `export`를 포함하는 모든 파일은 모듈로 간주된다.
- 반대로, 최상위 레벨 `import`나 `export` 선언이 없는 파일은 그 내용이 전역 스코프에서 사용 가능한 스크립트로 취급된다. (따라서 모듈에서도 접근 가능)

>[!IMPORTANT]
>module vs script
>`TypeScript`가 파일을 모듈로 인식하는 기준은
>top-level(최상위 레벨) `import` 또는 `export` 유무 이다

---

## 비모듈 (Non-modules)

JavaScript 명세는 `import` 선언, `export`, 또는 top-level `await`이 없는 JavaScript 파일은 스크립트로 간주되어야 하며 모듈이 아니라고 선언한다.

>[!IMPORTANT]
>`import`/`export`가 없는 파일을 강제로 모듈로 만드는 빈 `export`선언
>현재 `import`나 `export`가 없지만 모듈로 취급되길 원하는 파일이 있다면, 다음 줄을 추가한다:
>`export {};`

이렇게 하면 파일이 아무것도 내보내지 않는 모듈로 변경된다. 이 구문은 모듈 target과 관계없이 작동한다.

---

## TypeScript에서의 모듈

TypeScript에서 모듈 기반 코드를 작성할 때 고려해야 할 세가지 주요사항

- Syntax: import와 export에 어떤 구문을 사용할 것인가?
- Module Resolution: 모듈 이름과 디스크의 파일 간의 관계는 무엇인가?
- Module Output Target: 내보내진 JavaScript 모듈은 어떤 모습이어야 하는가?

---

### ES Module 구문

파일은 `export default`를 통해 주요 export를 선언할 수 있다.

```ts
// @filename: hello.ts
export default function helloWorld() {
  console.log("Hello, world!");
}

// 다음과 같이 import 된다.
import helloWorld from "./hello.js";
helloWorld();
```

default export 외에도, `default`를 생략한 `export`를 통해 여러 변수와 함수를 내보낼 수 있다.

```ts
// @filename: maths.ts
export var pi = 3.14;
export let squareTwo = 1.41;
export const phi = 1.61;

export class RandomNumberGenerator {}

export function absolute(num: number) {
  if (num < 0) return num * -1;
  return num;
}

// `import` 구문을 통해 다른 파일에서 사용할 수 있다:
import { pi, phi, absolute } from "./maths.js";

console.log(pi);
const absPhi = absolute(phi);
// const absPhi: number
```

>[!IMPORTANT]
>**export default** - 모듈의 주요 내보내기를 단일 값으로 선언
>**named export** - `default` 없이 여러 값을 개별적으로 내보내기

---

### 추가 Import 구문

import는 `import {old as new}`형식을 사용하여 이름을 변경할 수 있다.

```ts
// @filename: maths.ts
export const pi = 3.14;
export default class RandomNumberGenerator {}

// @filename: app.ts
import RandomNumberGenerator, { pi as π } from "./maths.js";

RandomNumberGenerator;
// (alias) class RandomNumberGenerator
// import RandomNumberGenerator

console.log(π);
// (alias) const π: 3.14
// import π
```

`* as name`을 사용하여 내보낸 모든 객체를 단일 네임스페이스에 넣을 수 있다

```ts
// @filename: app.ts
import * as math from "./maths.js";

console.log(math.pi);
const positivePhi = math.absolute(math.phi);
// const positivePhi: number
```

`import "./file"`을 통해 현재 모듈에 변수를 포함하지 않고 파일을 import할 수 있다

```ts
// @filename: app.ts
import "./maths.js";

console.log("3.14");
```

>이 경우 `import`는 아무것도 하지 않는다.
>그러나 `maths.ts`의 모든 코드가 평가되었으며,
>이는 다른 객체에 영향을 미치는 부수 효과(side-effects)를 트리거할 수 있다.


>[!IMPORTANT]
>**namespace import** `* as name` 구문을 사용하여 모든 export를 단일 네임스페이스 객체로 가져오는 방식
>**side-effect import** 변수를 가져오지 않고 모듈의 코드만 실행하는 import 방식

---

### TypeScript 전용 ES Module 구문

TypeScript는 타입의 import를 선언하기 위해 두 가지 개념으로 `import` 구문을 확장했다

```ts
// @filename: animal.ts
export type Cat = { breed: string; yearOfBirth: number };
export type Dog = { breeds: string[]; yearOfBirth: number };
export const createCatName = () => "fluffy";

// @filename: valid.ts
import type { Cat, Dog } from "./animal.js";
export type Animals = Cat | Dog;

// @filename: app.ts
import type { createCatName } from "./animal.js";
const name = createCatName();
// 'createCatName' cannot be used as a value because it was imported using 'import type'.
```

>[!IMPORTANT]
>**import type** 타입만 import하여 JavaScript 출력에서 완전히 제거되는 TypeScript 전용 import

TypeScript 4.5에서는 개별 import 앞에 `type`을 붙여 해당 참조가 타입임을 나타낼 수 있다

```ts
// @filename: app.ts
import { createCatName, type Cat, type Dog } from "./animal.js";

export type Animals = Cat | Dog;
const name = createCatName();
```

이를 통해 Babel, swc, esbuild와 같은 비-TypeScript 트랜스파일러가 어떤 import를 안전하게 제거할 수 있는지 알 수 있다.

>[!IMPORTANT]
>**inline type import** 개별 import 앞에 `type` 키워드를 붙여 해당 import가 타입임을 표시하는 방식

---

## CommonJS 구문

- CommonJS는 npm의 대부분의 모듈이 제공되는 포맷
- CommonJS 구문이 어떻게 작동하는지 간략히 이해하면 더 쉽게 디버그할 수 있다

### 내보내기 (Exporting)

1. 식별자는 `module`이라는 전역의 `exports` 속성을 설정하여 내보낸다.
2. 그런 다음 이 파일들은 `require` 문을 통해 import할 수 있다.
3. 또는 JavaScript의 구조 분해 기능을 사용하여 약간 단순화할 수 있다.

```ts
// 1
function absolute(num: number) {
  if (num < 0) return num * -1;
  return num;
}

module.exports = {
  pi: 3.14,
  squareTwo: 1.41,
  phi: 1.61,
  absolute,
};

// 2
const maths = require("./maths");
maths.pi;
// any

// 3
const { squareTwo } = require("./maths");
squareTwo;
// const squareTwo: any
```

>[!IMPORTANT]
>**CommonJS** -  `module.exports`와 `require()`를 사용하는 Node.js 전통 모듈 시스템

### CommonJS와 ES 모듈의 상호 운용성

- default import와 module namespace object import 간의 구분에 관해 CommonJS와 ES Modules 사이에 기능 불일치가 있다.
- TypeScript에는 두 가지 다른 제약 조건 세트 간의 마찰을 줄이기 위한 컴파일러 플래그 [`esModuleInterop`](https://www.typescriptlang.org/tsconfig#esModuleInterop)를 제공한다.

>[!IMPORTANT]
>**esModuleInterop** -  CommonJS와 ES Modules 간의 default import 불일치를 해결하는 컴파일러 플래그

---

## TypeScript의 모듈 해석 옵션

모듈 해석(Module resolution)은 `import` 또는 `require` 문의 문자열을 가져와서 해당 문자열이 어떤 파일을 가리키는지 결정하는 과정

- TypeScript에는 두 가지 해석 전략이 포함되어 있다
- Classic과 Node. 컴파일러 옵션 `module`이 `commonjs`가 아닐 때 기본값인 Classic은 이전 버전과의 호환성을 위해 포함되어 있다.
- Node 전략은 Node.js가 CommonJS 모드에서 작동하는 방식을 복제하며, `.ts` 및 `.d.ts`에 대한 추가 검사를 포함한다.
- TypeScript 내에서 모듈 전략에 영향을 미치는 많은 TSConfig 플래그가 있다, `moduleResolution`, `baseUrl`, `paths`, `rootDirs`

>[!IMPORTANT]
>**Module Resolution** - import/require 문의 문자열이 디스크의 어떤 파일을 가리키는지 결정하는 과정

---

## TypeScript의 모듈 출력 옵션

내보내진 JavaScript 출력에 영향을 미치는 두가지 옵션이 있다

- `target`: 어떤 JS 기능이 다운그레이드되고 어떤 기능은 그대로 유지되는지를 결정한다
- `module`: 모듈이 서로 상호 작용하는 데 어떤 코드가 사용되는지 결정

>어떤 `target`을 사용할지는 TS코드를 실행할 것으로 예상되는 JS 런타임에서 사용 가능한 기능에 따라 결정된다.
>모듈 간의 모든 통신은 모듈 로더를 통해 이뤄지며, 컴파일러 옵션 `module`은 어떤 것이 사용되는지 결정한다.
>런타임에 모듈 로더는 모듈을 실행하기 전에 모듈의 모든 종속성을 찾아 실행하는 역할을 한다.

>[!IMPORTANT]
>**module output option** - TypeScript가 JavaScript로 변환할 때 어떤 모듈 형식으로 출력할지 결정하는 설정

---

## TypeScript 네임스페이스

>TypeScript는 ES Modules 표준보다 앞서는 `namespaces`라는 자체 모듈 포맷을 가지고 있다.
>이 구문은 복잡한 정의 파일을 만드는 데 많은 유용한 기능이 있으며, `DefinitelyTyped`에서 여전히 활발하게 사용되고 있다. deprecated되지는 않았지만, namespaces의 대부분의 기능은 ES Modules에 존재하며 JavaScript의 방향에 맞추기 위해 ES Modules를 사용하는 것을 권장

>[!IMPORTANT]
>**namespaces** - ES Modules 이전에 TypeScript가 제공한 자체 모듈 포맷 - 현재는 ES Modules 사용 권장
