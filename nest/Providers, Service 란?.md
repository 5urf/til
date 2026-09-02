## Providers

>프로바이더는 Nest의 핵심 개념
>
>대부분의 기본 Nest 클래스는(서비스, 리포지토리, 팩토리, 핼퍼) 프로바이더로 취급될 수 있다
>
>프로바이더의 핵심 아이디어는 의존성으로 **주입**될 수 있다는 것
>
>즉, 객체는 서로 다양한 관계를 만들 수 있으며, 객체의 인스턴스를 '연결'하는 기능은 대부분 Nest 런타임 시스템에 위임될 수 있다.

![Providers](https://docs.nestjs.com/assets/Components_1.png)

## Service 란?

>서비스는 소프트웨어 개발내의 공통 개념이며, Nest.js, JavaScript에서만 쓰이는 개념이 아니다.
>
>`@Injectable()` 데코레이터로 감싸져서 모듈에 제공되며, 이 서비스 인스턴스는 애플리케이션 전체에서 사용 될 수 있다.
>
>서비스는 컨트롤러에서 데이터의 유효성을 체크하거나 데이터베이스에 아이템을 생성하는 등의 작업을 하는 부분을 처리한다.

>[!NOTE]
>컨트롤러는 클라이언트의 요청 처리만을 담당하고, 데이터의 유효성을 체크하거나 데이터베이스에 아이템을 생성하는 등의 실제 핵심 로직은 서비스가 전담하도록 설계된다.
>
>이를 통해 책임을 명확히 분리하고 SOLID 원칙을 준수하는 객체 지향적 구조를 구현할 수 있다.

>[!NOTE]
>객체 지향적 구조란?
>
>프로그램의 데이터와 이를 처리하는 로직을 하나의 독립된 '객체'로 묶어 조립하듯 설계하는 방식
>
>컨트롤러(요청 처리)와 서비스(핵심 로직)처럼 각 객체가 명확히 하나의 역할만 맡도록 책임을 분리하면(단일 책임 원칙),
>
>특정 기능에 문제가 생기거나 확장이 필요할 때 해당 객체만 수정하면 되므로 유지보수와 코드 재사용성이 크게 향상된다.

## Service를 Controller에서 사용하는 법 (Dependency Injection(의존성 주입))

```ts
import { BoardsService } from './boards.service';

@Controller('boards')
export class BoardsController {
  constructor(private boardsService: BoardsService) {}
  
  @Get('/:id')
  getBoardById(@Param('id') id: string): Board {
    return this.boardsService.getBoardById(id);
  }
}
```

- 생성자를 통한 주입(Constructor Injection): 서비스는 컨트롤러의 생성자(constructor)를 통해 주입된다.
- TypeScript 단축 문법(`private`): 생성자 매개변수 앞에 `private`키워드를 붙이면, 클래스 내부에 멤버 변수를 선언함과 동시에 초기화까지 한번에 처리해주는 타입스크립트의 단축 문법이다.
	- 즉 `this.boardsService = boardsService;`구문을 생략할 수 있다.
- 타입 기반 의존성 해결: Nest.js는 의존성 주입(DI)라는 강력한 디자인 패턴을 기반으로 구축되었다. 타입스크립트의 기능을 활용하여, 코드에 명시된 타입(BoardsServie)만 보고도 어떤 의존성이 필요한지 자동으로 파악하고 해결한다.
- 자동 인스턴스화: 개발자가 직접 `new BoardsService()`를 호출할 필요가 없다. Nest.js가 알아서 서비스의 인스턴스를 생성하여 반환해 주며, 이미 다른곳에서 요청되어 생성된 적이 있다면 기존의 싱글톤(Singleton) 인스턴스를 재사용하여 컨트롤러에 주입한다.
