## **REDI Project**
REDI 프로젝트는 2022 빛가람 에너지밸리 소프트웨어 작품 경진대회에 참가하기 위해 개발한 웹 사이트 입니다.<br>
REDI란 Reduce Disposable Items로 일회용품을 줄이자는 의미를 가지고 있습니다. 이 웹 사이트는 사용자의 <br>
일회용품 사용량을 기록하고 직접 눈으로 확인할 수 있으며 경각심을 느끼게 하고 일회용품을 대체하는 대체품 <br>
들도 알려주면서 일회용품 사용량을 줄이자! 라는 목적을 가진 작품입니다.<br>

<br>

### **[다이어그램 간략 설명]**

먼저 클라이언트가 장고에게 요청을 날립니다. 그 요청을 처리할 때 DB의 데이터가 필요하면 꺼내서 클라이언트에게 넘기고,<br>
만약 클라이언트가 소셜로그인을 카카오나 디스코드로 한다면 API로 사용자 인증을 거쳐 로그인 할 수 있게 해줍니다.<br> 
또한 클라이언트가 차트를 요청하면 Chart.js 라이브러리를 사용하여 클라이언트에게 보여주고 장고에서 클라이언트로 <br> 
넘어가는 html 응답들은 모두 tailwindCSS를 거쳐 랜더링됩니다.

### **[TEAM FBIT]** <br>

REDI Project를 함께 개발한 팀원들입니다.<br><br>
Front, Back - 김원욱<br><br>
Front, Back - 김종한<br><br>
Front, Design - 김주은<br><br>
Back, Design - 이현준<br><br>
Front, Design - 정민서<br><br>
