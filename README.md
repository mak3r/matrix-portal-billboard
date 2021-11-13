# The SUSE Billboard for Matrix Portal
This is a simple application which will display a choice of text or images on the Adafruit Matrix Portal 32x64 display

## Code

* lib - libraries and resources needed to run the bilboard app
    - These can and should be updated to the latest versions 
    - Libraries included here are used to simplify the time to get up and running 
    - [Get the latest libraries](https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries)
* `code.py` - the application code which parses and displays the content
* `content.json` 
    - The content which will get displayed on the matrix portal.
    - See the section [Content Layout](#Content Layout) below for details
* `secrets.py` - contains secrets like a wifi SSID and passphrase

## Quick Start
1. [Prepare the MatrixPortal](https://learn.adafruit.com/matrix-portal-new-guide-scroller/prep-the-matrixportal)
1. [Install CircuitPython](https://learn.adafruit.com/matrix-portal-new-guide-scroller/install-circuitpython)
1. **(Optional)** Create a `secrets.py` file with your WiFi SSID and passphrase
1. Copy all files from this repo into the `CIRCUITPY` directory that was mounted when you installed CircuitPython
1. Power up
1. Click up/down buttons to switch content

## Content Layout
The `content.json` file contains a list of content which can be cycled through on the Matrix Portal. Content could be text or bitmap images. Or a combination of both. Text can be scrolled orizontally and colors can be set for the foreground and background. The content file must be json formatted.

**NOTE:** Each entry in the `content.json` file must have a unique key. The values of the entry are specfied as one fo the 4 content types. This allows for each content type to be repeated in the file in any order. Python reads dictionaries in without regard to order so sequencing according the the file layout is not possible without further development

### There are 4 content types:

1. `text` can be a simple word or phrase which is shown statically on the display. `text` has 2 attributes `fg_color` and `bg`. This type can be read from the `content.json` file or from a `url` content type

1. `stext` or scrolling text can be a simple word or phrase which will be scrolled from right to left across the display. `stext` has 3 attributes `fg_color`, `bg` and `rate`. This type can be read from the `content.json` file or from a `url` content type.

1. `img` is the path to a bitmap image on disk. It is recommended that `img` bitmaps are formatted to the exact size of the display (default 64x32 - WxH). This type can be read from the `content.json` file or from a `url` content type.

1. `url` is a special content type only read from the content.json file which allows for any 1 individual content type to be read from a URL. The `url` content must be properly formatted and it cannot itself be a `url` content type. The `url` type requires that WiFi is connected which can be done using the `secrets.py` file.


### Attributes:
1. `fg_color` is the foreground color of the text specified as a hex string in RGB - for example 0xFFFFFF is white.
1. `bg` can be either a hex string specified in RGB or a path to a file on disk. 
1. `rate` is the speed at which scrolling text moves from right to left across the screen. Reasonable values appear to be between .04 (fast) and .2 (slow). Any floating point value may be used however the code does not check for 'reasonable' values. 

### Example `content.json`
```
{
	"geeko": {"img": "images/geeko.bmp"},
	"hello-url": {"url": "https://raw.githubusercontent.com/mak3r/MatrixPortalBilboardContent/main/hello.json"},
	"text1": {
		"text" : "howdy",
		"bg": "0x800020",
		"fg_color": "0x777777"
	},
	"rancher": {"img": "images/rancher.bmp"},
	"scroll-url": {"url": "https://raw.githubusercontent.com/mak3r/MatrixPortalBillboardContent/main/scroll.json"},
	"scroll-text": {
		"stext" : "scroll this by me",
		"bg": "0x800020",
		"fg_color": "0xAAAAAA",
		"rate" : ".2"	
	},
	"wrap-example": {
		"text" : "wrap text\nexample",
		"fg_color" : "0x982200",
		"bg" : "0x000000"
	},
	"file-bg-example": {
		"text" : "GEEKO",
		"fg_color" : "0xFFFFFF",
		"bg" : "images/geeko.bmp"
	},
	"in-meeting": {
		"text": "IN A\nMEETING",
		"fg_color" : "0xFF11BB",
		"bg" : "0x000000"
	}

}

```