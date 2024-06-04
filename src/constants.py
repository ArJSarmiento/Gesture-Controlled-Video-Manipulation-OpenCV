"""
    Constants used in the project
"""
from enum import Enum


class ImageProcessingTechnique(Enum):
    BRIGHTNESS = 'brightness'
    BLUR = 'blur'
    SATURATION = 'saturation'
    CONTRAST = 'contrast'
    SHARPENING = 'sharpening'
