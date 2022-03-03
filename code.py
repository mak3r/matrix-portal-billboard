
import time
import board
import busio
import json
import displayio
import terminalio
import digitalio
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_requests as requests
from adafruit_matrixportal.matrixportal import MatrixPortal
from adafruit_matrixportal.network import Network


try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

displayio.release_displays()

# --- Display setup ---
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=False, bit_depth=5)
#network = matrixportal.network
#network.connect()

# Initialize a requests object with a socket and esp32spi interface
#socket.set_interface(network._wifi.esp)
#requests.set_socket(socket, network._wifi.esp)

class Billboard:

    content = ""
    item = "NO ITEMS"
    keys_index = 0
    keys = []
    display_types = ["img", "url", "text", "stext"]
    scroll_rate = .1
    SCROLLING = False
    text_index = None
    stext_index = None

    def __init__(self, filename):
        matrixportal.display.auto_refresh = True
        with open(filename, 'r') as c:
            self.content = json.load(c)
        
        for k in self.content.keys():
            self.keys.append(k)

        print("Content for display: ", self.content)

        self.text_index = matrixportal.add_text(
            text_font=terminalio.FONT, #"fonts/Arial-12.bdf", #
            text_position=((matrixportal.graphics.display.width // 2), (matrixportal.graphics.display.height // 2) - 1),
            scrolling=False,
            text_anchor_point=(.5,.5) # This centers the text (approximately)
        )

        self.stext_index = matrixportal.add_text(
            text_font="fonts/IBMPlexMono-Medium-24_jep.bdf", 
            text_position=((matrixportal.graphics.display.width // 2), (matrixportal.graphics.display.height // 2) - 1),
            scrolling=True,
        )
        #Show the first item
        self.next()


    def next(self):
        if len(self.keys) > 0:
            if self.keys_index < len(self.keys) - 1:
                self.keys_index += 1
            else:
                self.keys_index = 0
        self.item = self.content[self.keys[self.keys_index]]
        self.__display__(self.keys[self.keys_index], self.item)

    def prev(self):
        if len(self.keys) > 0:
            if self.keys_index == 0:
                self.keys_index = len(self.keys) - 1
            else:
                self.keys_index -= 1
        self.item = self.content[self.keys[self.keys_index]]
        self.__display__(self.keys[self.keys_index], self.item)
        
    def __display__(self, key, item):
        print("key {}, item: {}".format(key,item))
        self.SCROLLING = False
        # Clear the display
        self.clear()
        for k in item.keys():
            if k in self.display_types:
                if k == "text":
                    self.load_text(
                        item[k], 
                        text_color=item['fg_color'], 
                        bg=self.parse_bg(item['bg'])
                    )
                if k == "stext":
                    self.scroll_rate = float(item['rate'] if "rate" in item.keys() else .1)
                    self.load_stext(
                        item[k], 
                        text_color=item['fg_color'], 
                        bg=self.parse_bg(item['bg'])
                    )
                    self.SCROLLING = True
                elif k == "img":
                    self.load_image(item[k])
                elif k == "url":
                    self.load_from_url(item[k])

    def parse_bg(self, bg):
        if bg.startswith("0x"):
            return int(bg,16)
        elif bg[-4:] == ".bmp":
            return bg
        else:
            return matrixportal.default_bg

    def clear(self):
        self.load_text("", text_color="0x000000", bg=0)
        self.load_stext("", text_color="0x000000", bg=0)


    def load_image(self, bmp):
        matrixportal.set_background(bmp)

    def load_from_url(self, url):        
        # Define a custom header as a dict.
        headers = {
            "user-agent": "matrix-portal/1.0.0", 
        }

        try:
            response = requests.get(url, headers=headers)
        except:
            print("Unable to get url {}".format(url))
            return False

        data = response.text
        url_content = json.loads(data)
        if "url" in url_content.keys():
            raise ValueError("url type cannot reference another url - to avoid infinite recursion issues")
        item = url_content.popitem()
        self.__display__(item[0], item[1])
        response.close()
        return True


    def load_text(self, msg, *, text_color="0x000000", bg="0x10BA08"):
        matrixportal.set_background(bg)
        matrixportal.set_text(msg, self.text_index)
        matrixportal.set_text_color(int(text_color,16), 0)

    def load_stext(self, msg, *, text_color="0x000000", bg="0x10BA08"):
        matrixportal.set_background(bg)
        matrixportal.set_text(msg, self.stext_index)
        matrixportal.set_text_color(int(text_color,16), 1)

# Setup the billboard
billboard = Billboard('content.json')

# Matrix Portal Button Responders
up_btn = digitalio.DigitalInOut(board.BUTTON_UP)
up_btn.direction = digitalio.Direction.INPUT
up_btn.pull = digitalio.Pull.UP

down_btn = digitalio.DigitalInOut(board.BUTTON_DOWN)
down_btn.direction = digitalio.Direction.INPUT
down_btn.pull = digitalio.Pull.UP

debounce_timeout =  .2
cur_debounce = time.monotonic() + debounce_timeout
def display_change():
    global cur_debounce
    global up_btn
    global down_btn
    global billboard
    global debounce_timeout
    if time.monotonic() > cur_debounce:
        if not up_btn.value:
            billboard.next()

        if not down_btn.value:
            billboard.prev()

        # reset debounce clock
        cur_debounce = time.monotonic() + debounce_timeout

do_scroll = time.monotonic() + billboard.scroll_rate
while True:
    display_change()
    if billboard.SCROLLING == True:
        if time.monotonic() > do_scroll:
            matrixportal.scroll()
            do_scroll = time.monotonic() + billboard.scroll_rate
