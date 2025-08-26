import RPi.GPIO as GPIO
import threading
import time
import tkinter as tk
from detection import camera

# ========================== USER SETTINGS ===========================

# 엘리베이터 내부 버튼 - 1 2 3 4
# 엘리베이터 외부 버튼 - 1↑ 2↑ 3↑ 2↓ 3↓ 4↓
# 순서대로 아래 배열 수정, 총 10개

buttons = [13, 26, 21, 19, 25, 24, 23, 16, 12, 18]

# ========================== DON'T EDIT ==============================
# ========================== global variables ==========================

det1, det2, det3, det4 = 0, 0, 0, 0

# ========================== basic settings ==========================

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in buttons:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

root = tk.Tk()
root.title("elevator")
root.geometry("500x600")

# ========================== labels ==========================

# l_square: 엘리베이터 위치 시각화 □ ■
l_square_text = '□' + '\n' + '□' + '\n' + '□' + '\n' + '■'
l_square = tk.Label(root, text=l_square_text, font=('Consolas', 50, 'bold'))
l_square.pack(padx=10, pady=10)

# l_curr: 현재 층 표시 (current floor: 1)
l_curr_text = (f'current floor: {floor}')
l_curr = tk.Label(root, text=l_curr_text, font=('Consolas', 30, 'bold'))
l_curr.pack(padx=10, pady=10)

# l_stat: 도착/문 열림/문 닫힘 출력 (arrived, open, closed)
l_stat_text = ('')
l_stat = tk.Label(root, text=l_stat_text, font=('Consolas', 30, 'bold'))
l_stat.pack(padx=10, pady=10)

# ========================== variables ==========================

# 현재 엘리베이터 동작 중 / 대기 중
MOVING = 1
IDLE = 2

mode = IDLE

# 다음 루프에서 이동해야 하는지
should_move = False

# 현재 엘리베이터가 머무르고 있는 층
floor = 1

# 각 층에서, 위로/아래로 가는 버튼이 눌려 있는지 (bool)
up = [0, 0, 0]  # 1, 2, 3
down = [0, 0, 0]  # 4, 3, 2

# 목적지 층수
dest = 1

# ========================== functions ==========================

# 사람 수 측정
def detect_people():
    global mode, det1, det2, det3, det4, up, down
    
    dets = [det1, det2, det3, det4]

    while True:
        for i in range(4):
            dets[i] = camera(i)
        
# 사람이 없으면 요청 제거 및 정지
def no_person():
    global det1, det2, det3, det4, mode, up, down, dest
    
    while True:            
        if det1 == 0:
            up[1] = 0
            if dest == 1:
                mode = IDLE

        if det2 == 0:
            up[1] = 0
            down[2] = 0
            if dest == 2:
                mode = IDLE

        if det3 == 0:
            up[2] = 0
            down[1] = 0
            if dest == 3:
                mode = IDLE

        if det4 == 0:
            down[0] = 0
            if dest == 4:
                mode = IDLE

# 현재 층수 시각화 라벨 업데이트
def update_display():
    display = ['□'] * 4
    display[4 - floor] = '■'
    l_square.config(text='\n'.join(display))

# 현재 상태 업데이트 (open/closed/arrived)
def set_status(text):
    l_stat.config(text=text)
    
# 현재 층수 출력
def print_curr():
    l_curr.config(text="current floor: {}".format(floor))

# 엘리베이터 문 열고 닫기 (딜레이 1초)
def open_close():
    set_status('open')
    time.sleep(1)
    set_status('closed')
    time.sleep(1)    

# 엘리베이터 내부 요청으로 목적지 갱신
def go_to_floor(floor_number):
    global mode, dest, should_move
    should_move = True
    
    dest = floor_number
    mode = MOVING

def one(): go_to_floor(1)
def two(): go_to_floor(2)
def three(): go_to_floor(3)
def four(): go_to_floor(4)

# 엘리베이터 외부 idx층에서 올라가는 버튼 누름
def go_up(idx):
    global should_move, mode, dest
    should_move = True
    
    # 엘리베이터가 이동 중이면 지금 바로 가지 않고 요청 등록해두기
    if mode == MOVING:
        up[idx] = 1
    # 엘리베이터가 대기 중이면 당장 목적지 설정
    elif mode == IDLE:
        dest = idx + 1
    
    mode = MOVING

def one_up(): go_up(0)
def two_up(): go_up(1)
def three_up(): go_up(2)

# 엘리베이터 외부 idx층에서 내려가는 버튼 누름
def go_down(idx):
    global should_move, mode, dest
    should_move = True
    
    if mode == MOVING:
        down[idx] = 1
    elif mode == IDLE:
        dest = 4 - idx
    mode = MOVING

def four_down(): go_down(0)
def three_down(): go_down(1)
def two_down(): go_down(2)

# ========================== while loop ==========================

def while_loop():
    global floor, dest, should_move, mode, l_square

    while True:
        # 움직여야 하고, 현재 엘리베이터 움직이는 중
        if should_move == True and mode == MOVING:
            
            # 엘리베이터 올라가야 함
            if floor < dest:
                # 1초 간격으로 한 층씩 올라감
                while floor <= dest:
                    time.sleep(1)
                    floor += 1
                    set_status('')
                    print_curr()
                    update_display()

                    # 도착: 이동 종료, 엘리베이터 대기로 전환
                    if floor == dest:
                        set_status('arrived.')
                        should_move = False
                        mode = IDLE
                        break
                    
                    # 중간에 멈춰야 하는 경우 (외부에서 올라가는 거 누름)
                    if floor <= 3 and up[floor - 1]:
                        open_close()
                        up[floor - 1] = 0

            # 엘리베이터 내려가야 함
            elif floor > dest:
                # 1초 간격으로 한 층씩 내려감
                while floor >= dest:
                    time.sleep(1)
                    set_status('')
                    floor -= 1
                    print_curr()
                    update_display()

                    # 중간에 멈춰야 하는 경우 (외부에서 내려가는 거 누름)
                    if 2 <= floor <= 4 and down[4 - floor]:
                        open_close()
                        down[4 - floor] = 0

                    # 도착: 이동 종료, 엘리베이터 대기로 전환
                    if floor == dest:
                        set_status('arrived.')
                        should_move = False
                        mode = IDLE
                        break
        
        # 엘리베이터 대기 중: 
        if mode == IDLE:
            
            # 올라가라는 요청이 있는가
            for i in range(3):
                if up[i] == 1:
                    up[i] = 0
                    dest = i + 1
                    
                    mode = MOVING
                    should_move = True
                    break
                
            # 내려가라는 요청이 있는가
            for i in range(3):
                if down[i] == 1:
                    down[i] = 0
                    dest = 4 - i
                    
                    mode = MOVING
                    should_move = True
                    break

# ========================== main (thread) ==========================

def main():
    while_thread = threading.Thread(target=while_loop)
    detect_thread = threading.Thread(target=detect_people)
    no_person_thread = threading.Thread(target=no_person)
    
    while_thread.start()
    detect_thread.start()
    no_person_thread.start()

    # 버튼 감지 콜백 등록
    callbacks = [one, two, three, four, one_up, two_up, three_up, two_down, three_down, four_down]
    for _ in range(10):
        GPIO.add_event_detect(buttons[_], GPIO.RISING, callback=callbacks[_], bouncetime=300)

if __name__ == "__main__":
    main()

root.mainloop()
