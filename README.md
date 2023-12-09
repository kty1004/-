# 연예인 사진 수집기
네이버 프로필 사진을 학습하여 연예인 사진을 크롤링 하는 프로그램입니다.
## 간단한 작동방식
1. 연예인 사진을 크롤링하기 위해 해당 인물의 네이버 프로필 사진을 수집하고, 이를 [face recognition](https://github.com/ageitgey/face_recognition/blob/master/README_Korean.md)에 넣습니다.
2. 네이버 검색 api를 사용하여 연애인 이름을 검색하여 뜨는 사진을 전부 다운로드한다음, [face recognition](https://github.com/ageitgey/face_recognition/blob/master/README_Korean.md)을 사용하여 해당 인물이 맞는지와 해당 인물만 있는지 확인합니다.
3. 해당 인물이 맞다면 해당 사진을 저장하고, 아니면 삭제합니다.
---
## 코린이들을 위한 Colab version
Colab에서도 사용할 수 있도록 만들었습니다. [이 링크](Celebrity_solo_shot_collector_for_Colab.ipynb)
를 클릭하면 Colab에서 사용할 수 있는 파일이 열립니다.

---
## 사용법
### A. 네이버 검색 api 키 발급
1. [네이버 게발자 센터](https://developers.naver.com/main/)에서 키를 발급받습니다.
2. 이를 환경변수에 등록합니다.
#### Windows에서 환경 변수 설정
1. 제어판 -> 시스템 -> 고급 시스템 설정 -> 환경 변수
2. 시스템 변수에서 새로 만들기를 누르고, 변수 이름에 `NAVER_CLIENT_ID`를 입력하고, 변수 값에 발급받은 Client ID를 입력합니다.
>자세한 환경변수 이름 설정은 **Linux와 MacOS에서 환경 변수 설정**을 참고하세요.

#### Linux와 MacOS에서 환경 변수 설정
터미널에 다음의 명령어를 입력합니다.
```bash
open ~/.bash_profile  # bash를 사용하는 경우
open ~/.zshrc  # zsh를 사용하는 경우
```
파일이 열리면 아래와 같이 환경 변수를 추가합니다.
```bash
export NAVER_CRAWLER_CLIENT_ID='your_client_id'
export NAVER_CRAWLER_CLIENT_PASSWORD='your_client_password'
```
파일을 저장하고 닫은 후, 터미널을 닫고 다시 열거나, 아래 명령어를 실행하여 변경 사항을 적용합니다:
```bash
source ~/.bash_profile  # bash를 사용하는 경우
source ~/.zshrc  # zsh를 사용하는 경우
```

### B. 크롤링할 연예인 이름 설정
**Celebrity_name.txt** 파일에 크롤링할 연예인 이름을 한 줄에 하나씩 입력합니다.
> 이 때 Celebrity_name.txt파일은 root 폴더에 위치해야 합니다.

### C. 프로그램 실행
main.py를 실행하기만 하면 됩니다. 

---
## 기타 설명
### 생성되는 폴더 설명
아래의 목록은 프로그램이 실행되면 생성되는 폴더들입니다.
- naver_profile: 수집한 네이버 프로필 사진을 저장하는 폴더입니다.
- img_source: 크롤링한 사진을 저장하는 폴더입니다.
- img_result: 크롤링한 사진 중 인물이 맞는 사진을 저장하는 폴더입니다.
### 다시 프로그램을 실행하고 싶은 경우
생성되는 폴더들을 삭제하고 다시 실행하면 됩니다. __(Celebrity_name.txt는 삭제하지 않습니다.)__
> 생성되는 폴더들을 삭제하지 않아도 실행이 되나, img_results 폴더에 중복된 사진이 저장될 수 있습니다.
### 콘솔창에서 출력되는 메시지 설명
#### '해당 이미지 링크에서 이미지 다운로드 실패'
해당 이미지 링크에서 이미지를 다운로드 받지 못했을 때 출력됩니다. 이는 해당 링크에서 이미지를 다운로드받지 못하는 경우를 말합니다. 본 프로그램에서는 이를 무시하고 다음 이미지를 다운로드 받습니다.
#### 'img_results 폴더 안의 사진 분포 : ...'
 img_results 폴더 안에 저장된 사진의 분포를 출력합니다. 이는 해당 폴더 안에 저장된 특정 인물의 사진의 수가 목표치의 사진 수랑 비교하기 위함입니다.

---

 # 주의 사항
 1. 사진을 모을 사람의 이름을 명확하게 입력해야 합니다. (예: '김연아'는 '연아'로 입력하면 안됩니다.)
 2. 동명이인이 있을 경우, 해당 인물의 사진이 아닌 다른 인물의 사진이 저장될 수 있습니다. 이를 피하기 위해 직업과 같은 추가 정보를 입력하면 좋습니다.
 3. 네이버를 사용하기 때문에, 네이버에 등록되지 않은 인물의 사진은 크롤링할 수 없습니다.
 4. 프로필을 성공적으로 찾았어도, 해당 인물의 프로필에 얼굴이 온전히 나와있지 않으면, 이미지 크롤링 결과에서 다른 사람의 사진이 있는 등 크롤링의 결과가 좋지 않을 수 있습니다. 
 >[프로필에 얼굴이 온전히 나와 있지 않은 경우](https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%9D%B4%EC%A4%80&oquery=%EB%B0%B0%EC%9A%B0+%EA%B9%80%EB%B2%94&tqi=iUek3dqVOsossFXwmnGssssstDK-196460)를 참고하세요.
