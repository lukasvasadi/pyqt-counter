import sys

from qtmodern import styles
from qtmodern.windows import ModernWindow

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
)

from workers import Timer


class MainWindow(QMainWindow):
    """Create user interface and manage data threads"""

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Timer boolean
        self.running = False

        # Initialize layouts
        self.layout_central = QVBoxLayout()
        self.layout_increment = QVBoxLayout()
        self.layout_controls = QVBoxLayout()
        self.layout_buttons = QHBoxLayout()

        # Initialize widgets
        self.lbl_increment = QLabel("Timer increment")
        self.txt_increment = QLineEdit("1")
        self.lbl_controls = QLabel("Timer controls")
        self.btn_start = QPushButton("Start timer")
        self.btn_stop = QPushButton("Stop timer")
        self.txt_timer = QLineEdit("0")
        self.txt_timer.setReadOnly(True)

        # Initialize thread and worker objects (good practice)
        self.thread = None
        self.worker = None

        # Restrict to integer data
        self.txt_increment.setValidator(QIntValidator(0, 10))
        self.txt_timer.setValidator(QIntValidator())

        # Connect the "clicked" signal to callback functions
        self.btn_start.clicked.connect(
            lambda: self.start_timer(int(self.txt_increment.text()))
        )
        self.btn_stop.clicked.connect(self.stop_timer)

        # Update delay value when user presses enter
        self.txt_increment.returnPressed.connect(self.update_increment)

        # Populate layouts
        self.layout_increment.addWidget(self.lbl_increment)
        self.layout_increment.addWidget(self.txt_increment)
        self.layout_buttons.addWidget(self.btn_start)
        self.layout_buttons.addWidget(self.btn_stop)
        self.layout_controls.addWidget(self.lbl_controls)
        self.layout_controls.addLayout(self.layout_buttons)
        self.layout_controls.addWidget(self.txt_timer)
        self.layout_central.addLayout(self.layout_increment)
        self.layout_central.addLayout(self.layout_controls)

        # Add margins between layouts
        self.layout_increment.setContentsMargins(10, 10, 10, 20)
        self.layout_controls.setContentsMargins(10, 10, 10, 20)

        self.setWindowTitle("PyQt Template Application")

        self.setGeometry(300, 200, 300, 200)
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(self.layout_central)

    def start_timer(self, increment: int):
        """Launch thread with timer"""

        if not self.running:
            self.running = True

            self.thread = QThread()
            self.worker = Timer(increment)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.sgl_start_cleanup.connect(self.thread.quit)
            self.worker.sgl_start_cleanup.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.finished.connect(lambda: self.txt_timer.setText("0"))
            self.worker.sgl_update_timer.connect(
                lambda time: self.txt_timer.setText(str(time))
            )

            self.thread.start()

    def stop_timer(self):
        """Close timer thread"""
        if self.running:
            self.running = False
            self.worker.running = False  # Initiates cleanup procedure

    def update_increment(self):
        if self.running:
            self.worker.increment = int(self.txt_increment.text())


def main():
    """Every PyQt application needs a main function that initializes a
    QApplication object
    """
    app = QApplication(sys.argv)
    win = MainWindow()

    styles.dark(app)

    main = ModernWindow(win)
    main.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
