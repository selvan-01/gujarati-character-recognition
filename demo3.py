# -*- coding: utf-8 -*-

"""
Project: Gujarati Character Recognition using CNN
Description:
PyQt5 GUI application for Gujarati character recognition using a CNN model.
The application allows users to:
1. Browse an image
2. Classify the character
3. Train the CNN model
"""

# ==============================
# Import Libraries
# ==============================

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

# Keras Imports
from keras.preprocessing import image
from keras.models import Sequential, model_from_json
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.layers import BatchNormalization, Dropout
from keras.preprocessing.image import ImageDataGenerator


# ==============================
# Main UI Class
# ==============================

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        # Central Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        # Browse Button
        self.BrowseImage = QtWidgets.QPushButton(self.centralwidget)
        self.BrowseImage.setGeometry(QtCore.QRect(160, 370, 151, 51))
        self.BrowseImage.setText("Browse Image")

        # Image Display Label
        self.imageLbl = QtWidgets.QLabel(self.centralwidget)
        self.imageLbl.setGeometry(QtCore.QRect(200, 80, 361, 261))
        self.imageLbl.setFrameShape(QtWidgets.QFrame.Box)

        # Title
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(110, 20, 621, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.title.setFont(font)
        self.title.setText("GUJARATI CHARACTER RECOGNITION USING CNN")

        # Classify Button
        self.Classify = QtWidgets.QPushButton(self.centralwidget)
        self.Classify.setGeometry(QtCore.QRect(160, 450, 151, 51))
        self.Classify.setText("Classify")

        # Training Button
        self.Training = QtWidgets.QPushButton(self.centralwidget)
        self.Training.setGeometry(QtCore.QRect(400, 450, 151, 51))
        self.Training.setText("Training")

        # Result Label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(430, 370, 111, 16))
        self.label.setText("Recognized Class")

        # Result Text Box
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(400, 390, 211, 51))

        MainWindow.setCentralWidget(self.centralwidget)

        # Button Connections
        self.BrowseImage.clicked.connect(self.loadImage)
        self.Classify.clicked.connect(self.classifyFunction)
        self.Training.clicked.connect(self.trainingFunction)

    # ==============================
    # Load Image Function
    # ==============================

    def loadImage(self):

        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )

        if fileName:
            self.file = fileName

            pixmap = QtGui.QPixmap(fileName)
            pixmap = pixmap.scaled(
                self.imageLbl.width(),
                self.imageLbl.height(),
                QtCore.Qt.KeepAspectRatio
            )

            self.imageLbl.setPixmap(pixmap)
            self.imageLbl.setAlignment(QtCore.Qt.AlignCenter)

    # ==============================
    # Classification Function
    # ==============================

    def classifyFunction(self):

        # Load model structure
        with open('model.json', 'r') as json_file:
            loaded_model = model_from_json(json_file.read())

        # Load weights
        loaded_model.load_weights("model.h5")

        labels = [
            "sunna","ek","das","be","tran","char","panc","cha","sat","at",
            "nav","ALA","ANA","B","BHA","CH","CHH","D","DA","DH",
            "DHA","F","G","GH","GNA","H","J","JH","K","KH",
            "KSH","L","M","N","P","R","S","SH","SHH","T",
            "TA","TH","THA","V","Y"
        ]

        path = self.file

        # Image preprocessing
        test_image = image.load_img(path, target_size=(128, 128))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)

        # Prediction
        result = loaded_model.predict(test_image)

        predicted_label = labels[result.argmax()]

        self.textEdit.setText(predicted_label)

    # ==============================
    # Training Function
    # ==============================

    def trainingFunction(self):

        self.textEdit.setText("Training under process...")

        model = Sequential()

        model.add(Conv2D(32,(3,3),activation='relu',input_shape=(128,128,1)))
        model.add(MaxPooling2D((2,2)))
        model.add(BatchNormalization())

        model.add(Conv2D(64,(3,3),activation='relu'))
        model.add(MaxPooling2D((2,2)))
        model.add(BatchNormalization())

        model.add(Conv2D(64,(3,3),activation='relu'))
        model.add(MaxPooling2D((2,2)))
        model.add(BatchNormalization())

        model.add(Conv2D(96,(3,3),activation='relu'))
        model.add(MaxPooling2D((2,2)))
        model.add(BatchNormalization())

        model.add(Conv2D(32,(3,3),activation='relu'))
        model.add(MaxPooling2D((2,2)))
        model.add(BatchNormalization())

        model.add(Dropout(0.2))

        model.add(Flatten())
        model.add(Dense(128,activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(45,activation='softmax'))

        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        # Data generators
        train_datagen = ImageDataGenerator(
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True
        )

        test_datagen = ImageDataGenerator(rescale=1./255)

        # Dataset loading
        training_set = train_datagen.flow_from_directory(
            'Dataset/train',
            target_size=(128,128),
            batch_size=8,
            class_mode='categorical'
        )

        test_set = test_datagen.flow_from_directory(
            'Dataset/test',
            target_size=(128,128),
            batch_size=8,
            class_mode='categorical'
        )

        # Train model
        model.fit(
            training_set,
            steps_per_epoch=100,
            epochs=10,
            validation_data=test_set,
            validation_steps=125
        )

        self.textEdit.setText("Training Completed")


# ==============================
# Main Execution
# ==============================

if __name__ == "__main__":

    import sys

    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())