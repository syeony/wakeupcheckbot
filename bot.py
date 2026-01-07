import discord
from discord import app_commands
from discord.ext import tasks
from datetime import datetime, time
import pytz
import json
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True

class AttendanceBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # 슬래시 커맨드 동기화
        await self.tree.sync()
        print("슬래시 커맨드가 동기화되었습니다!")

        # 자동 체크 태스크 시작
        if not daily_attendance_check.is_running():
            daily_attendance_check.start()

bot = AttendanceBot()

# 한국 시간대
KST = pytz.timezone('Asia/Seoul')

# 데이터 파일
DATA_FILE = 'attendance_data.json'

# 데이터 로드
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 데이터 저장
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 데이터 초기화
attendance_data = load_data()

@bot.event
async def on_ready():
    print(f'{bot.user.name} 봇이 준비되었습니다!')
    print(f'봇 ID: {bot.user.id}')
    print(f'슬래시 커맨드를 사용하려면 /기상, /지각확인 등을 입력하세요!')
    print(f'자동 출석 체크: 매일 밤 11시 59분 (KST) 실행')

# 매일 밤 11시 59분에 실행되는 자동 체크 태스크
@tasks.loop(time=time(hour=14, minute=59, tzinfo=pytz.UTC))  # KST 23:59 = UTC 14:59
async def daily_attendance_check():
    global attendance_data

    now = datetime.now(KST)
    current_day = now.weekday()  # 0=월요일, 6=일요일

    # 주말이면 체크 안 함
    if current_day >= 5:
        print(f"[자동 체크] 오늘은 주말({now.strftime('%Y-%m-%d')})이라 체크하지 않습니다.")
        return

    print(f"[자동 체크] {now.strftime('%Y-%m-%d')} 평일 출석 체크 시작...")

    current_year = now.year
    current_month = now.month
    month_key = f"{current_year}-{current_month:02d}"
    date_key = now.strftime('%Y-%m-%d')

    # 전체 기록에서 모든 사용자 ID 수집 (한 번이라도 기상 체크를 한 사람들)
    all_user_ids = set()
    for month_data in attendance_data.values():
        for user_id in month_data.keys():
            all_user_ids.add(user_id)

    # 이번 달 데이터 구조 초기화
    if month_key not in attendance_data:
        attendance_data[month_key] = {}

    absent_count = 0

    # 각 사용자별로 오늘 기록 확인
    for user_id in all_user_ids:
        # 이번 달 사용자 데이터 초기화
        if user_id not in attendance_data[month_key]:
            # 과거 기록에서 이름 찾기
            user_name = None
            for month_data in attendance_data.values():
                if user_id in month_data:
                    user_name = month_data[user_id].get('name', f'User_{user_id}')
                    break

            attendance_data[month_key][user_id] = {
                'name': user_name or f'User_{user_id}',
                'tardiness': 0,
                'records': {}
            }

        # 오늘 기록이 없으면 지각 처리
        if date_key not in attendance_data[month_key][user_id]['records']:
            attendance_data[month_key][user_id]['tardiness'] += 1
            absent_count += 1
            user_name = attendance_data[month_key][user_id]['name']
            print(f"  - {user_name}님: 미출석 → 지각 +1 (총 {attendance_data[month_key][user_id]['tardiness']}회)")

    # 데이터 저장
    save_data(attendance_data)

    print(f"[자동 체크] 완료! 총 {absent_count}명이 지각 처리되었습니다.")

