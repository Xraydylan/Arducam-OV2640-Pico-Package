# Arducam OV2640 Pico Package

This is a Software package for the Rasperry Pi Pico and Arducam OV2640 to take pictures and send them via Serial to a Python script.

## Table of contents
- [Description](#Description)
- [Installation](#Installation)
- [Functionality](#Functionality)
- [Usage](#Usage)
- [License](#License)

## Description
This package is supposed to be a simple solution for taking pictures with the Arducam OV2640 connected to a Raspberry Pi Pico and sending the images to a PC with a Serial connection.

The Raspberry Pi Pico runs on MicroPython and on PC the included Arducam2640 python package can be used to control the functionality of the Arducam.

Included are:
- Raspberry Pi Pico Code
- Python Package for PC

The application can:
- Take JPEG images (different resolutions)
- Take YUV images (fixed resolution 96x96)
- Change Arducam settings

Existing code adapted from the project of the [Arducam][arducam main] main GitHub repo.
The main Pico code stems from the [PICO_SPI_CAM][arducam base] Example. 
Capability for YUV was adapted from the [PICO Arducam][arducam YUV] Example.

In the future following can be integrated:
- Proper video stream capability
- Support for other file formats
- Support for other YUV resolutions
- Wider range of changeable camera settings
- Support for Arducam OV5642

## Installation
For the setup of the Raspberry Pi Pico follow the instructions in the [REAM.me][Pico readme] in the Pico folder.

The actual Arducam2640 package can be placed into the working directory or added to path and then regularly imported.

##Functionality

### Camera Functions
- Capture images
    - JPEG
    - YUV (Fixed resolution 96x96)
- Set image types
    - JPEG
    - YUV (Fixed resolution 96x96)
- Set resolution (only JPEG)
    - 160x120
    - 176x144
    - 320x240
    - 352x288
    - 640x480
    - 800x600
    - 1024x768
    - 1280x1024
    - 1600x1200
- Set compression (only JPEG)
- Set light mode
- Set saturation
- Set brightness
- Set contrast
- Set special effect
### Other functions
- connection check
- convert byte array to JPEG
- convert byte array to YUV (YUV422, with pattern 'YUYV')
- convert YUV pixel to RGB pixel

## Usage




## License
Code released under the [MIT License](https://github.com/twbs/bootstrap/blob/main/LICENSE). Docs released under [Creative Commons](https://creativecommons.org/licenses/by/3.0/).
***
Note:This is the fist thing I actually intend to be publicly available and useful.
Constructing criticism and tips are much appreciated.

[arducam main]: https://github.com/ArduCAM
[arducam base]: https://github.com/ArduCAM/PICO_SPI_CAM
[arducam YUV]: https://github.com/ArduCAM/RPI-Pico-Cam
[Pico readme]: Pico/README.md