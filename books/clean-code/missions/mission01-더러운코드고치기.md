# MISSION 01

## MISSION: 더러운 코드를 고쳐라!

아래 가이드를 보고 총 3개의 더러운 코드를 깨끗하게 고쳐 보세요.

### Quiz 1

- Hint❕ : 검색하기 쉬운 이름을 사용하세요.
- blastOFF는 로켓 발사를 의미. 86400000은 하루의 밀리초 (milliseconds) 의미.

```js
// What the heck is 86400000 for?
setTimeout(blastOff, 86400000);
```

**위 코드를 깨끗하게 다시 작성해 주세요.**

```js
const MILLISECONDS_IN_A_DAY = 86400000;
setTimeout(blastOff, MILLISECONDS_IN_A_DAY);
```

**어떻게 고쳤는지, 사례에서 무엇을 배워야 하는지 설명해주세요.**

- 매직 넘버 `86400000`을 의미 있는 상수명 `MILLISECONDS_IN_A_DAY`로 바꿔 코드의 의도를 명확하게 했습니다.
- 2장의 "검색하기 쉬운 이름을 사용하라" 원칙과 "의도를 분명히 밝혀라" 원칙을 적용했습니다.
- 숫자만으로는 알 수 없는 값을 명확한 이름으로 표현하는 것이 중요합니다.

### Quiz 2

- Hint❕ : 의미있는 이름을 사용해 주세요.

```js
const yyyymmdstr = moment().format("YYYY/MM/DD");
```

**위 코드를 깨끗하게 다시 작성해 주세요.**

```js
const currentDate = moment().format("YYYY/MM/DD");
```

**어떻게 고쳤는지, 사례에서 무엇을 배워야 하는지 설명해주세요.**

- 축약된 변수명 `yyyymmdstr`을 의미 있는 이름 `currentDate`로 바꿔 코드의 목적을 명확하게 했습니다.
- 2장의 "의도를 분명히 밝혀라" 원칙을 적용했습니다.
- 변수명만 봐도 무엇을 담고 있는지 바로 알 수 있어야 합니다.

### Quiz 3

- Hint❕ : 불필요하게 반복하지 마세요.

```js
const Car = {
  carMake: "Honda",
  carModel: "Accord",
  carColor: "Blue",
};

function paintCar(car, color) {
  car.carColor = color;
}
```

**위 코드를 깨끗하게 다시 작성해 주세요.**

```js
const Car = {
  make: "Honda",
  model: "Accord",
  color: "Blue",
};

function paintCar(car, color) {
  car.color = color;
}
```

**어떻게 고쳤는지, 사례에서 무엇을 배워야 하는지 설명해주세요.**

- 불필요한 `car` 접두사를 제거하여 간결하게 만들었습니다.
- 2장의 "불필요한 맥락을 없애라" 원칙을 적용했습니다.
- 이미 Car 객체 안에 있으니 중복된 맥락은 제거하는 것이 좋습니다.