@bot.tree.command(name="기상", description="평일 오전 8시~10시 사이에 기상 체크를 합니다")
async def wake_up(interaction: discord.Interaction):
    # 현재 한국 시간
    now = datetime.now(KST)
    current_hour = now.hour
    current_minute = now.minute
    current_day = now.weekday()  # 0=월요일, 6=일요일
    current_month = now.month
    current_year = now.year

    # 평일 체크 (월~금)
    if current_day >= 5:  # 토요일(5), 일요일(6)
        await interaction.response.send_message(
            f"{interaction.user.display_name}님, 주말에는 기상 체크를 하지 않습니다! 😴"
        )
        return

    # 사용자 정보
    user_id = str(interaction.user.id)
    user_name = interaction.user.display_name
    date_key = now.strftime('%Y-%m-%d')
    month_key = f"{current_year}-{current_month:02d}"

    # 데이터 구조 초기화
    if month_key not in attendance_data:
        attendance_data[month_key] = {}

    if user_id not in attendance_data[month_key]:
        attendance_data[month_key][user_id] = {
            'name': user_name,
            'tardiness': 0,
            'records': {}
        }

    # 이미 오늘 기상 체크를 했는지 확인
    if date_key in attendance_data[month_key][user_id]['records']:
        existing_time = attendance_data[month_key][user_id]['records'][date_key]
        await interaction.response.send_message(
            f"{user_name}님, 오늘은 이미 {existing_time}에 기상 체크를 하셨습니다!"
        )
        return

    # 시간 체크
    current_time_str = now.strftime('%H:%M')

    # 8시~10시 사이: 정상 기상
    if (current_hour == 8) or (current_hour == 9) or (current_hour == 10 and current_minute == 0):
        attendance_data[month_key][user_id]['records'][date_key] = current_time_str
        save_data(attendance_data)
        await interaction.response.send_message(
            f"✅ {user_name}님 기상 확인되었습니다! (시간: {current_time_str})"
        )

    # 10시 이후: 지각
    elif current_hour >= 10:
        attendance_data[month_key][user_id]['records'][date_key] = current_time_str
        attendance_data[month_key][user_id]['tardiness'] += 1
        save_data(attendance_data)
        await interaction.response.send_message(
            f"⏰ {user_name}님 기상 확인되었습니다! (시간: {current_time_str}) - 지각 처리되었습니다."
        )

    # 8시 이전: 너무 이른 기상
    else:
        await interaction.response.send_message(
            f"{user_name}님, 기상 체크는 오전 8시부터 가능합니다! (현재: {current_time_str})"
        )

@bot.tree.command(name="지각확인", description="이번 달 전체 지각 현황을 확인합니다")
async def check_tardiness(interaction: discord.Interaction):
    now = datetime.now(KST)
    current_month = now.month
    current_year = now.year
    month_key = f"{current_year}-{current_month:02d}"

    if month_key not in attendance_data or not attendance_data[month_key]:
        await interaction.response.send_message(f"[{current_month}월] 아직 기록이 없습니다.")
        return

    # 결과 메시지 작성
    result = f"**[{current_month}월 지각 현황]**\n"

    # 사용자별 지각 횟수 정렬 (지각 많은 순)
    users = attendance_data[month_key].items()
    sorted_users = sorted(users, key=lambda x: x[1]['tardiness'], reverse=True)

    for user_id, user_data in sorted_users:
        name = user_data['name']
        tardiness = user_data['tardiness']
        result += f"• {name}님: 지각 {tardiness}번\n"

    await interaction.response.send_message(result)

@bot.tree.command(name="내기록", description="내 이번 달 기상 기록을 확인합니다")
async def my_record(interaction: discord.Interaction):
    now = datetime.now(KST)
    current_month = now.month
    current_year = now.year
    month_key = f"{current_year}-{current_month:02d}"
    user_id = str(interaction.user.id)
    user_name = interaction.user.display_name

    if month_key not in attendance_data or user_id not in attendance_data[month_key]:
        await interaction.response.send_message(f"{user_name}님, 이번 달 기록이 없습니다.")
        return

    user_data = attendance_data[month_key][user_id]
    tardiness = user_data['tardiness']
    records = user_data['records']

    result = f"**{user_name}님의 {current_month}월 기상 기록**\n"
    result += f"총 지각: {tardiness}번\n\n"
    result += "**상세 기록:**\n"

    for date, time in sorted(records.items()):
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        weekday = ['월', '화', '수', '목', '금', '토', '일'][date_obj.weekday()]
        result += f"• {date} ({weekday}) - {time}\n"

    await interaction.response.send_message(result)

