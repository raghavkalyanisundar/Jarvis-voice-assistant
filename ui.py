import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QTextEdit,
    QVBoxLayout, QHBoxLayout, QScrollArea
)
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QSystemTrayIcon
from PySide6.QtGui import QIcon



# CUSTOM WIDGET: the animated HUD ring

class HUDRing(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(360,360)
        self.angle = 0          # current rotation angle, in degrees
        self.status_text = "JARVIS"

        # QTimer calls self.rotate() repeatedly, forever, every 30ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.timer.start(30)   # smaller number = faster/smoother spin

    def rotate(self):
        self.angle = (self.angle + 2) % 360   # loop back to 0 after a full circle
        self.update()   # tells PyQt "redraw this widget now"

    def set_status(self, text):
        self.status_text = text
        self.update()

    # this method is called AUTOMATICALLY every time the widget needs to redraw
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # smooths out the circle edges

        center_x = self.width() / 2
        center_y = self.height() / 2
        painter.translate(center_x, center_y)   # move the "drawing origin" to the center

        self.draw_ticks(painter)

        # Outer rotating ring (dashed, spinning)
        painter.save()                # remember current rotation state
        painter.rotate(self.angle)    # rotate everything drawn after this line
        pen = QPen(QColor("#00FFFF"))
        pen.setWidth(2)
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        painter.drawEllipse(-120, -120, 240, 240)
        painter.restore()             # undo the rotation for what's drawn next

        # Middle ring (spins the opposite direction) 
        painter.save()
        painter.rotate(-self.angle * 1.5)
        pen2 = QPen(QColor("#00CFFF"))
        pen2.setWidth(2)
        painter.setPen(pen2)
        painter.drawEllipse(-90,-90, 180, 180)
        painter.restore()



        # Status text in the center
        painter.setPen(QColor("#00FFFF"))
        painter.setFont(QFont("Consolas", 12, QFont.Bold))
        painter.drawText(-60, -10, 120, 20, Qt.AlignCenter, self.status_text)

        self.draw_crosshairs(painter)

    def draw_ticks(self, painter):
        painter.save()
        pen = QPen(QColor("#00FFFF"))
        painter.setPen(pen)

        for i in range(72):   # 72 ticks = one every 5 degrees (360 / 5 = 72)
            painter.rotate(5)  # rotate a little bit before drawing each tick

            if i % 6 == 0:
                # every 6th tick (so every 30 degrees) — make it a long tick
                pen.setWidth(2)
                painter.setPen(pen)
                painter.drawLine(0, -145, 0, -160)
            else:
                # otherwise — a short tick
                pen.setWidth(1)
                painter.setPen(pen)
                painter.drawLine(0, -145, 0, -152)


        painter.restore()


    def draw_crosshairs(self, painter):
        painter.save()
        painter.rotate(self.angle * 1.5)

        pen = QPen(QColor("#00FFFF"))
        painter.setPen(pen)

        for i in range(36):
            painter.rotate(10)

            if i % 3 == 0:
                # every 3rd tick — longer, extends further outward
                pen.setWidth(2)
                painter.setPen(pen)
                painter.drawLine(0, -55, 0, -65)
            else:
                # the rest — short outward tick
                pen.setWidth(1)
                painter.setPen(pen)
                painter.drawLine(0, -55, 0, -60)

        


        painter.restore()


# Chat bubble helper — makes a styled label for STT/TTS lines
def make_bubble(text, sender):
    label = QLabel(text)
    label.setWordWrap(True)
    label.setContentsMargins(10, 6, 10, 6)

    if sender == "user":
        label.setStyleSheet("""
            background-color: #1E1E1E;
            color: #EEEEEE;
            border: 1px solid #444444;
            border-radius: 8px;
        """)
    else:  # jarvis
        label.setStyleSheet("""
            background-color: #052226;
            color: #00FFFF;
            border: 1px solid #00FFFF88;
            border-radius: 8px;
        """)
    return label



# MAIN WINDOW
class JarvisUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS")
        self.resize(1200, 650)

        # ---------------- LEFT: LOG PANEL ----------------
        log_label = QLabel("LOG")
        log_label.setStyleSheet("color: #00FFFF; font-weight: bold; letter-spacing: 1px;")
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setPlaceholderText("(no activity yet)")

        left_layout = QVBoxLayout()
        left_layout.addWidget(log_label)
        left_layout.addWidget(self.log_box)
        left_panel = QWidget()
        left_panel.setLayout(left_layout)

        # ---------------- CENTER: HUD RING ----------------
        self.hud = HUDRing()
        center_layout = QVBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(self.hud, alignment=Qt.AlignCenter)
        center_layout.addStretch()
        center_panel = QWidget()
        center_panel.setLayout(center_layout)

        # ---------------- RIGHT: CHAT BUBBLES ----------------
        chat_label = QLabel("CONVERSATION")
        chat_label.setStyleSheet("color: #00FFFF; font-weight: bold; letter-spacing: 1px;")

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.addStretch()   # keeps bubbles pinned to the top as they're added
        self.chat_container.setLayout(self.chat_layout)

        chat_scroll = QScrollArea()
        chat_scroll.setWidgetResizable(True)
        chat_scroll.setWidget(self.chat_container)

        right_layout = QVBoxLayout()
        right_layout.addWidget(chat_label)
        right_layout.addWidget(chat_scroll)
        right_panel = QWidget()
        right_panel.setLayout(right_layout)

        # ---------------- COMBINE ALL THREE ----------------
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_panel, 2)
        main_layout.addWidget(center_panel, 2)
        main_layout.addWidget(right_panel, 3)
        self.setLayout(main_layout)

        # ---------------- GLOBAL DARK THEME ----------------
        self.setStyleSheet("""
            QWidget {
                background-color: #0A0A0A;
                color: #EEEEEE;
                font-family: Consolas;
            }
            QTextEdit {
                background-color: #111111;
                border: 1px solid #00FFFF44;
                color: #EEEEEE;
            }
            QScrollArea {
                border: none;
            }
        """)
        
    def add_bubble(self, text, sender):
        bubble = make_bubble(text, sender)
        # insert before the stretch so new bubbles stack downward, top to bottom
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)

    def update_status(self, status):
        self.hud.set_status(status)

    def show_heard_text(self, text):
        self.add_bubble(text, "user")

    def show_classification(self, mode):
        pass  # not displaying this visually yet, that's fine for now

    def show_reply(self, text):
        self.add_bubble(text, "jarvis")

    def append_log(self, message):
        self.log_box.append(message)

    def show_and_focus(self):
        self.show()
        self.raise_()
        self.activateWindow()


if __name__ == "__main__":
    from assistant_thread import AssistantThread

    app = QApplication(sys.argv)
    window = JarvisUI()
    window.hide()

    thread = AssistantThread()
    thread.status_changed.connect(window.update_status)
    thread.heard_text.connect(window.show_heard_text)
    thread.classified.connect(window.show_classification)
    thread.replied_text.connect(window.show_reply)
    thread.log_message.connect(window.append_log)
    thread.app_should_quit.connect(app.quit)
    thread.show_window.connect(window.show_and_focus)
    thread.hide_window.connect(window.hide)
    thread.start()

    sys.exit(app.exec())