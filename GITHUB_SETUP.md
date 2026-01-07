# GitHub에 올리기 가이드

이 가이드는 봇을 GitHub 프라이빗 레포지토리에 안전하게 올리는 방법을 설명합니다.

## ⚠️ 시작하기 전에

**절대로 토큰을 GitHub에 올리지 마세요!** `.gitignore` 파일이 이미 설정되어 있어 안전합니다.

제외되는 파일들:
- `.env` - 실제 토큰이 들어있는 파일 ❌ 업로드 안 됨
- `config.py` - 토큰이 들어있는 파일 ❌ 업로드 안 됨
- `attendance_data.json` - 사용자 데이터 ❌ 업로드 안 됨

업로드되는 파일들:
- `.env.example` - 토큰 예시 파일 ✅ 업로드 됨
- `config_example.py` - 설정 예시 파일 ✅ 업로드 됨
- `bot.py` - 봇 코드 ✅ 업로드 됨
- 기타 문서 파일들 ✅ 업로드 됨

## 📋 단계별 가이드

### 1단계: Git 초기화

터미널에서 봇 폴더로 이동한 후:

```bash
cd /Users/ohseungyeon/discord-attendance-bot

# Git 초기화
git init

# 현재 상태 확인 (.env, config.py가 없는지 확인!)
git status
```

**중요:** `git status` 결과에 `.env`나 `config.py`가 보이면 안 됩니다!

### 2단계: GitHub 레포지토리 연결

```bash
# GitHub 원격 레포지토리 추가
git remote add origin https://github.com/syeony/wakeupcheckbot.git

# 확인
git remote -v
```

### 3단계: 첫 커밋 및 푸시

```bash
# 모든 파일 스테이징
git add .

# 다시 한번 확인 (.env, config.py가 staged에 없는지!)
git status

# 커밋
git commit -m "Initial commit: Discord attendance bot"

# GitHub에 푸시 (프라이빗 레포지토리)
git branch -M main
git push -u origin main
```

**GitHub 인증이 필요할 수 있습니다:**
- Personal Access Token을 사용하세요
- 또는 GitHub CLI (`gh auth login`)를 사용하세요

### 4단계: GitHub에서 확인

1. https://github.com/syeony/wakeupcheckbot 접속
2. 레포지토리가 **Private**인지 확인
3. `.env` 파일이 **없는지** 확인
4. `.env.example` 파일은 **있는지** 확인

## 🔒 보안 체크리스트

업로드 전에 반드시 확인하세요:

- [ ] `.gitignore` 파일에 `.env`가 포함되어 있음
- [ ] `.gitignore` 파일에 `config.py`가 포함되어 있음
- [ ] `.gitignore` 파일에 `attendance_data.json`이 포함되어 있음
- [ ] `git status`에 `.env`가 나타나지 않음
- [ ] `git status`에 `config.py`가 나타나지 않음
- [ ] 레포지토리가 **Private**으로 설정됨

## 📥 나중에 다른 곳에서 다운받을 때

```bash
# 레포지토리 클론
git clone https://github.com/syeony/wakeupcheckbot.git
cd wakeupcheckbot

# 패키지 설치
pip install -r requirements.txt

# .env 파일 생성
cp .env.example .env

# .env 파일 편집하고 실제 토큰 입력
nano .env
# 또는
code .env

# 봇 실행
python bot.py
```

## 🔄 코드 업데이트할 때

```bash
# 변경사항 확인
git status

# 모든 변경사항 추가
git add .

# 커밋
git commit -m "Update: 변경 내용 설명"

# 푸시
git push
```

## ⚠️ 실수로 토큰을 올렸다면?

1. **즉시 Discord Developer Portal에서 토큰 재생성**
2. GitHub에서 해당 커밋 삭제 (또는 레포지토리 삭제 후 재생성)
3. 새 토큰으로 `.env` 파일 업데이트

## 💡 팁

- `.env` 파일은 절대 `git add`하지 마세요
- 실수 방지를 위해 `git add .` 후 항상 `git status`로 확인하세요
- Private 레포지토리를 사용하세요 (이미 설정되어 있음)
- 정기적으로 백업하세요

## 문제 해결

**"remote origin already exists" 에러:**
```bash
git remote remove origin
git remote add origin https://github.com/syeony/wakeupcheckbot.git
```

**토큰 입력이 계속 요구됨:**
```bash
# GitHub CLI 사용 (권장)
gh auth login

# 또는 SSH 사용
git remote set-url origin git@github.com:syeony/wakeupcheckbot.git
```

**실수로 .env를 추가했다면:**
```bash
# 스테이징에서 제거
git reset .env

# .gitignore 다시 확인
cat .gitignore | grep .env
```
