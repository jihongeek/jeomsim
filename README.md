# jeomsim
점심 식사 고민을 해결할 구글 스프레드시트, 디스코드를 이용한 간단한 **음식점** **추천 봇** 프로젝트

## Dependancy

### python3

* gspread
* requests

## 어떻게 작동합니까? 

파이썬 스크립트를 통한 구글 스프레드시트 조작 및 Discord 메시지 전송 with Github Actions workflow

<img width="800" alt="jeomsimwork" src="https://user-images.githubusercontent.com/34394165/130898016-b0c23519-5d26-4575-9514-f630fd7a6135.png">

## 파일설명

```
root of this repository
├─.github // 깃허브 관련 폴더
│  └─workflows // 깃허브 actions workflow 폴더
|    └──────── updater.yml // updater.py를 실행하는 workflow 설정파일
|	 └──────── webhook_sender.yml // webhook_sender.py를 실행하는 workflow 설정파일
├─jeomsim
│  └─updater.py // Google Forms로 추가된 음식점들을 stable(확정)인 워크시트로 옮기는 스크립트
|  └─webhook_sender.py // discord 서버로 음식점 리스트를 뽑아서 embed로 보내는 스크립트
├─README.md // 레포 설명을 위한 리드미 (지금 이 파일)
├─.gitignore // git이 추적하지 않는 파일,폴더 리스트 (가상환경 venv 폴더 등)
├─.requirements.txt // 프로젝트와 관련된 패키지 설치를 위한 파일 
```

## 시작하기

1. 레포 포크

2. cmd나 터미널을 키고 포크한 레포를 받을 디렉토리로 이동

    ```shell
    cd <이동할 경로>
    ```

3. 포크한 레포 로컬에 클론

    ```shell
    git clone <.git으로 끝나는 url주소>
    ```

4. 가상환경 설정
    ```shell
    python -m venv venv
    ```

5. 관련 패키지 설치

    ```shell
    pip install -r requirements.txt 
    ```

4. 수정

   1. 수정한 기능마다 파일 로컬 레포에 추가 및 커밋

      ``` shell
      git add <수정한 파일경로>
      git commit -m "수정한 내용"
      ```

   2. 포크한 레포에 push

      ``` shell
      git push origin main
      ```

   3. 포크한 레포에 가서 pull request 날리기 
   4. 레포 주인장이 검토 후에 반영