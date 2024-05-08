<h1 align="center">
  <br>
  <a href="https://github.com/e-commerce-www/MALL.git"><img src="https://github.com/e-commerce-www/MALL/assets/158125247/2bd4c467-8770-40b4-975a-4b4060b01b9d" alt="MVP" width="500"></a>
</h1>

<h4 align="center">
A music platform for indie musicians to sell their tracks and for buyers to legally use them in creative projects.</h4>

<p align="center">
<a href="https://github.com/e-commerce-www/MALL/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-v3.10.12-yellow"></a>
<a href="https://github.com/e-commerce-www/MALL.git"><img src="https://img.shields.io/badge/PRs-welcome-green"></a>
<a href="https://www.paypal.me/madEffort"><img src="https://img.shields.io/badge/$-donate-ff69b4"></a>
</p>

<p align="center">
  <a href="#key-features">Key Features</a> • <a href="#database-erd">Database ERD</a> • <a href="#how-to-use">How To Use</a> • <a href="#download">Download</a> • <a href="#credits">Credits</a> • <a href="#related">Related</a> • <a href="#support">Support</a> • <a href="#license">License</a>
</p>

<img src="https://github.com/e-commerce-www/MALL/assets/158125247/53dd779e-7971-40c9-a5a2-57c434e0141c" alt="MVP"/>

## What is Music Value Platform?


## Key Features
* ### 로그인/회원가입 -> 구글,네이버 소셜 로그인 및 가입 지원.
  
* ### 맘에 드는 음악 찜하기/취소하기
  
   - NavBar에 '찜한음악' 클릭 시 표시됩니다
     
     + 자신이 찜한 음악의 썸네일, 타이틀, 아티스트명, 가사 버튼, mp3 플레이어, 구매버튼이 표시됨. 찜 취소시 목록에서 삭제됩니다.
       
     + 최근들은 음악: 최근 들은 음악 10개가 표시됨. 가장 최근 음악이 맨 위로 올라오고 들은지 가장 오래된 음악이 삭제됩니다.
       
* ### 마이페이지(홈/구매내역/판매내역/팔로우)
  
  - 홈
    
    + 프로필 이미지 및 닉네임을 변경 가능.
    + 구매자의 경우 [찜한음악, 판매자 신청하러 가기] 두개의 바로가기가 표시됩니다.
    + 구매자의 경우 자신이 최근에 구매한 9개의 음악 썸네일이 입체적으로 표시됩니다.
      
  - 구매내역
    
    + 구매한 음악의 구매날짜, 제목, 제작자, 가격이 최신순으로 표시됩니다.
    + 구매날짜 클릭 시, 결제 정보를 더 상세하게 확인 가능합니다.
      
  - 판매내역
    
    + 자신이 판매한 음악의 등록날짜, 제목, 총 구매자의 수, 총 수익이 표시됩니다.
      
  - 팔로우
    
    + 자신이 팔로우 중인 아티스트들이 표시됩니다.
    + 팔로우한 아티스트들의 최근 활동 내역이 표시됩니다.
    + 팔로우 취소버튼을 누르면 팔로우 목록에서 삭제됩니다.

* ### 음악 업로드(판매자 전용)
  
  - 음악은 판매자만 업로드 할 수 있습니다.
  - 타이틀, 장르, 템포, 썸네일, 음원파일은 필수 입력 사항이고, 가사는 옵션입니다.
  - 음악의 가격은 3000원으로 통일됩니다.

* ### 홈페이지(검색/ 신곡/ TOP5)

  - 검색

    + 노래 제목으로 검색이 가능합니다.
    + 노래 제목이 중복되는 경우가 존재할 경우'노래명;아티스트명'으로 특정 노래 검색이 가능합니다.

  - 신곡

    + 가장 최근 등록된 음악 4곡이 표시됩니다
   
  - TOP5

    + 상위 랭킹 5위까지의 음악이 표시됩니다.

      + 순위 산정 기준은 '시간 가중치 순위 알고리즘'을 사용합니다.
      + 노래 클릭 후 좋아요를 누르면 누적 좋아요가 아닌 당일눌린 좋아요 증가치 순위로 순위를 매깁니다.
        
        #### 시간 가중치 순위 알고리즘
        
         1. 코드식: L_decayed = sum(0.5 ** ((t_now - t_i) / T) for i in range(1, n+1))
         2. L_decayed 는 시간 가중치가 적용된 좋아요 수 입니다.
         3. n 은 곡에 대한 좋아요의 총 개수입니다.
         4. t_now는 현재 시간입니다.
         5. T는 반감기(halflife)로, 좋아요의 가중치가 절반으로 줄어드는 데 걸리는 시간입니다.
         6. 0.5 ** ((t_now - t_i) / T) for i in range(1, n+1) 는 각 좋아요의 시간에 따른 가중치입니다
           
        + 좋아요를 누른 순간부터 시간이 지날수록 점수가 계속 떨어지는 방식입니다.
        + 좋아요의 수가 같아도 최근에 좋아요가 눌린 음악이 순위가 더 높습니다.

* ### 차트화면(최신순/인기순/장르별/템포별/검색)

  - NavBar에 '음악'을 누르면 표시되는 화면입니다.
  - 최신순
    
    + 최근에 업로드 된 음악 순으로 표시됩니다.
      
  - 인기순
    
    + 랭킹 알고리즘으로 산출된 점수가 높은 순으로 표시됩니다.
      
  - 장르별/ 템포별/ 검색
    
    + 장르, 템포 및 제목으로 음악을 필터링하여 검색합니다.

## Database ERD

To view the **`Database ERD`**, please click [here](https://www.erdcloud.com/p/JYqD8jKydarZYmrxE).
               
## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com) and [Python](https://www.python.org/downloads/) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/e-commerce-www/MALL.git

# Go into the repository
$ cd MALL

# Install dependencies
$ pip install -r requirements.txt
or
$ poetry install
```

After setting up the database and templates, please use the `makemigrations`, `migrate` and `collectstatic` commands.

```bash
# Run the app
$ python manage.py runserver
```

## Download

You can [download](https://github.com/e-commerce-www/MALL/releases) the latest release version of the MVP(Music-Value-Platform).

## Credits

This software uses the following open source packages:

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Bootstrap5](https://getbootstrap.com/)

## Related

- [Amazon Web Service](https://aws.amazon.com/) : AWS S3
- [Twilio](https://www.twilio.com) : SMS Phone Verification
- [PortOne](https://www.portone.io) : Payment Module

## Support

<a href="https://www.paypal.com/paypalme/madEffort">
<img src="https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png" alt="Donate with PayPal" width="200">
</a>

## License

This project adheres to the Apache-2.0 license, and you can find more detailed information in the [LICENSE](https://github.com/e-commerce-www/MALL/blob/main/LICENSE)

---

> GitHub <br>
> [@madEffort](https://github.com/madEffort) &nbsp;&middot;&nbsp; [@2taeyeon](https://github.com/2taeyeon) &nbsp;&middot;&nbsp; [@chlryddk](https://github.com/chlryddk) &nbsp;&middot;&nbsp; [@HalalGuys1232](https://github.com/HalalGuys1232) &nbsp;&middot;&nbsp; [@ieunchan](https://github.com/ieunchan) &nbsp;&middot;&nbsp; [@KMJ7916](https://github.com/KMJ7916)




