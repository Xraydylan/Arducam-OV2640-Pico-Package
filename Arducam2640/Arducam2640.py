import os
from serial import Serial
import time
import numpy as np
from PIL import Image, JpegImagePlugin
import io

# Default Serial settings
PORT = "COM4"
BAUDRATE = 921600
TIMEOUT = 1

# Image types
YUV = 0
JPEG = 1

YUV_SIZE = [96, 96]

# JPEG Compressions
Compression_Off = 0
Compression_1 = 1
Compression_2 = 2
Compression_3 = 3
Compression_4 = 4
Compression_Full = 5

# JPEG resolutions
OV2640_160x120 = 0
OV2640_176x144 = 1
OV2640_320x240 = 2
OV2640_352x288 = 3
OV2640_640x480 = 4
OV2640_800x600 = 5
OV2640_1024x768 = 6
OV2640_1280x1024 = 7
OV2640_1600x1200 = 8

# Light modes
Auto = 0
Sunny = 1
Cloudy = 2
Office = 3
Home = 4

# Saturation
# Saturation4 = 0
# Saturation3 = 1
Saturation2 = 2
Saturation1 = 3
Saturation0 = 4
Saturation_1 = 5
Saturation_2 = 6
# Saturation_3 = 7
# Saturation_4 = 8

# Brightness
# Brightness4 = 0
# Brightness3 = 1
Brightness2 = 2
Brightness1 = 3
Brightness0 = 4
Brightness_1 = 5
Brightness_2 = 6
# Brightness_3 = 7
# Brightness_4 = 8

# Contrast
# Contrast4 = 0
# Contrast3 = 1
Contrast2 = 2
Contrast1 = 3
Contrast0 = 4
Contrast_1 = 5
Contrast_2 = 6
# Contrast_3 = 7
# Contrast_4 = 8

# Special Effects
Antique = 0
Bluish = 1
Greenish = 2
Reddish = 3
BW = 4
Negative = 5
BWnegative = 6
Normal = 7


# Sepia = 8
# Overexposure = 9
# Solarize = 10
# Blueish = 11
# Yellowish = 12


