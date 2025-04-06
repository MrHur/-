import calendar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import matplotlib.patches as patches

# ✅ 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"
font_prop = fm.FontProperties(fname=font_path, size=12)
plt.rc("font", family=font_prop.get_name())

# 2025년 한국 공휴일 (대체공휴일 포함)
holidays = {
    "01-01": "신정", "03-01": "삼일절", "05-05": "어린이날", "05-06": "대체공휴일",
    "06-06": "현충일", "08-15": "광복절", "09-10": "추석", "09-11": "추석", "09-12": "추석",
    "10-03": "개천절", "10-09": "한글날", "12-25": "크리스마스"
}

# 패턴: (주간 2일, 휴일 2일) * 4 + (야간 2일, 휴일 2일) * 4
base_work_pattern = (
    ["주간"] * 2 + ["휴일"] * 2
) * 4 + (
    ["야간"] * 2 + ["휴일"] * 2
) * 4  # 총 32일 주기

# 근무 시작 기준일
base_year = 2025
base_start_month = 4
base_start_day = 10

# 기준일로부터 경과일 계산 함수
def days_since_base(month, day):
    from datetime import date
    base = date(base_year, base_start_month, base_start_day)
    current = date(base_year, month, day)
    return (current - base).days

# 월별 근무표 생성
schedule = {}
for month in range(4, 13):  # 4월~12월
    _, days_in_month = calendar.monthrange(2025, month)
    schedule[month] = {}
    for day in range(1, days_in_month + 1):
        offset = days_since_base(month, day)
        if offset < 0:
            schedule[month][day] = "휴일"  # 기준일 이전은 전부 휴일
        else:
            index = offset % len(base_work_pattern)
            schedule[month][day] = base_work_pattern[index]

# 달력 생성 함수
def create_calendar_sunday_start(month):
    _, days_in_month = calendar.monthrange(base_year, month)
    first_weekday = calendar.monthrange(base_year, month)[0]
    first_sunday_offset = (first_weekday + 1) % 7

    cal = np.full((6, 7), "", dtype=object)
    day = 1
    for i in range(6):
        for j in range(7):
            if i == 0 and j < first_sunday_offset:
                continue
            if day > days_in_month:
                break

            date_key = f"{month:02d}-{day:02d}"
            color = "black"
            bgcolor = "white"

            work_type = schedule[month][day]
            if work_type == "야간":
                bgcolor = "#aea1f0"
            elif work_type == "주간":
                bgcolor = "#f0d0a1"

            if date_key in holidays:
                color = "red"
            elif j == 0:
                color = "red"
            elif j == 6:
                color = "blue"

            text = f"{day}\n{schedule[month][day]}"
            if date_key in holidays:
                text += f"\n{holidays[date_key]}"

            cal[i, j] = (text, color, bgcolor)
            day += 1

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    for i in range(6):
        for j in range(7):
            if cal[i, j]:
                text, color, bgcolor = cal[i, j]
                ax.add_patch(patches.Rectangle((j - 0.5, 5 - i - 0.5), 1, 1, color=bgcolor, alpha=0.6))
                ax.text(j, 5 - i, text, ha="center", va="center", fontsize=12, color=color, fontproperties=font_prop)

    days_of_week = ["일", "월", "화", "수", "목", "금", "토"]
    for j, day in enumerate(days_of_week):
        color = "red" if j == 0 else "blue" if j == 6 else "black"
        ax.text(j, 5.5, day, ha="center", va="center", fontsize=14, fontweight="bold", color=color, fontproperties=font_prop)

    for i in range(6):
        for j in range(7):
            ax.plot([j - 0.5, j - 0.5], [5.5, -0.5], color="black", linewidth=1)
            ax.plot([-0.5, 6.5], [i - 0.5, i - 0.5], color="black", linewidth=1)

    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-0.5, 5.5)
    plt.subplots_adjust(left=0, right=1, top=0.85, bottom=0)
    plt.title(f"2025년 {month}월 근무표 \n", fontsize=20, fontweight="bold", fontproperties=font_prop)
    plt.show()

# 4월~12월 달력 출력
for month in range(4, 13):
    create_calendar_sunday_start(month)
