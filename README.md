# The SUSE Billbard for Matrix Portal
This is a simple application which will display a choice of text or images on the Adafruit Matrix Portal 32x64 display

## Code

* lib - libraries and resources needed to run the bilboard app
    - These can and should be updated to the latest versions 
    - Libraries included here are used to simplify the time to get up and running 
* `code.py` - the application code which parses and displays the content
* `content.json` 
    - The content which will get displayed on the matrix portal.
    - See the section (Content Layout)[#Content Layout] below for details

## Content Layout
The content.txt file should contain a list of content which can be cycled through on the Matrix Portal. Content could be text or bitmap images. The content file should be json formatted for easy parsing.

```
{
  "img": "images/snoopy.bmp",
  "http": "https://raw.githubusercontent.com/mak3r/MatrixPortalBilboardContent/main/hello.json",
  "file": "hello.txt"
}
```