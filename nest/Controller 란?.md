>컨트롤러는 들어오는 요청을 처리하고 클라이언트에 응답을 반환하는 역할을 담당

![Controller](https://docs.nestjs.com/assets/Controllers_1.png)

- 컨트롤러는 `@Controller()` 데코레이터로 클래스를 데코레이션하여 정의됨
```ts
@Controller('/boards')
export class BoardsController {
  
}
```

- 데코레이터는 인자를 컨트롤러에 의해서 처리되는 '경로'를 받음

### Hnadler 란?

>핸들러는 `@GET`, `@Post`, `@Patch`,`@Delete`등과 같은 데코레이터로 장식된 컨트롤러 클래스 내의 단순한 메서드

```ts
@Controller('/boards')
export class BoardsController {
  @Get()
  getBoards(): string {
    return 'This action return all boards'
  }
}
```
