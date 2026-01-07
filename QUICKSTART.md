# 빠른 시작 가이드

## 5분 안에 봇 실행하기

### 1단계: Python 설치 확인

터미널에서 다음 명령어를 실행하세요:

```bash
python --version
```

Python 3.8 이상이 설치되어 있어야 합니다. 없다면 [python.org](https://www.python.org/downloads/)에서 설치하세요.

### 2단계: 디스코드 봇 만들기

1. https://discord.com/developers/applications 접속
2. **"New Application"** 클릭
3. 이름 입력 (예: "기상체크봇")
4. 좌측 **"Bot"** 메뉴 클릭
5. **"Add Bot"** 클릭
6. **"Reset Token"** 클릭하고 토큰 복사 (중요: 절대 공유하지 마세요!)

### 3단계: 봇을 서버에 초대

1. 좌측 **"OAuth2"** > **"URL Generator"** 클릭
2. **SCOPES**에서 다음 체크:
   - ✅ `bot`
   - ✅ `applications.commands` **(중요! 슬래시 커맨드 필수)**
3. **BOT PERMISSIONS**에서 다음 체크:
   - ✅ Read Messages/View Channels
   - ✅ Send Messages
   - ✅ Read Message History
4. 하단의 **생성된 URL** 복사
5. 새 탭에서 URL 접속하여 봇을 서버에 초대

### 4단계: 봇 설정

터미널에서 다음 명령어를 실행하세요:

```bash
# 프로젝트 폴더로 이동
cd discord-attendance-bot

# 필요한 패키지 설치
pip install -r requirements.txt

# .env 파일 생성 (권장)
cp .env.example .env
```

이제 텍스트 에디터로 `.env` 파일을 열고, 토큰을 입력하세요:

```bash
# 에디터로 .env 파일 열기
nano .env
# 또는
code .env
```

`.env` 파일 내용:
```
DISCORD_BOT_TOKEN=여기에_2단계에서_복사한_토큰_붙여넣기
```

### 5단계: 봇 실행

```bash
python bot.py
```

"봇이 준비되었습니다!"라는 메시지가 나오면 성공입니다! 🎉

### 6단계: 테스트

디스코드 서버에서 슬래시 커맨드를 테스트해보세요!

1. 디스코드 채팅창에 `/` 입력
2. 봇의 명령어 목록이 자동완성으로 나타남 (기상, 지각확인, 내기록, 도움말)
3. `/기상` 선택하여 실행

**Tip:** `/`를 입력하면 봇 명령어가 자동으로 뜹니다! 클릭만 하면 됩니다!

**중요:** 봇이 24시간 실행되고 있어야 매일 밤 11시 59분 자동 지각 체크가 작동합니다!

---

## 문제가 생겼나요?

### "discord 모듈을 찾을 수 없습니다" 오류

```bash
pip install discord.py
```

### "pytz 모듈을 찾을 수 없습니다" 오류

```bash
pip install pytz
```

### 슬래시 커맨드가 안 보여요

1. 봇 초대할 때 `applications.commands` 권한을 체크했는지 확인
2. 봇 재시작 후 1-2분 정도 기다려보기
3. 디스코드 앱 완전 종료 후 재실행
4. 봇을 다시 초대해보기 (3단계 다시 진행)

### 봇이 응답하지 않아요

1. 봇이 실행 중인지 확인 (터미널에서)
2. 디스코드 서버에서 봇이 온라인 상태인지 확인
3. 봇이 메시지를 볼 수 있는 권한이 있는지 확인
4. 터미널에 "슬래시 커맨드가 동기화되었습니다!" 메시지가 나타났는지 확인

### Mac에서 pip 명령어가 안 될 때

```bash
pip3 install -r requirements.txt
python3 bot.py
```

---

## 다음 단계

### 사용 방법
- 평일 오전 8-10시에 `/기상` 명령어로 기상 체크
- `/지각확인`으로 이번 달 지각 현황 확인
- `/전체기록`으로 최근 3개월 지각 현황 확인
- `/내기록`으로 내 기상 기록 확인
- `/도움말`로 모든 명령어 보기

### 자동 지각 체크 🤖
- 매일 밤 11시 59분에 자동으로 미출석자 체크
- 평일에 `/기상` 안 하면 자동으로 지각 처리
- 봇이 24시간 실행 중이어야 작동함!

자세한 내용은 `README.md`를 참고하세요!
