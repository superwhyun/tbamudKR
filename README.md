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


## 관련 자료

[World 파일 구조](https://www.circlemud.org/cdp/building/building-3.html)





