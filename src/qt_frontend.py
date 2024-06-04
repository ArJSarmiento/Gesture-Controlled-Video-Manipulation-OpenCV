"""
    This module contains the code for the graphical user interface of the application.
"""
import math
import time

import cv2
import imutils
import numpy as np
import pyshine as ps
from constants import ImageProcessingTechnique
from hand_tracking import HandDetector
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from video_controller import VideoController


class Ui_MainWindow(object):
    def __init__(self):
        self.default_brightness_value_now = 0
        self.default_blur_value_now = 0
        self.default_saturation_value_now = 1.0
        self.default_sharpening_value_now = 0
        self.default_contrast_value_now = 1.0

        self.brightness_value_now = None
        self.blur_value_now = None
        self.saturation_value_now = None
        self.sharpening_value_now = None
        self.contrast_value_now = None

        self.__image_processing_technique = ImageProcessingTechnique.BRIGHTNESS
        self.last_length = 0
        self.max_length = 0

        self.__video_controller = VideoController()
        self.__hand_detector = HandDetector(detection_con=0.7)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 500)
        MainWindow.setMinimumSize(QtCore.QSize(700, 500))
        MainWindow.setMaximumSize(QtCore.QSize(900, 600))
        MainWindow.setStyleSheet("background-color: rgb(30, 32, 48);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(9, 9, 910, 354))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 300))
        self.frame_2.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.frame_2.setStyleSheet("border-color: rgb(183, 189, 248);\n" "background-color: rgb(73, 77, 100);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.imageInput = QtWidgets.QLabel(self.frame_2)
        self.imageInput.setGeometry(QtCore.QRect(10, 10, 900, 355))
        self.imageInput.setText("")
        self.imageInput.setObjectName("imageInput")
        self.imageProcessingTechniqueContainer = QtWidgets.QGroupBox(self.centralwidget)
        self.imageProcessingTechniqueContainer.setGeometry(QtCore.QRect(9, 365, 900, 130))
        self.imageProcessingTechniqueContainer.setMinimumSize(QtCore.QSize(675, 100))
        self.imageProcessingTechniqueContainer.setMaximumSize(QtCore.QSize(900, 902))
        self.imageProcessingTechniqueContainer.setStyleSheet("color: rgb(255, 255, 255);")
        self.imageProcessingTechniqueContainer.setObjectName("imageProcessingTechniqueContainer")
        self.gridLayout = QtWidgets.QGridLayout(self.imageProcessingTechniqueContainer)
        self.gridLayout.setObjectName("gridLayout")

        # Image processing technique Blur===============================================================
        self.ImageBlur = QtWidgets.QFrame(self.imageProcessingTechniqueContainer)
        self.ImageBlur.setStyleSheet("")
        self.ImageBlur.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ImageBlur.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ImageBlur.setObjectName("ImageBlur")

        self.label_2 = QtWidgets.QLabel(self.ImageBlur)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 100, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setObjectName("label_2")

        self.imageBlurSlider = QtWidgets.QSlider(self.ImageBlur)
        self.imageBlurSlider.setGeometry(QtCore.QRect(10, 30, 100, 16))
        self.imageBlurSlider.setStyleSheet(
            "QSlider::handle:horizontal {\n"
            "    color: rgb(255, 255, 255);\n"
            "    border: 1px solid #5c5c5c;\n"
            "    width: 26px;\n"
            "    height: 26px;\n"
            "    border-radius: 13px; \n"
            "    background-color: rgb(211, 211, 211);\n"
            "}\n"
            "\n"
            "QSlider::handle:horizontal:hover {\n"
            "    background: rgb(185, 185, 185) /*Color on hover*/\n"
            "}\n"
            ""
        )
        self.imageBlurSlider.setOrientation(QtCore.Qt.Horizontal)
        self.imageBlurSlider.setObjectName("imageBlurSlider")
        self.imageBlurSlider.valueChanged['int'].connect(self.blur_value)

        self.imageBlurGesture = QtWidgets.QPushButton(self.ImageBlur)
        self.imageBlurGesture.setGeometry(QtCore.QRect(10, 50, 100, 16))
        self.imageBlurGesture.clicked.connect(self.set_gesture_blur)

        self.gridLayout.addWidget(self.ImageBlur, 0, 0, 1, 1)

        # Image processing technique Saturation===============================================================
        self.Saturation = QtWidgets.QFrame(self.imageProcessingTechniqueContainer)
        self.Saturation.setStyleSheet("")
        self.Saturation.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Saturation.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Saturation.setObjectName("Saturation")
        self.label_4 = QtWidgets.QLabel(self.Saturation)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 100, 16))
        self.label_4.setObjectName("label_4")
        self.saturationSlider = QtWidgets.QSlider(self.Saturation)
        self.saturationSlider.setGeometry(QtCore.QRect(10, 30, 100, 16))
        self.saturationSlider.setStyleSheet(
            "QSlider::handle:horizontal {\n"
            "    color: rgb(255, 255, 255);\n"
            "    border: 1px solid #5c5c5c;\n"
            "    width: 26px;\n"
            "    height: 26px;\n"
            "    border-radius: 13px; \n"
            "    background-color: rgb(211, 211, 211);\n"
            "}\n"
            "\n"
            "QSlider::handle:horizontal:hover {\n"
            "    background: rgb(185, 185, 185) /*Color on hover*/\n"
            "}\n"
            ""
        )
        self.saturationSlider.setOrientation(QtCore.Qt.Horizontal)
        self.saturationSlider.setObjectName("saturationSlider")
        self.saturationSlider.valueChanged['int'].connect(self.saturation_value)

        self.gridLayout.addWidget(self.Saturation, 0, 1, 1, 1)

        self.saturationGesture = QtWidgets.QPushButton(self.Saturation)
        self.saturationGesture.setGeometry(QtCore.QRect(10, 50, 100, 16))
        self.saturationGesture.clicked.connect(self.set_gesture_saturation)

        # Image processing technique Image Brightness===============================================================
        self.ImageBrightness = QtWidgets.QFrame(self.imageProcessingTechniqueContainer)
        self.ImageBrightness.setStyleSheet("")
        self.ImageBrightness.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ImageBrightness.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ImageBrightness.setObjectName("ImageBrightness")

        self.label = QtWidgets.QLabel(self.ImageBrightness)
        self.label.setGeometry(QtCore.QRect(10, 10, 100, 16))
        self.label.setObjectName("label")

        self.brightnessSlider = QtWidgets.QSlider(self.ImageBrightness)
        self.brightnessSlider.setGeometry(QtCore.QRect(10, 30, 100, 16))
        self.brightnessSlider.setStyleSheet(
            "QSlider::handle:horizontal {\n"
            "    color: rgb(255, 255, 255);\n"
            "    border: 1px solid #5c5c5c;\n"
            "    width: 26px;\n"
            "    height: 26px;\n"
            "    border-radius: 13px; \n"
            "    background-color: rgb(211, 211, 211);\n"
            "}\n"
            "\n"
            "QSlider::handle:horizontal:hover {\n"
            "    background: rgb(185, 185, 185) /*Color on hover*/\n"
            "}\n"
            ""
        )
        self.brightnessSlider.setOrientation(QtCore.Qt.Horizontal)
        self.brightnessSlider.setObjectName("brightnessSlider")
        self.brightnessSlider.valueChanged['int'].connect(self.brightness_value)

        self.brightnessGesture = QtWidgets.QPushButton(self.ImageBrightness)
        self.brightnessGesture.setGeometry(QtCore.QRect(10, 50, 100, 16))
        self.brightnessGesture.clicked.connect(self.set_gesture_brightness)

        self.gridLayout.addWidget(self.ImageBrightness, 0, 2, 1, 1)

        # Image processing technique Contrast===============================================================
        self.ImageNoise = QtWidgets.QFrame(self.imageProcessingTechniqueContainer)
        self.ImageNoise.setStyleSheet("")
        self.ImageNoise.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ImageNoise.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ImageNoise.setObjectName("ImageNoise")

        self.label_5 = QtWidgets.QLabel(self.ImageNoise)
        self.label_5.setGeometry(QtCore.QRect(10, 10, 100, 16))
        self.label_5.setObjectName("label_5")

        self.contrastSlider = QtWidgets.QSlider(self.ImageNoise)
        self.contrastSlider.setGeometry(QtCore.QRect(10, 30, 100, 16))
        self.contrastSlider.setStyleSheet(
            "QSlider::handle:horizontal {\n"
            "    color: rgb(255, 255, 255);\n"
            "    border: 1px solid #5c5c5c;\n"
            "    width: 26px;\n"
            "    height: 26px;\n"
            "    border-radius: 13px; \n"
            "    background-color: rgb(211, 211, 211);\n"
            "}\n"
            "\n"
            "QSlider::handle:horizontal:hover {\n"
            "    background: rgb(185, 185, 185) /*Color on hover*/\n"
            "}\n"
            ""
        )
        self.contrastSlider.setOrientation(QtCore.Qt.Horizontal)
        self.contrastSlider.setObjectName("contrastSlider")
        self.contrastSlider.valueChanged['int'].connect(self.contrast_value)

        self.contrastGesture = QtWidgets.QPushButton(self.ImageNoise)
        self.contrastGesture.setGeometry(QtCore.QRect(10, 50, 100, 16))
        self.contrastGesture.clicked.connect(self.set_gesture_contrast)

        self.gridLayout.addWidget(self.ImageNoise, 0, 3, 1, 1)

        # Image processing technique Sharpen===============================================================
        self.Sharpen = QtWidgets.QFrame(self.imageProcessingTechniqueContainer)
        self.Sharpen.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Sharpen.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Sharpen.setObjectName("GrayScale")

        self.label_3 = QtWidgets.QLabel(self.Sharpen)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 100, 16))
        self.label_3.setObjectName("label_3")
        self.sharpenSlider = QtWidgets.QSlider(self.Sharpen)
        self.sharpenSlider.setGeometry(QtCore.QRect(10, 30, 100, 16))
        self.sharpenSlider.setStyleSheet(
            "QSlider::handle:horizontal {\n"
            "    color: rgb(255, 255, 255);\n"
            "    border: 1px solid #5c5c5c;\n"
            "    width: 26px;\n"
            "    height: 26px;\n"
            "    border-radius: 13px; \n"
            "    background-color: rgb(211, 211, 211);\n"
            "}\n"
            "\n"
            "QSlider::handle:horizontal:hover {\n"
            "    background: rgb(185, 185, 185) /*Color on hover*/\n"
            "}\n"
            ""
        )
        self.sharpenSlider.setOrientation(QtCore.Qt.Horizontal)
        self.sharpenSlider.setObjectName("brightnessSlider")
        self.sharpenSlider.valueChanged['int'].connect(self.onSharpeningSliderChanged)

        self.sharpenGesture = QtWidgets.QPushButton(self.Sharpen)
        self.sharpenGesture.setGeometry(QtCore.QRect(10, 50, 100, 16))
        self.sharpenGesture.clicked.connect(self.set_gesture_sharpening)

        self.gridLayout.addWidget(self.Sharpen, 0, 4, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.actionSave = QtWidgets.QAction(MainWindow)

        self.actionSave.setObjectName("actionSave")
        self.actionOpen_Image = QtWidgets.QAction(MainWindow)

        self.actionOpen_Image.setObjectName("actionOpen_Image")
        self.startVideo = QtWidgets.QAction(MainWindow)
        self.startVideo.setObjectName("startVideo")

        self.actionSaveEdit = QtWidgets.QAction(MainWindow)
        self.actionSaveEdit.setObjectName("actionSaveEdit")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(313, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 1, 1, 1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Added code here
        self.brightness_value_now = self.default_brightness_value_now
        self.blur_value_now = self.default_blur_value_now
        self.saturation_value_now = self.default_saturation_value_now
        self.sharpening_value_now = self.default_sharpening_value_now
        self.contrast_value_now = self.default_contrast_value_now

        self.filename = (
            'Snapshot ' + str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.png'
        )  # Will hold the image address location
        self.tmp = None  # Will hold the temporary image for display
        self.fps = 0
        self.started = False

    def loadImage(self):
        """This function will load the camera device, obtain the image
        and set it to label using the setPhoto function
        """
        if self.started:
            self.started = False
            self.startVideo.setText('Start')
        else:
            self.started = True
            self.startVideo.setText('Stop')

        vid = cv2.VideoCapture(0)

        cnt = 0
        frames_to_count = 20
        st = 0

        while vid.isOpened():
            QtWidgets.QApplication.processEvents()
            img, self.image = vid.read()
            self.image = imutils.resize(self.image, height=480)

            if cnt == frames_to_count:
                try:  # To avoid divide by 0 we put it in try except
                    print(frames_to_count / (time.time() - st), 'FPS')
                    self.fps = round(frames_to_count / (time.time() - st))

                    st = time.time()
                    cnt = 0
                except Exception as e:
                    pass

            cnt += 1

            self.hand_tracking_handler()
            self.update()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def setPhoto(self, image):
        """This function will take image input and resize it
        only for display purpose and convert it to QImage
        to set at the label.
        """
        self.tmp = image
        image = imutils.resize(image, width=640)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.imageInput.setPixmap(QtGui.QPixmap.fromImage(image))

    def contrast_value(self, value):
        """This function will take value from the slider
        for the contrast from 0 to 99
        """
        self.contrast_value_now = max(self.default_contrast_value_now, value)
        print('Contrast: ', value)
        self.update()

    def brightness_value(self, value):
        """This function will take value from the slider
        for the brightness from 0 to 99
        """
        self.brightness_value_now = max(self.default_brightness_value_now, value)
        print('Brightness: ', value)
        self.update()

    def blur_value(self, value):
        """This function will take value from the slider
        for the blur from 0 to 99"""
        self.blur_value_now = max(self.default_blur_value_now, value)
        print('Blur: ', value)
        self.update()

    def saturation_value(self, value):
        """This function will take value from the slider
        for the saturation from 0.0 to 1.5"""
        computed_value = 1.5 * value / 100
        self.saturation_value_now = min(max(0, computed_value), 1.5)  # between 0.0 and 1.5
        print('Saturation: ', computed_value)
        self.update()

    def onSharpeningSliderChanged(self, value):
        """Update the image based on the sharpening slider value."""
        self.sharpening_value_now = max(self.default_sharpening_value_now, value)
        print('Sharpening: ', value)
        self.update()

    def onContrastSliderChanged(self, value):
        """Update the image based on the contrast slider value."""
        self.contrast_value_now = value
        print('Contrast: ', value)
        self.update()

    def update(self):
        """This function will update the photo according to the
        current values of blur and brightness and set it to photo label.
        """
        img = self.__video_controller.changeBrightness(self.image, self.brightness_value_now)
        img = self.__video_controller.changeBlur(img, self.blur_value_now)
        img = self.__video_controller.adjust_saturation(img, self.saturation_value_now)
        img = self.__video_controller.adjust_contrast(img, self.contrast_value_now)
        img = self.__video_controller.apply_sharpening(img, self.sharpening_value_now)

        # Here we add display text to the image
        text = 'FPS: ' + str(self.fps)
        img = ps.putBText(
            img,
            text,
            text_offset_x=20,
            text_offset_y=30,
            vspace=20,
            hspace=10,
            font_scale=1.0,
            background_RGB=(10, 20, 222),
            text_RGB=(255, 255, 255),
        )
        text = str(time.strftime("%H:%M %p"))
        img = ps.putBText(
            img,
            text,
            text_offset_x=self.image.shape[1] - 180,
            text_offset_y=30,
            vspace=20,
            hspace=10,
            font_scale=1.0,
            background_RGB=(228, 20, 222),
            text_RGB=(255, 255, 255),
        )
        text = f"Brightness: {self.brightness_value_now}"
        img = ps.putBText(
            img,
            text,
            text_offset_x=80,
            text_offset_y=425,
            vspace=20,
            hspace=10,
            font_scale=1.0,
            background_RGB=(20, 210, 4),
            text_RGB=(255, 255, 255),
        )
        text = f'Blur: {self.blur_value_now}: '
        img = ps.putBText(
            img,
            text,
            text_offset_x=self.image.shape[1] - 200,
            text_offset_y=425,
            vspace=20,
            hspace=10,
            font_scale=1.0,
            background_RGB=(210, 20, 4),
            text_RGB=(255, 255, 255),
        )

        self.setPhoto(img)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyShine video process"))
        self.imageProcessingTechniqueContainer.setTitle(_translate("MainWindow", "Image Processing Options"))
        self.label_2.setText(_translate("MainWindow", "Image Blur"))
        self.label_4.setText(_translate("MainWindow", "Saturation"))
        self.label.setText(_translate("MainWindow", "Image Brightness"))
        self.label_5.setText(_translate("MainWindow", "Contrast"))
        self.label_3.setText(_translate("MainWindow", "Sharpen"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setToolTip(_translate("MainWindow", "Save Photo"))
        self.actionOpen_Image.setText(_translate("MainWindow", "Open Image"))
        self.actionOpen_Image.setToolTip(_translate("MainWindow", "Open Image"))
        self.startVideo.setText(_translate("MainWindow", "Open Image"))
        self.actionSaveEdit.setText(_translate("MainWindow", "Save Edit"))
        self.imageBlurGesture.setText(_translate("MainWindow", "Set Gesture"))
        self.sharpenGesture.setText(_translate("MainWindow", "Set Gesture"))
        self.saturationGesture.setText(_translate("MainWindow", "Set Gesture"))
        self.brightnessGesture.setText(_translate("MainWindow", "Set Gesture"))
        self.contrastGesture.setText(_translate("MainWindow", "Set Gesture"))

    def hand_tracking_handler(self):
        # Angle and length variables
        min_hand = 50
        max_hand = 300
        angle_bar = 400
        angle_deg = 0

        img = self.__hand_detector.find_hands(self.image)
        lm_list = self.__hand_detector.find_position(img, draw=False)

        if lm_list:
            # Get the positions of the thumb and index finger
            x1, y1 = lm_list[4][1], lm_list[4][2]
            x2, y2 = lm_list[8][1], lm_list[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # Draw circles and line
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

            # Calculate the length between the two points
            length = math.hypot(x2 - x1, y2 - y1)

            # Interpolate angle and angle bar values
            angle_bar = np.interp(length, [min_hand, max_hand], [400, 150])
            angle_deg = np.interp(length, [min_hand, max_hand], [0, 180])

            print(f'Current length {length}')
            print(f'Last length {self.last_length}')
            self.last_length = length
            self.max_length = max(self.max_length, length)
            self.gesture_handler()

            # Draw green circle if length is below threshold
            if length < 50:
                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

        # Draw angle bar and text
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(angle_bar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(angle_deg)} deg', (40, 90), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3)

        self.setPhoto(img)

    def gesture_handler(self):
        computed_value = int(100 * self.last_length / self.max_length)
        if self.__image_processing_technique == ImageProcessingTechnique.BRIGHTNESS:
            self.brightness_value(computed_value)
        elif self.__image_processing_technique == ImageProcessingTechnique.BLUR:
            self.blur_value(computed_value)
        elif self.__image_processing_technique == ImageProcessingTechnique.SATURATION:
            self.saturation_value(computed_value)
        elif self.__image_processing_technique == ImageProcessingTechnique.SHARPENING:
            self.onSharpeningSliderChanged(computed_value)
        elif self.__image_processing_technique == ImageProcessingTechnique.CONTRAST:
            self.onContrastSliderChanged(computed_value)

    def __set_image_processing_technique_gesture(self, technique: ImageProcessingTechnique):
        print(f"Setting gesture for {technique}")
        self.reset_parameters()
        self.__image_processing_technique = technique

    def set_gesture_brightness(self):
        self.__set_image_processing_technique_gesture(ImageProcessingTechnique.BRIGHTNESS)

    def set_gesture_blur(self):
        self.__set_image_processing_technique_gesture(ImageProcessingTechnique.BLUR)

    def set_gesture_saturation(self):
        self.__set_image_processing_technique_gesture(ImageProcessingTechnique.SATURATION)

    def set_gesture_sharpening(self):
        self.__set_image_processing_technique_gesture(ImageProcessingTechnique.SHARPENING)

    def set_gesture_contrast(self):
        self.__set_image_processing_technique_gesture(ImageProcessingTechnique.CONTRAST)

    def reset_parameters(self):
        self.brightness_value_now = self.default_brightness_value_now
        self.blur_value_now = self.default_blur_value_now
        self.saturation_value_now = self.default_saturation_value_now
        self.sharpening_value_now = self.default_sharpening_value_now
        self.contrast_value_now = self.default_contrast_value_now
        self.update()
