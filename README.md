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

## Quick Start
1. [Prepare the MatrixPortal](https://learn.adafruit.com/matrix-portal-new-guide-scroller/prep-the-matrixportal)
1. [Install CircuitPython](https://learn.adafruit.com/matrix-portal-new-guide-scroller/install-circuitpython)
1. **(Optional)** Create a `secrets.py` file with your WiFi SSID and passphrase
1. Copy all files from this repo into the `CIRCUITPY` directory that was mounted when you installed CircuitPython
1. Power up
1. Click up/down buttons to switch content

## Content Layout
The `content.json` file contains a list of content which can be cycled through on the Matrix Portal. Content could be text or bitmap images. Or a combination of both. Text can be scrolled orizontally and colors can be set for the foreground and background. The content file must be json formatted.

### There are 4 content types:

1. `text` can be a simple word or phrase which is shown statically on the display. `text` has 2 attributes `fg_color` and `bg`
2. `img` is a bitmap image 

```
{
  "img": "images/snoopy.bmp",
  "http": "https://raw.githubusercontent.com/mak3r/MatrixPortalBilboardContent/main/hello.json",
  "file": "hello.txt"
}
```