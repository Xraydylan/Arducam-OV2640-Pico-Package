# Arducam_OV2640_Python_Package_Raspberry_Pi_Pico
***
For:
- Raspberry Pi Pico
- Arducam OV2640
***
Contains:
- Raspberry Pi Pico Code
- Python Package for PC
***
## Info
This Repository contains code for the Raspberry Pi Pico to control the Arducam OV2640 and the Python Package for PC to communicate with the Pico with a USB-Serial adapter.

How to set up the Raspberry Pi Pico is described in the READ.ME in the "Pico" folder.
***
## Requirements
- pyserial
- numpy
- Pillow
***
## Functionality
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
