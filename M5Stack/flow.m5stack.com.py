from m5stack import *
from m5ui import *
from uiflow import *
import time
lcd.setRotation(2)

setScreenColor(0x111111)


duration = None
sec_per_min = None
json_content = None
next_message = None
brightness = None
bg_R = None
bg_G = None
bg_B = None
cur_message = None
text_R = None
text_G = None
text_B = None
default_message = None



message = M5TextBox(82, 65, "content", lcd.FONT_DejaVu24, 0xffd700, rotate=90)
circle0 = M5Circle(25, 24, 12, 0xFFFFFF, 0xFFFFFF)


# Describe this function...
def init():
  global duration, sec_per_min, json_content, next_message, brightness, bg_R, bg_G, bg_B, cur_message, text_R, text_G, text_B, default_message
  json_content = {'msg':'from json'}
  sec_per_min = 60
  duration = 0
  bg_R = 108
  bg_G = 11
  bg_B = 169
  text_R = 255
  text_G = 215
  text_B = 0
  default_message = 'Hello M5'
  brightness = 100
  axp.setLcdBrightness(brightness)

# Describe this function...
def flash_led():
  global duration, sec_per_min, json_content, next_message, brightness, bg_R, bg_G, bg_B, cur_message, text_R, text_G, text_B, default_message
  for count in range(10):
    M5Led.on()
    wait_ms(100)
    M5Led.off()
    wait_ms(200)


def buttonA_wasPressed():
  global duration, sec_per_min, json_content, next_message, brightness, bg_R, bg_G, bg_B, cur_message, text_R, text_G, text_B, default_message
  axp.setLcdBrightness(100)
  next_message = json_content['msg']
  message.setText(str(next_message))
  flash_led()
  axp.setLcdBrightness(brightness)
  pass
btnA.wasPressed(buttonA_wasPressed)

def buttonA_wasDoublePress():
  global duration, sec_per_min, json_content, next_message, brightness, bg_R, bg_G, bg_B, cur_message, text_R, text_G, text_B, default_message
  if brightness == 0:
    brightness = 100
  else:
    brightness = 0
  axp.setLcdBrightness(brightness)
  pass
btnA.wasDoublePress(buttonA_wasDoublePress)

def buttonB_wasPressed():
  global duration, sec_per_min, json_content, next_message, brightness, bg_R, bg_G, bg_B, cur_message, text_R, text_G, text_B, default_message
  duration = 15 * sec_per_min
  lcd.circle(110, 30, 10, color=0x33ff33)
  lcd.arc(25, 24, 15, 4, 0, 90, color=0xcc0000)
  cur_message = default_message
  message.setText(str(cur_message))
  pass
btnB.wasPressed(buttonB_wasPressed)


init()
setScreenColor((bg_R << 16) | (bg_G << 8) | bg_B)
message.setColor((text_R << 16) | (text_G << 8) | text_B)
message.setText(str(next_message))
while True:
  wait(3)
  if next_message != cur_message:
    cur_message = next_message
    setScreenColor((bg_R << 16) | (bg_G << 8) | bg_B)
    message.setColor((text_R << 16) | (text_G << 8) | text_B)
    message.setText(str(cur_message))
  wait_ms(2)
