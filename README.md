# 한글화 진행 중

일일이 번역하기에는 시간이 너무 소모되고, volunteer들을 이용하면 비효율적이라 인공지능 번역엔진을 이용해 보기로 함.
몇가지 이슈가 있기는 한데, 일단 달려 봄.


## 현재 진행 상황

- 번역기능 개발완료 
  - lib/world/wld/\*.wld
    - room data
  - lib/world/mob/\*.mob
    - mob data    

- 진행예정
  - lib/world/shp/\*.shp
    - shop data
  - lib/world/obj/\*.obj
    - object
  - lib/world/trg/
    - target?    

## Future TODO
- User Interface Source Codes
send_to_chars() 함수가 사용자에게 메시지를 보내는 함수로 보임.
이 함수에서 string argument를 끄집어 내어 번역한 후 다시 집어넣어 컴파일토록 할 계획임.

## 번역 API 선택

### Google Translation API vs Nave Papago API vs Kakao API

. | Google | Naver | Kakao
----|------- | ------|------
Quality | 대동소이 | 대동소이 | 대동소이
Price | High  | High | Free
무료지원 | n/a  | 10,000자/day | 쿼터있음, 수량확인불가 
URL 번역 | 지원 | 지원 | 미지원

### 번역 품질 비교

다 고만고만하다. 품질의 일관성(존댓말, 반말)은 구글과 네이버가 좋았고, 카카오는 섞여 나오는 경향이 있다. 아마 학습시킨 데이터에 반말/존댓말이 섞인 모양이다. ~~무료로 제공해 주는게 어딘가. 쌩유~ 카카오! 일일 제한이 있다. 있으면 있다고 알려 줘야지 ~~

- 원문 

> The river is deep, and runs swiftly in an east-west direction.  To the north the river eddies and enters a backwash where a small bank extends down from a dark, thick stand of trees.  It doesn't look particularly inviting however

- Google
> 강은 깊고 동서 방향으로 빠르게 달린다. 북쪽의 강은 소용돌이 치며 작은 나무가 어둡고 두꺼운 나무 줄기에서 흘러 내리는 역류로 들어갑니다. 그러나 특히 매력적이지는 않습니다.

- Papago

> '강은 깊고, 동서쪽으로 빠르게 흐른다. 북쪽으로는 강물이 소용돌이치며 작은 둑이 어둡고 두꺼운 나무 받침대에서 아래로 뻗어나가는 역세차 속으로 들어간다. 하지만 특별히 매력적으로 보이지는 않는다.'

- Kakao

> "강은 깊고 동서 방향으로 빠르게 흐릅니다.","북쪽으로는 강이 소용돌이 치며 작은 은행이 어둡고 두꺼운 나무 스탠드에서 뻗어있는 역류로 들어갑니다.","하지만 특별히 초대하는 것 같지는 않다"

## 번역 API Quota 회피하기

웹브라우저 테스트 툴킷으로 만들어진 셀레니움을 이용하는 방법을 사용함. 아래 github 링크의 내용대로 하면 안되어서 참고만 해서 새로 만듬.
구글에서 번역결과물이 표시되는 곳의 tag id, class등을 모두 null로 해 놓아서 response에서 번역결과물을 얻기 위해 Xpath로 직접 찾아들어가는 방법 사용함.
해당 Xpath는 크롬->보기->개발자도구 를 이용하면 찾을 수 있음. 
- https://github.com/animikhaich/Python-Google-Translate/blob/master/Python%20Google%20Translate/GoogleTranslate_Selenium.py
- https://selenium-python.readthedocs.io/locating-elements.html


**TODO** 구글 번역이 쪼끔 구리다. 파파고로 함 다시 해봐야겠다.

## 관련 자료

[World 파일 구조](https://www.circlemud.org/cdp/building/building-3.html)





