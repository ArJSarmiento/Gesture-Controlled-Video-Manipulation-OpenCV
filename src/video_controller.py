"""
    VideoController class which is used to apply different image processing techniques to a video feed.
"""
import cv2
import numpy as np


class VideoController:
    def changeBrightness(self, img, value=0) -> cv2.typing.MatLike:
        """This function will take an image (img) and the brightness
        value. It will perform the brightness change using OpenCv
        and after split, will merge the img and return it.
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img

    def changeBlur(self, img, value=0) -> cv2.typing.MatLike:
        """This function will take the img image and blur values as inputs.
        After perform blur operation using opencv function, it returns
        the image img.
        """
        kernel_size = (value + 1, value + 1)  # +1 is to avoid 0
        img = cv2.blur(img, kernel_size)
        return img

    def adjust_saturation(self, image, saturation_scale=1.0) -> cv2.typing.MatLike:
        """Adjust the saturation of an image."""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        s = cv2.multiply(s, saturation_scale)
        final_hsv = cv2.merge((h, s, v))
        image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return image

    def adjust_contrast(self, image, alpha=1.0) -> cv2.typing.MatLike:
        """Adjust the contrast of an image. Alpha values >1 increase contrast, <1 decrease contrast."""
        image = cv2.convertScaleAbs(image, alpha=alpha)
        return image

    def apply_sharpening(self, image, strength=0) -> cv2.typing.MatLike:
        """Apply sharpening to an image."""
        kernel = np.array([[-1, -1, -1], [-1, 9 + strength, -1], [-1, -1, -1]])
        image = cv2.filter2D(image, -1, kernel)
        return image
