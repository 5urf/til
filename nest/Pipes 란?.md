## Pipe(파이프)란?

>[!NOTE]
>파이프는 `Injectable()` 데코레이터가 주석으로 달린 클래스로,
>
>**Data Transformation(데이터 변환)** 과 **Data Validation(유효성 검사)** 을 수행하기 위해 사용한다.
>
>컨트롤러의 라우트 핸들러 메소드가 실행되기 직전에 끼어들어, 해당 메소드로 전달되는 인수를 가로채어 검사하거나 변환한다.

## 파이프의 주요 두 가지 역할

- **Data Transformation (데이터 변환)**
	- 입력 데이터를 컨트롤러 핸들러가 기대하는 형식으로 변환한다.
	- 클라이언트로부터 전달되는 데이터(예: 쿼리 스트링, URL 파라미터)는 기본적으로 문자열 형태인 경우가 많다.
		- 파이프를 이용하면 이를 정수형이나 특정 인스턴스로 자동 변환할 수 있다.
		- 예시: 문자열 `'7'` -> 숫자(정수) `7`
- **Data Validation (유효성 검증)**
	- 들어온 입력 데이터를 평가하여 규격에 맞는지 확인한다.
	- 데이터가 유효하면 원래 형태를 유지하거나 정제된 상태로 컨트롤러 핸들러에 전달한다.
	- 데이터가 올바르지 않으면 예외(BadRequestException 등)를 발생시켜 컨트롤러 로직이 실행되지 않도록 차단한다.
	- 예시: 필드 길이가 10자 이하여야 하는데 10자를 초과한 경우 즉시 에러 응답 반환

## 파이프의 실행 흐름

```text
[Client (HTTP Request)]
       │  (1. HTTP 요청 전달: 예: /board/123 또는 Body)
       ▼
┌──────────────────────────────────────────────┐
│  Pipe (Transformation & Validation)          │
│  - 라우트 핸들러 호출 '직전'에 인수(Arguments) 수신  │
│  - 유효성 검사 실패 시 -> 즉시 400 Bad Request 예외  │
│  - 검증 통과 및 타입 변환 수행 (예: string -> number) │
└──────────────────────┬───────────────────────┘
                       │ (2. 변환 및 검증 완료된 파라미터 전달)
                       ▼
┌──────────────────────────────────────────────┐
│  Controller (Route Handler)                  │
│  - createBoard(@Body() ...) / getBoard(@Param() ...) │
│  - 안전하고 정제된 데이터만을 받아 로직 실행         │
└──────────────────────┬───────────────────────┘
                       │ (3. 비즈니스 로직 호출)
                       ▼
┌──────────────────────────────────────────────┐
│  Service 계층                                │
└──────────────────────────────────────────────┘
```

1. **Client -> Pipe** : 클라이언트가 요청을 보내면, 라우트 핸들러 메소드가 실행되기 직전에 파이프가 파라미터 인수를 먼저 수신한다.
2. **Pipe -> Controller** : 파이프 내부에서 유효성 검증과 필요한 타입 변환을 처리한다. 데이터에 문제가 없으면 변환된 인수를 컨트롤러 메소드의 인자로 안전하게 넘겨준다.
3. **Controller -> Service** : 컨트롤러는 타입 안전성이 보장된 데이터를 가지고 비즈니스 로직(서비스 계층)을 실행한다.


## 파이프 바인딩 방법 (Binding Pipes)

파이프를 사용하는 방법은 스코프(적용 범위)에 따라 세 가지로 나뉜다.

### Handler-level Pipes (핸들러 레벨)
* 핸들러 레벨에서 `@UsePipes()` 데코레이터를 이용해서 사용할 수 있다.
* 이 파이프는 해당 메소드로 들어오는 모든 파라미터에 적용된다.

```ts
@Post()
@UsePipes(ValidationPipe)
createBoard(
  @Body('title') title: string,
  @Body('description') description: string,
) {}
```

### Parameter-level Pipes (파라미터 레벨)
* 파라미터 레벨의 파이프이기에 특정한 파라미터에만 적용되는 파이프다.
* 아래 코드의 경우 `title` 파라미터에만 파이프가 적용된다.

```ts
@Post()
createBoard(
  @Body('title', ParameterPipe) title: string,
  @Body('description') description: string,
) {}
```

### Global-level Pipes (글로벌 레벨)
* 애플리케이션 레벨의 글로벌 파이프로서, 클라이언트에서 들어오는 모든 요청에 적용된다.
* 가장 상단 영역인 `main.ts`에 설정해 주면 된다.

```ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(new ValidationPipe());
  await app.listen(3000);
}
bootstrap();
```

## 기본 제공 내장 파이프 (Built-in Pipes)

Nest.js에서 기본적으로 사용할 수 있게 만들어 놓은 내장 파이프다.

* `ValidationPipe` : DTO와 함께 사용하여 유효성을 검증하는 파이프
* `ParseIntPipe` : 문자열을 정수(number) 타입으로 변환하는 파이프
* `ParseBoolPipe` : 문자열(`'true'`, `'false'`)을 불리언 타입으로 변환하는 파이프
* `ParseArrayPipe` : 문자열 등을 배열 타입으로 변환하는 파이프
* `ParseUUIDPipe` : 파라미터가 유효한 UUID 형식인지 검증하는 파이프
* `DefaultValuePipe` : 값이 전달되지 않았을 때 기본값을 주입하는 파이프

### ParseIntPipe 활용 예시

URL 파라미터나 쿼리 스트링은 HTTP 특성상 기본적으로 문자열 형태로 들어온다.

`ParseIntPipe`를 사용하면 컨트롤러 실행 직전에 정수 형태로 자동 변환해 준다.

```ts
@Get(':id')
getBoardById(@Param('id', ParseIntPipe) id: number) {
  // 클라이언트 요청: GET /board/7
  // id에는 문자열 '7'이 아닌 숫자 7이 전달된다.
  return this.boardService.getBoardById(id);
}
```

> [!WARNING]
> 숫자로 변환할 수 없는 값(예: `GET /board/abc`)이 들어오면 핸들러가 실행되기 전에 즉시 요청을 차단하고 `400 Bad Request` 에러를 반환한다.
