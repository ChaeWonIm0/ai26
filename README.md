# ai26

## 테스트

##### 2023-04-14 일기쓰기, 공지사항, 공개일기장, 로그인/회원가입 기능이 포함된 flask 파일 넣음 (채원)
##### 2023-04-17 (전체 공유) 일기쓰기에 문법교정 기능, 일기 내용 태그 생성(문장 요약) 미완성, 공개일기장 형태 수정. 
##### 2023-04-19 (for 상준, 진혁) 공유를 위해서 깃허브에 myproject 업로드. 폴더 청소함. (채원)
##### 2023-04-24 (for 전체공유) 
##### (해결함) "Truncation was not explicitly activated but `max_length` is provided a specific value, please use `truncation=True` to explicitly truncate examples to max length. Defaulting to 'longest_first' truncation strategy. If you encode pairs of sequences (GLUE-style) with the tokenizer you can select this strategy more precisely by providing a specific strategy to `truncation`." <br>
grammar.py 관련 문제 : 검토+저장하기를 클릭했을 때, 문장이 모두 문법 검사된 상태로 배출되지 않고, 50%는 생략되서 나오는 문제가 발생. <br>
max_length, truncation 문제로 추측 진행. <br>
~~현시점까지 오류를 해결하지 못해서 공유.(채원)~~
##### 2023-04-26 (for 전체공유) 04-25까지 작업한 코드 덮어씌우기로 삭제됨. 회원정보 수정기능, 일기 문법검사 기능 복구중.
##### 04-26 + 공개일기장 정렬기능 추가
