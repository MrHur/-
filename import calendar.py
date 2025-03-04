import calendar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import matplotlib.patches as patches

# ✅ 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 윈도우: 맑은 고딕
font_prop = fm.FontProperties(fname=font_path, size=12)
plt.rc("font", family=font_prop.get_name())

# 2025년 한국 공휴일 목록 (대체공휴일 포함)
holidays = {
    "01-01", "02-29", "03-01", "05-05", "05-06", "06-06", "08-15", "09-10", "09-11", "09-12",
    "10-03", "10-09", "12-25"
}

# 근무 패턴 설정 (3/1부터 시작하는 패턴)
work_pattern = ["야간", "야간", "휴일", "휴일", "야간", "야간", "휴일", "휴일",
                "주간", "주간", "휴일", "휴일", "주간", "주간", "휴일", "휴일"]

# 3월부터 12월까지의 근무 일정 생성
schedule = {}
day_count = 0

for month in range(3, 13):
    _, days_in_month = calendar.monthrange(2025, month)
    schedule[month] = {}
    for day in range(1, days_in_month + 1):
        pattern_index = day_count % len(work_pattern)
        schedule[month][day] = work_pattern[pattern_index]
        day_count += 1

# 달력 이미지 생성 함수
def create_calendar_sunday_start(month):
    _, days_in_month = calendar.monthrange(2025, month)
    first_weekday = calendar.monthrange(2025, month)[0]  # 0: 월요일, 6: 일요일
    first_sunday_offset = (first_weekday + 1) % 7  # 일요일 시작으로 조정

    # 달력 배열 (6주 x 7일)
    cal = np.full((6, 7), "", dtype=object)
    
    day = 1
    for i in range(6):
        for j in range(7):
            if i == 0 and j < first_sunday_offset:
                continue
            if day > days_in_month:
                break

            date_key = f"{month:02d}-{day:02d}"
            color = "black"  # 기본 색상
            bgcolor = "white"  # 기본 배경색

            if schedule[month][day] == "야간":
                bgcolor = "#D0E8FF"  # 옅은 하늘색
            elif schedule[month][day] == "주간":
                bgcolor = "#FFFACD"  # 옅은 노란색

            if j == 0 or date_key in holidays:  # 일요일 및 공휴일 빨간색
                color = "red"
            elif j == 6:  # 토요일 파란색
                color = "blue"

            text = f"{day}\n{schedule[month][day]}"  # 날짜 + 근무 형태
            cal[i, j] = (text, color, bgcolor)
            day += 1

    # 달력 그리기
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_frame_on(False)

    # 배경 색상 및 텍스트 추가
    for i in range(6):
        for j in range(7):
            if cal[i, j]:  # 날짜가 있는 경우
                text, color, bgcolor = cal[i, j]
                ax.add_patch(patches.Rectangle((j - 0.5, 5 - i - 0.5), 1, 1, color=bgcolor, alpha=0.6))
                # 요일 텍스트 색상 변경 (토요일 파란색, 일요일 빨간색)
                if j == 0:  # 일요일 빨간색
                    color = "red"
                elif j == 6:  # 토요일 파란색
                    color = "blue"
                else:  # 평일 검정색
                    color = "black"
                ax.text(j, 5 - i, text, ha="center", va="center", fontsize=12, color=color, fontproperties=font_prop)

    # 요일 레이블 추가 (일요일부터 시작)
    days_of_week = ["일", "월", "화", "수", "목", "금", "토"]
    for j, day in enumerate(days_of_week):
        if j == 0:  # 일요일 빨간색
            color = "red"
        elif j == 6:  # 토요일 파란색
            color = "blue"
        else:  # 평일 검정색
            color = "black"
            
        ax.text(j, 5.5, day, ha="center", va="center", fontsize=14, fontweight="bold", color=color, fontproperties=font_prop)

    # 달력 구분선 추가
    for i in range(6):
        for j in range(7):
            ax.plot([j - 0.5, j - 0.5], [5.5, -0.5], color="black", linewidth=1)  # 세로선
            ax.plot([-0.5, 6.5], [i - 0.5, i - 0.5], color="black", linewidth=1)  # 가로선

    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-0.5, 5.5)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.8, bottom=0.1)  # 여백 조정
    plt.title(f"2025년 {month}월 근무표 \n", fontsize=50, fontweight="bold", fontproperties=font_prop)
    plt.show()

# 3월부터 12월까지 달력 생성
for month in range(3, 13):
    create_calendar_sunday_start(month)
