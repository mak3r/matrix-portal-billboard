# Matrix Portal Billboard Controller

Rationionale for implementation on the M5StickC Plus:
* I have a few of them laying around
* They have several buttons and a display for human interaction
* They have WiFi (a means to communicate with the billboard)

## Basic architecture

* `[billboard](AP) <==== wifi ==== [controller](STATION)`
* This is a close loop system where the controller and billboard are tightly coupled

    * The controller has the wifi password hardcoded
    * The controller's function is to send messages to the billboard
    * Messages sent to the billboard include `screen` information and a duration
    * The billboard displays the screen until duration has elapsed or a new screen in sent
    * If the `screen` duration expires the 'default' `screen` is displayed on the billboard

* `screens` 

    * are the set of options to display on the billboard
    * encoded in json format - see the main [README.MD](../README.md)

## Implementation

* Controller:

    * has a known set of 'screens' written to its memory
    * has wifi access
    * connects to billboard AP
    * displays the current screen
        * may display it's connection status
    * Sends a screen when the A button is pressed

* Billboard

    * Is a WiFi AP
    * Hosts 2 http request capabilities
        * GET (returns information about the billboard)
        * POST (the screen to display and for how long)

## Usage

* 