# Use Arducam Class
class Arducam:
    def __init__(self, port=None, baudrate=None, timeout=None, image_type=None, conversion_size=None, save_dir=None):
        '''
        Arducam class

        :param port: Serial Port
        :param baudrate: Baudrate for serial connection
        :param timeout: Timeout for serial connection (for pyserial timeout)
        :param image_type: integer for to select type
                0: YUV
                1: JPEG
        :param conversion_size: Size for YUV resolution
        :param save_dir: Directory for saving images
        '''
        if port is None:
            port = PORT
        if baudrate is None:
            baudrate = BAUDRATE
        if timeout is None:
            timeout = TIMEOUT
        if image_type is None:
            image_type = YUV
        if conversion_size is None:
            conversion_size = YUV_SIZE
        if save_dir is None:
            save_dir = "saves/"

        self.image_type = YUV
        self.conversion_size = conversion_size
        self.save_dir = None

        self.ser = SerialCommunicator(port=port, baudrate=baudrate, timeout=timeout)

        self.change_save_dir(save_dir)
        self.check_connection()
        self.set_image_type(image_type)

    def _check_save_dir_exist(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def set_image_type(self, image_type):
        '''
        Set image type of Arducam.

        :param image_type: integer for to select type
                0: YUV
                1: JPEG
        '''

        if image_type == YUV:
            self.ser.sender(b"\x11")
        elif image_type == JPEG:
            self.ser.sender(b"\x12")
        else:
            return

        self.image_type = image_type
        time.sleep(0.5)

    def set_compression_JPEG(self, compression):
        '''
        Set compression for JPEG images.

        :param compression: integer 0-5 (0 no jpeg compression, 5 max jpeg compression)
        '''
        if self.image_type == YUV:
            print("Mode is YUV. [set_quality] not possible. Please set image_type to JPEG")
            return

        if compression == Compression_Off:
            self.ser.sender(b"\x90")
        elif compression == Compression_1:
            self.ser.sender(b"\x91")
        elif compression == Compression_2:
            self.ser.sender(b"\x92")
        elif compression == Compression_3:
            self.ser.sender(b"\x93")
        elif compression == Compression_3:
            self.ser.sender(b"\x94")
        elif compression == Compression_Full:
            self.ser.sender(b"\x95")

    def set_resolution_JPEG(self, resolution):
        '''
        Set compression for JPEG images.

        :param resolution: integer 0-8
        '''
        if self.image_type == YUV:
            print("Mode is YUV. [set_quality] not possible. Please set image_type to JPEG")
            return

        if resolution == OV2640_160x120:
            self.ser.sender(b"\x00")
        elif resolution == OV2640_176x144:
            self.ser.sender(b"\x01")
        elif resolution == OV2640_320x240:
            self.ser.sender(b"\x02")
        elif resolution == OV2640_352x288:
            self.ser.sender(b"\x03")
        elif resolution == OV2640_640x480:
            self.ser.sender(b"\x04")
        elif resolution == OV2640_800x600:
            self.ser.sender(b"\x05")
        elif resolution == OV2640_1024x768:
            self.ser.sender(b"\x06")
        elif resolution == OV2640_1280x1024:
            self.ser.sender(b"\x07")
        elif resolution == OV2640_1600x1200:
            self.ser.sender(b"\x08")

    def set_light_mode(self, light_mode):
        '''
        Set saturation.

        :param light_mode: integer 0-4
        '''

        if light_mode == Auto:
            self.ser.sender(b"\x40")
        elif light_mode == Sunny:
            self.ser.sender(b"\x41")
        elif light_mode == Cloudy:
            self.ser.sender(b"\x42")
        elif light_mode == Office:
            self.ser.sender(b"\x43")
        elif light_mode == Home:
            self.ser.sender(b"\x44")

    def set_saturation(self, saturation):
        '''
        Set light mode.

        :param saturation: integer 2-6
        '''

        if saturation == Saturation2:
            self.ser.sender(b"\x50")
        elif saturation == Saturation1:
            self.ser.sender(b"\x51")
        elif saturation == Saturation0:
            self.ser.sender(b"\x52")
        elif saturation == Saturation_1:
            self.ser.sender(b"\x53")
        elif saturation == Saturation_2:
            self.ser.sender(b"\x54")

    def set_brightness(self, brightness):
        '''
        Set brightness.

        :param brightness: integer 2-6
        '''

        if brightness == Brightness2:
            self.ser.sender(b"\x60")
        elif brightness == Brightness1:
            self.ser.sender(b"\x61")
        elif brightness == Brightness0:
            self.ser.sender(b"\x62")
        elif brightness == Brightness_1:
            self.ser.sender(b"\x63")
        elif brightness == Brightness_2:
            self.ser.sender(b"\x64")

    def set_contrast(self, contrast):
        '''
        Set brightness.

        :param contrast: integer 2-6
        '''

        if contrast == Contrast2:
            self.ser.sender(b"\x70")
        elif contrast == Contrast1:
            self.ser.sender(b"\x71")
        elif contrast == Contrast0:
            self.ser.sender(b"\x72")
        elif contrast == Contrast_1:
            self.ser.sender(b"\x73")
        elif contrast == Contrast_2:
            self.ser.sender(b"\x74")

    def set_special_effect(self, effect):
        '''
        Set brightness.

        :param effect: integer 0-7
        '''

        if effect == Antique:
            self.ser.sender(b"\x80")
        elif effect == Bluish:
            self.ser.sender(b"\x81")
        elif effect == Greenish:
            self.ser.sender(b"\x82")
        elif effect == Reddish:
            self.ser.sender(b"\x83")
        elif effect == BW:
            self.ser.sender(b"\x84")
        elif effect == Negative:
            self.ser.sender(b"\x85")
        elif effect == BWnegative:
            self.ser.sender(b"\x86")
        elif effect == Normal:
            self.ser.sender(b"\x87")

    def capture_frame(self, raw=False, resize_YUV=True, YUV_to_RGB=False, save_name=None):
        '''
        Takes an image with Arducam according to settings.

        :param raw: if set returns the raw bytearray
        :param resize_YUV: resize YUV according to conversion_size
        :param YUV_to_RGB: if set returns image RGB image from YUV
        :param save_name: if save name is a string then the return value of capture_frame will be saved.
                    the defaults are:
                        .txt for byte array
                        .npy for numpy arrays
                        .jpeg for images
        :return:    for a JPEG returns image object
                    for a YUV returns array of pixels (resized to conversion_size if resize_YUV set True)
                        or an RGB image object if YUV_to_RGB set True
                    for raw returns bytearray
        '''
        self.ser.sender(b"\x10")
        byte_array = self.ser.get_data()
        if raw:
            if save_name is not None:
                self.save(byte_array, save_name)
            return byte_array
        image = self.convert_to_image(byte_array, resize_YUV=resize_YUV, YUV_to_RGB=YUV_to_RGB)
        if save_name is not None:
            self.save(image, save_name)
        return image

    def convert_to_image(self, byte_array, image_type=None, resize_YUV=True, YUV_to_RGB=False):
        '''
        Converts bytearray to image.

        :param byte_array: bytearray of image
        :param image_type: image_type the bytearray is converted to. If None the previously set type is used.
        :param resize_YUV: resize YUV according to conversion_size
        :param YUV_to_RGB: if set returns image RGB image from YUV
        :return:    for a JPEG returns image object
                    for a YUV returns array of pixels (resized to conversion_size if resize_YUV set True)
                        or an RGB image object if YUV_to_RGB set True
        '''
        if image_type is None:
            image_type = self.image_type

        img = None
        if image_type == YUV:
            img = self.convert_to_YUV(byte_array, resize=resize_YUV, YUV_to_RGB=YUV_to_RGB)
        elif image_type == JPEG:
            img = self.convert_to_JPEG(byte_array)
        return img

    def convert_to_JPEG(self, byte_array):
        '''
        Converts byte_array to JPEG image.

        :param byte_array: bytearray of the image
        :return: Image object
        '''
        return Image.open(io.BytesIO(byte_array))

    def convert_to_YUV(self, byte_array, resize=True, YUV_to_RGB=False):
        '''
        Converts byte_array to YUV pixel array according to conversion_size if resize.

        The format is YUV422 with the order 'YUYV'

        :param byte_array: bytearray of the image
        :param resize: determine if pixel array needs to be resized
        :param YUV_to_RGB: if set returns image RGB image from YUV
        :return: for a YUV returns array of pixels (resized to conversion_size if resize set True)
                        or an RGB image object if YUV_to_RGB set True
        '''

        Y = []
        U = []
        V = []
        for index, byte in enumerate(byte_array):
            val = byte_to_int(byte)
            if index % 4 == 1:
                U += [val] * 2
            elif index % 4 in [0, 2]:
                Y.append(val)
            elif index % 4 == 3:
                V += [val] * 2

        YUV_simple = [Y, U, V]
        YUV_pix = np.array(list(zip(*YUV_simple)))

        if YUV_to_RGB:
            YUV_pix = np.array([self.YUV_pix_to_RGB_pix(pix) for pix in YUV_pix])
            YUV_pix = np.resize(YUV_pix, list(self.conversion_size) + [3])
            return Image.fromarray(np.uint8(YUV_pix)).convert("RGB")
        if resize:
            return np.resize(YUV_pix, list(self.conversion_size) + [3])
        return YUV_pix

    def YUV_pix_to_RGB_pix(self, pix):
        '''
        Converts YUV pixel into RGB pixel

        :param pix: pixel with YUV values
        :return: pixel with RGB values
        '''
        Y, U, V = pix
        R = limit_value(Y + 1.370705 * (V - 128))
        G = limit_value(Y - 0.698001 * (V - 128) - 0.337633 * (U - 128))
        B = limit_value(Y + 1.732446 * (U - 128))
        return np.array([R, G, B])

    def check_connection(self):
        '''
        Checks if Pico is operational if not an Exception is raised
        '''
        if not self.ser.test_connection():
            raise Exception("No Pico Connected or Pico not working")
        print("Connection Established")

    def change_save_dir(self, directory):
        '''
        Changes name of save dictionary

        :param directory: name of dictionary
        '''
        if directory[-1] != "/":
            directory += "/"
        self.save_dir = directory

    def save(self, data, name):
        '''
        Saves data according to type

        :param data: data
        :param name: name of file. Extension may be modified.
        :return:
        '''
        self._check_save_dir_exist()
        pil_image_types = [Image.Image, JpegImagePlugin.JpegImageFile]

        if type(data) == np.narray:
            if len(elem := name.split(".")) != 1:
                name = ".".join(elem[:-1])
            path = self.save_dir + name
            np.save(path, data)

        elif type(data) in pil_image_types:
            if len(name.split(".")) == 1:
                name += ".jpg"
            path = self.save_dir + name
            data.save(path)

        elif type(data) == bytes:
            if len(name.split(".")) == 1:
                name += ".txt"
            path = self.save_dir + name
            with open(path, "wb") as f:
                f.write(data)




    def load(self, name, in_save_dir=True):
        '''
        Loads data according to file extension

        :param name: name of file
        :param in_save_dir: flag if file is located in the save_dir (automatically adds path to save_dir)
        :return: loaded data according to file extension
        '''

        path = name
        if in_save_dir:
            path = self.save_dir + name

        split = name.split(".")
        if len(split) == 1:
            extension = ".npy"
            path += ".npy"
            split.append(extension)

        if split[-1] == ".npy":
            return np.load(path)

        if split[-1] == ".txt":
            with open(path, "rb") as f:
                return f.read()

        return Image.open(path)


class SerialCommunicator:
    def __init__(self, port=None, baudrate=None, timeout=None):
        if port is None:
            port = PORT
        if baudrate is None:
            baudrate = BAUDRATE
        if timeout is None:
            timeout = TIMEOUT

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self.connection_test_loops = 2
        self.confirmation_byte = b'\x00'

        self.ser = None

        self.init_serial()

    def init_serial(self):
        self.ser = Serial(self.port, self.baudrate, timeout=self.timeout)

    def sender(self, data, wait=True):
        self.ser.write(data)
        if wait:
            time.sleep(0.2)

    def get_data(self):
        array = b''
        image_flag = 0
        while 1:
            data = self.ser.readline()
            if data == b"":
                continue

            if data == b"STOP\n":
                print("Image Received")
                array = array[:-1]
                return array

            if image_flag == 1:
                array += data

            if data == b"START\n":
                print("Start Flag")
                image_flag = 1

    def test_connection(self):
        self.sender(b'\xA0')
        for i in range(self.connection_test_loops):
            byte = self.ser.read()
            if not byte:
                continue
            if byte == self.confirmation_byte:
                return True
        return False


def byte_to_int(byte):
    if type(byte) == int:
        return byte
    return int.from_bytes(byte, byteorder='big')


def limit_value(value):
    if value > 255:
        return 255
    if value < 0:
        return 0
    return value
