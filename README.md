# 한글화 진행 중

일일이 번역하기에는 시간이 너무 소모되고, volunteer들을 이용하면 비효율적이라 인공지능 번역엔진을 이용해 보기로 함.

## 한글화가 필요한 부분

### Wolrd 파일
lib/world/wld/ 디렉토리 밑에 world(room) 파일들이 있음.

### User Interface Source Codes
send_to_chars() 함수가 사용자에게 메시지를 보내는 함수로 보임.
이 함수에서 string argument를 끄집어 내어 번역한 후 다시 집어넣어 컴파일.

## 번역 API 선택

### Google Translation API vs Nave Papago API

- 번역 품질은 파파고 승
- 두 API 모두 유료이며, 무료로 사용할 수 있는 부분은 매우 한정적
- 웹페이지 번역이 가능하므로 파파고 이용하는 것으로 결정
- 하려 하였으나...

### KAKAO Translation AIP
- 아직 무료다.
- 얘로 하자.

### Papago vs Kakao 

번역 품질은 Papago 압승인 듯?

- 원문 

he river is deep, and runs swiftly in an east-west direction.  To the north the river eddies and enters a backwash where a small bank extends down from a dark, thick stand of trees.  It doesn't look particularly inviting however


- Papago

{'message': {'@type': 'response', '@service': 'naverservice.nmt.proxy', '@version': '1.0.0', 'result': {'srcLangType': 'en', 'tarLangType': 'ko', 'translatedText': '강은 깊고, 동서쪽으로 빠르게 흐른다. 북쪽으로는 강물이 소용돌이치며 작은 둑이 어둡고 두꺼운 나무 받침대에서 아래로 뻗어나가는 역세차 속으로 들어간다. 하지만 특별히 매력적으로 보이지는 않는다.'}}}


- Kakao

{"translated_text":[["강은 깊고 동서 방향으로 빠르게 흐릅니다.","북쪽으로는 강이 소용돌이 치며 작은 은행이 어둡고 두꺼운 나무 스탠드에서 뻗어있는 역류로 들어갑니다.","하지만 특별히 초대하는 것 같지는 않다"]]}





## 관련 자료

[World 파일 구조](https://www.circlemud.org/cdp/building/building-3.html)





