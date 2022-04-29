## 👩‍💻 Team
- **[양수영](github.com/tasddc1226)**
- **[권은경](github.com/fore0919)**
- **[윤상민](github.com/redtea89)**

`프로젝트 진행 기간 2022.04.26 09:00 ~ 2022.04.29 18:00`

[`Team-A-notion`](https://pretty-marlin-13a.notion.site/Team-A-03cf51c7174847ce88a6302e6939ea2a)


## 🛠 기술 스택
<img src="https://img.shields.io/badge/python-3776AB?style=plastic&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/django-092E20?style=plastic&logo=django&logoColor=white">
<img src="https://img.shields.io/badge/mysql-C70D2C?style=plastic&logo=mysql&logoColor=white">
<img src="https://img.shields.io/badge/docker-2496ED?style=plastic&logo=docker&logoColor=white">


## 🍦 서비스 개요
- 광고주가 제공한 회원의 화면데이터(클릭 수, 화면전환, 광고노출수 등)를 이용하여 광고효과를 정량적으로 제공한다.

## 사용자 요구사항 정의
- 주어진 데이터셋을 요구사항대로 서빙하기위한 데이터베이스를 설계
    - [x] 주어진 데이터 csv를 DB에 적재
    - [x] 데이터셋 테이블의 advertiser와 date, media는인덱싱 기능을 포함
- 아래 기능을 제공하는 REST API 서버를 개발
    - 광고주 등록
        - [x] 광고주이름, 이메일, 핸드폰번호 필드 추가
        - [ ] 자동으로 광고주 id 생성
    - 광고주 정보 수정
        - [x] 광고주이름, 이메일, 핸드폰번호만 수정가능
    - 광고주 삭제
        - [x] 광고주를 삭제하면 관련된 광고데이터 삭제
    - 광고주 목록 조회
        - [x] 고유id, 이름, 이메일, 핸드폰번호가 보이도록
    - 분석데이터 조회
        - [x] 광고주 고유번호(adviser_id), 기간(date)을 입력하여 조회
            - 기간은 start_date, end_date로 입력
            - 분석데이터는 매체(media)별로 그룹지어 나타냄
            - 분석결과는 아래와 같이 나타내되 json형식에 맞게 리턴
                - CTR = click * 100 / impression (백분율 %, 소수점 둘째까지출력)
                - ROAS = cv * 100 / cost (백분율 %, 소수점 둘째까지출력)
                - CPC = cost / click (소수점 둘째까지출력)
                - CVR = conversion * 100 / click (백분율 %, 소수점 둘째까지출력)
                - CPA = cost / conversion (소수점 둘째까지출력)



## DB Modeling
![madup-db](https://user-images.githubusercontent.com/55699007/165890362-65309bbb-0e77-4396-bbcb-973b2dc94f3f.png)


---
## 광고주 CRUD
- `POST` `/api/v1/advertisers/signin`
  - 요청 Body
    ```json
      {
      "advertiser_id": "19971226",
      "name": "tasddc",
      "email": "tasddc@naver.com",
      "phone": "010-1234-1234"
      }
    ```
  - server 응답
    ```json
      {
        "message": "SUCCESS"
      }
    ```
- `GET` `/api/v1/advertisers/<str:advertiser_id>`
  - 요청 Body : `None`
  - server 응답
    ```json
      {
        "result": {
          "advertiser_id": "19971226",
          "name": "tasddc",
          "email": "tasddc@naver.com",
          "phone": "010-1234-1234"
        }
      }
    ```

- `PATCH` `/api/v1/advertisers/<str:advertiser_id>`
  - 요청 Body
    ```json
      {
        "email": "admin@admin.com",
        "name": "홍길동",
        "phone": "010-9999-8888"
      }
    ```
  - server 응답
    ```json
    {
      "message": "SUCCESS"
    }
    ```
  - 변경 후 조회 결과
    ```json
    {
      "result": {
        "advertiser_id": "19971226",
        "name": "홍길동",
        "email": "admin@admin.com",
        "phone": "010-9999-8888"
      }
    }
    ```


- `DELETE` `/api/v1/advertisers/<str:advertiser_id>`
  - 요청 Body : `None`
  - server 응답
    ```json
      {
        "message": "SUCCESS"
      }
    ```
  - 광고주 삭제 후 재삭제 요청에 대한 server 요청
    ```json
      {
        "message": "ADVERTISER_DOES_NOT_EXIST"
      }
    ```

---
## 기간 내 광고 효율 분석 API

- `GET` `/api/v1/ads/analysis-detail`
  - 요청 쿼리 data set : `advertiser_id`, `start_date`, `end_date`

- 특정 광고주의 특정 기간 내의 광고 효율 데이터를 받아오기 위한 예시 요청
  - `/api/v1/ads/analysis-detail?advertiser_id=37445071&start_date=2022.04.01&end_date=2022.04.30`

- 예시 요청에 대한 server 응답
  ```json
    {
      "naver": {
        "ctr": 1.63,
        "roas": 514.28,
        "cpc": 47850.01,
        "cvr": 9.72,
        "cpa": 492212.26
      },
      "facebook": {
        "ctr": 1.51,
        "roas": 155.49,
        "cpc": 68889.16,
        "cvr": 35.08,
        "cpa": 196363.81
      },
      "google": {
        "ctr": 14.72,
        "roas": 545.5,
        "cpc": 22409.06,
        "cvr": 67.77,
        "cpa": 33065.92
      }
    }
  ```
  