@bot.tree.command(name="전체기록", description="최근 3개월의 지각 현황을 확인합니다")
async def all_records(interaction: discord.Interaction):
    if not attendance_data:
        await interaction.response.send_message("아직 기록이 없습니다.")
        return

    now = datetime.now(KST)

    # 최근 3개월의 month_key 생성
    recent_months = []
    for i in range(3):
        # i개월 전 계산
        year = now.year
        month = now.month - i

        # 월이 0 이하가 되면 작년으로
        while month <= 0:
            month += 12
            year -= 1

        month_key = f"{year}-{month:02d}"
        recent_months.append(month_key)

    # attendance_data에 있는 것 중 최근 3개월에 해당하는 것만 필터링
    filtered_months = [m for m in recent_months if m in attendance_data]

    if not filtered_months:
        await interaction.response.send_message("최근 3개월 기록이 없습니다.")
        return

    result = "**[최근 3개월 지각 현황]**\n\n"

    # 최신 달부터 표시 (이미 recent_months가 최신순)
    for month_key in filtered_months:
        # 월 표시 (예: 2025-12 → 2025년 12월)
        year, month = month_key.split('-')
        result += f"**[{year}년 {int(month)}월]**\n"

        # 해당 월의 사용자별 지각 횟수 정렬 (지각 많은 순)
        users = attendance_data[month_key].items()
        sorted_users = sorted(users, key=lambda x: x[1]['tardiness'], reverse=True)

        for user_id, user_data in sorted_users:
            name = user_data['name']
            tardiness = user_data['tardiness']
            result += f"• {name}님: 지각 {tardiness}번\n"

        result += "\n"  # 월 구분을 위한 빈 줄

    await interaction.response.send_message(result)

@bot.tree.command(name="도움말", description="봇 사용법을 확인합니다")
async def help_command(interaction: discord.Interaction):
    help_text = """
**기상 체크 봇 사용법**

**/기상** - 평일 오전 8시~10시 사이에 기상 체크
  • 8시~10시: 정상 처리
  • 10시 이후: 지각 처리
  • 주말에는 작동하지 않습니다

**/지각확인** - 이번 달 전체 지각 현황 확인

**/전체기록** - 최근 3개월의 지각 현황 확인 (월별로 표시)

**/내기록** - 내 이번 달 기상 기록 확인

**/도움말** - 이 도움말 표시

**🤖 자동 지각 체크**
평일 밤 11시 59분에 `/기상` 안 한 사람은 자동으로 지각 처리됩니다!
    """
    await interaction.response.send_message(help_text)

# 봇 토큰은 환경변수나 별도 파일에서 관리하세요
if __name__ == '__main__':
    # 토큰 로딩 우선순위: .env 파일 > 환경변수 > config.py
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')

    if not TOKEN:
        # .env와 환경변수에 없으면 config.py 시도
        try:
            from config import DISCORD_BOT_TOKEN
            TOKEN = DISCORD_BOT_TOKEN
            print("ℹ️  config.py에서 토큰을 로드했습니다.")
        except ImportError:
            pass

    if not TOKEN:
        print("❌ 오류: 봇 토큰이 설정되지 않았습니다!")
        print("\n다음 중 하나의 방법으로 토큰을 설정하세요:")
        print("1. .env.example을 .env로 복사하고 토큰 입력 (권장)")
        print("   cp .env.example .env")
        print("2. config_example.py를 config.py로 복사하고 토큰 입력")
        print("3. DISCORD_BOT_TOKEN 환경변수 설정")
        exit(1)

    bot.run(TOKEN)
