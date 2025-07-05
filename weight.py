import RPi_I2C_driver
import time
import sys
import RPi.GPIO as GPIO

EMULATE_HX711 = False
if EMULATE_HX711:
    from emulated_hx711 import HX711
else:
    from hx711 import HX711

######## 하드웨어에 맞게 핀 번호 수정
LED = 27
HX_DT = 20
HX_SCK = 16
# 무게추 1개 평균값 (default: 50g)
WEIGHT = 24000
# 허용 오차 (WEIGHT-MARGIN ~ WEIGHT+MARGIN)
MARGIN = 2000

######## 아래 수정 X
HIGH = True
LOW = False
comments = ["full", "congest", "congest", "normal", "pleasant", "pleasant"]

def cleanAndExit():
    if not EMULATE_HX711:
        GPIO.cleanup()
    sys.exit()

def getResult(val):
    for i in range(6):
        left = i * WEIGHT - MARGIN
        right = i * WEIGHT + MARGIN

        if left <= val < right:
            return 5-i, comments[5-i]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

lcd = RPi_I2C_driver.lcd()
lcd.lcd_display_string("available:", 1)
lcd.lcd_display_string("State:", 2)

referenceUnit = 1

hx = HX711(HX_DT, HX_SCK)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()

while True:
    try:
        val = hx.get_weight(5)
        result, cmt = getResult(val)

        if result == 5:
            GPIO.output(LED, LOW)
        else:
            GPIO.output(LED, HIGH)
            
        # LCD에 수용 가능 인원, 혼잡도 출력
        lcd.lcd_display_string_pos(str(result), 1, 11)
        lcd.lcd_display_string_pos(cmt, 2, 7)

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
