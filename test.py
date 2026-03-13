# -*- coding: utf-8 -*-

"""
Project: Gujarati Character Recognition using CNN
File: test.py

Description:
This file creates a simple PyQt5 GUI window with a START button.
It is mainly used as a starting interface for launching the
character recognition application.
"""

# ===============================
# Import Required Libraries
# ===============================

import sys
from PyQt5 import QtCore, QtGui, QtWidgets


# ===============================
# UI Class Definition
# ===============================

class Ui_MainWindow(object):
    """
    This class builds the GUI window.
    """

    def setupUi(self, MainWindow):
        """
        Setup the GUI layout and widgets
        """

        # Window settings
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # START button
        self.Start = QtWidgets.QPushButton(self.centralwidget)
        self.Start.setGeometry(QtCore.QRect(260, 180, 120, 40))
        self.Start.setObjectName("Start")

        # Set central widget
        MainWindow.setCentralWidget(self.centralwidget)

        # Status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Translate UI text
        self.retranslateUi(MainWindow)

        # Auto-connect signals
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    # ===============================
    # UI Text Setup
    # ===============================

    def retranslateUi(self, MainWindow):
        """
        Set window and widget text
        """

        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(
            _translate("MainWindow", "Gujarati Character Recognition")
        )

        self.Start.setText(
            _translate("MainWindow", "START")
        )


# ===============================
# Main Application Execution
# ===============================

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())