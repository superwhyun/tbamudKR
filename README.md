# 한글화 진행 중

일일이 번역하기에는 시간이 너무 소모되고, volunteer들을 이용하면 비효율적이라 인공지능 번역엔진을 이용해 보기로 함.

## 현재 진행 상황

- 번역기능 개발완료 (번역 API quota 부족...)
  - lib/world/wld/\*.wld
    - room data

- 진행예정
  - lib/world/shp/\*.shp
    - shop data
  - lib/world/mob/\*.mob
    - mob data

## Future TODO
- User Interface Source Codes
send_to_chars() 함수가 사용자에게 메시지를 보내는 함수로 보임.
이 함수에서 string argument를 끄집어 내어 번역한 후 다시 집어넣어 컴파일.
요놈은 시간을 솔찮이 잡아먹을 듯.. 아닐라나..

## 번역 API 선택

### Google Translation API vs Nave Papago API vs Kakao API

. | Google | Naver | Kakao
----|------- | ------|------
Quality | 대동소이 | 대동소이 | 대동소이
Price | High  | High | Free
무료지원 | n/a  | 10,000자/day | 쿼터있음, 수량확인불가 
URL 번역 | 지원 | 지원 | 미지원

### 번역 품질 비교

다 고만고만하다. 품질의 일관성(존댓말, 반말)은 구글과 네이버가 좋았고, 카카오는 섞여 나오는 경향이 있다. 아마 학습시킨 데이터에 반말/존댓말이 섞인 모양이다. ~~무료로 제공해 주는게 어딘가. 쌩유~ 카카오! 일일 제한이 있다. 있으면 있다고 알려줘야지요~~

- 원문 

> The river is deep, and runs swiftly in an east-west direction.  To the north the river eddies and enters a backwash where a small bank extends down from a dark, thick stand of trees.  It doesn't look particularly inviting however

- Google
> 강은 깊고 동서 방향으로 빠르게 달린다. 북쪽의 강은 소용돌이 치며 작은 나무가 어둡고 두꺼운 나무 줄기에서 흘러 내리는 역류로 들어갑니다. 그러나 특히 매력적이지는 않습니다.

- Papago

> '강은 깊고, 동서쪽으로 빠르게 흐른다. 북쪽으로는 강물이 소용돌이치며 작은 둑이 어둡고 두꺼운 나무 받침대에서 아래로 뻗어나가는 역세차 속으로 들어간다. 하지만 특별히 매력적으로 보이지는 않는다.'

- Kakao

> "강은 깊고 동서 방향으로 빠르게 흐릅니다.","북쪽으로는 강이 소용돌이 치며 작은 은행이 어둡고 두꺼운 나무 스탠드에서 뻗어있는 역류로 들어갑니다.","하지만 특별히 초대하는 것 같지는 않다"

## 번역 API Quota 회피하기

음. 이렇게 하면 될것 같긴 했는데, 역시 선각자들은 어디에나 있는 법.
https://github.com/animikhaich/Python-Google-Translate/blob/master/Python%20Google%20Translate/GoogleTranslate_Selenium.py



## 관련 자료

[World 파일 구조](https://www.circlemud.org/cdp/building/building-3.html)





