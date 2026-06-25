# 📂 1. 프로젝트 폴더 구조 설정
개발할 PC(M1 Mac)에 아래와 같이 폴더와 파일들을 생성하고, `data` 폴더 안에 준비하신 '사내 정보보안 규정' 문서(텍스트 또는 PDF)를 넣어주세요.

```text
security-chatbot/
├── data/
│   └── 사내_정보보안_규정.txt    <-- 여기에 보안규정 문서 배치
├── app.py                     <-- RAG 및 가이드라인 핵심 소스코드
└── requirements.txt           <-- 필요한 파이썬 라이브러리 목록
```
----
# 구동 순서 
> [1] 내가 만든 프로젝트 폴더로 이동합니다.
    $ cd ~/Desktop/security-chatbot

> [2] 'myenv'라는 이름의 가상환경(독립된 방)을 생성합니다.
    $ python3 -m venv myenv

> [3] 생성한 가상환경을 활성화(입장)합니다.
    $ source myenv/bin/activate (mac)
    $ myenv/Script/activate.bat (window)
    ([확인] 활성화가 잘 되면 터미널 프롬프트 앞에 (myenv) 라고 표시됩니다)

> [4] 가상환경 내부의 pip(패키지 관리자)를 최신 버전으로 업데이트합니다.
    $ pip install --upgrade pip

> [5] 준비해둔 requirements.txt 안의 라이브러리들을 이 가상환경에만 설치합니다.
    $ pip install -r requirements.txt

> [6] (docker container가 이미 있는경우) 기존 컨테이너 중지 및 삭제 
    $ docker stop ollama
    $ docker rm ollama

> [7] [중요] 외부 연결 전면 허용 옵션을 넣어서 컨테이너 다시 생성
    $ docker run -d -v ollama:/root/.ollama -p 11434:11434 -e OLLAMA_HOST=0.0.0.0 --name ollama ollama/ollama

> [8] 컨테이너 안에 EXAONE이 잘 대기하고 있는지 확인 겸 실행
    $ docker exec -it ollama ollama run exaone3.5:2.4b

> [9] 이제 완벽하게 격리된 환경에서 RAG 챗봇 코드를 실행합니다!
    $ python app.py

----

# flow
graph TD
    %% 1단계
    subgraph Step1 [1단계: 맥북 바탕화면 폴더 작업]
        A[1. 맥북 바탕화면에 폴더 생성 <br> 이름: security-chatbot]
        A --> B[2. 폴더 안에 하위 폴더 생성 <br> 이름: data]
        B --> C[3. data 폴더 안에 규정 파일 저장 <br> 사내_정보보안_규정.txt]
        C --> D[4. VS Code 등으로 폴더 열고 <br> app.py / requirements.txt 파일 생성]
    end

    %% 2단계
    subgraph Step2 [2단계: Ollama 컨테이너 가동 터미널 작업]
        E[5. 맥북 터미널 실행]
        E --> F[6. docker run 명령어로 Ollama 실행 <br> 11434 포트 개방]
        F --> G[7. docker exec 명령어로 exaone3.5 다운로드]

        # 1. Ollama라는 이름의 컨테이너를 맥북 배경에서 실행 (포트 11434 개방)
            $ docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

        # 2. 방금 켠 컨테이너 속에 들어가서 EXAONE 모델 다운로드 및 준비시키기
            $ docker exec -it ollama ollama run exaone3.5:2.4b
    end

    %% 3단계
    subgraph Step3 [3단계: 내 파이썬 코드 실행 터미널 작업]
        H[8. 새 터미널 창 열기]
        H --> I[9. cd 명령어로 내 폴더 이동 <br> cd Desktop/security-chatbot]
        I --> J[10. 라이브러리 설치 <br> pip install -r requirements.txt]
        J --> K[11. 내 파이썬 코드 실행 <br> python app.py]
    end

    %% 연결 관계
    D -.->|코드가 실행되면서 파일 접근| K
    G -.->|컨테이너 내부에서 AI 대기| K
