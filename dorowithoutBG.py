import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt, QTimer
import pygame


class DesktopPet(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化窗口
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 200, 200)

        # 加載圖片
        walk_list = []
        for i in range(4):
            walk_img = pygame.image.load(f"./img/walk/0{i}.png").convert_alpha()
            walk_list.append(walk_img)
        dark_list = []
        for i in range(5):
            dark_img = pygame.image.load(f"./img/dark/0{i}.png").convert_alpha()
            dark_list.append(dark_img)

        death_list = []
        for i in range(3):
            death_img = pygame.image.load(f"./img/death/0{i}.png").convert_alpha()
            death_list.append(death_img)

        sleep_list = []
        for i in range(3):
            sleep_img = pygame.image.load(f"./img/sleep/0{i}.png").convert_alpha()
            sleep_list.append(sleep_img)

        # 初始化動畫屬性
        self.alive = True
        self.animation_list = self.walk_list
        self.index = 0
        self.sleep_counter = 0
        self.dark_counter=0
        self.update_time = pygame.time.get_ticks()

        # 設置定時器更新動畫
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(100)

        # 滑鼠拖動屬性
        self.old_pos = None

    def update_animation(self):
        """更新角色動畫"""
        ANIMATION_COOLDOWN = 100

        # 切換動畫列表
        if self.alive:
            if self.sleep_counter > 0:
                self.sleep_counter -= 1
                self.animation_list = self.sleep_list
            elif self.dark_counter>0:
                self.dark_counter-=1
                self.animation_list=self.dark_list
            else:
                if random.randint(1, 200) == 2:
                    self.animation_list = self.sleep_list
                    self.sleep_counter = 120
                elif random.randint(1,100)==5:
                    self.animation_list=self.dark_list
                    self.dark_counter=200
                else:
                    self.animation_list = self.walk_list
        else:
            self.animation_list = self.death_list

        # 更新幀
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
            if self.index >= len(self.animation_list):
                self.index = 0

        # 更新畫面
        self.repaint()

    def paintEvent(self, event):
        """繪製角色動畫"""
        painter = QPainter(self)
        current_img = self.animation_list[self.index]
        qimage = QPixmap.fromImage(
            QPixmap(pygame.image.tostring(current_img, "RGBA"), current_img.get_width(), current_img.get_height())
        )
        painter.drawPixmap(0, 0, qimage)

    def mousePressEvent(self, event):
        """滑鼠點擊事件，用於拖動"""
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        """滑鼠移動事件，用於拖動窗口"""
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        """滑鼠釋放事件"""
        if event.button() == Qt.LeftButton:
            self.old_pos = None

    def closeEvent(self, event):
        """關閉應用"""
        pygame.quit()
        event.accept()


if __name__ == "__main__":
    # 初始化 Pygame
    pygame.init()

    # 創建 PyQt 應用
    app = QApplication(sys.argv)
    desktop_pet = DesktopPet()
    desktop_pet.show()

    # 運行應用
    sys.exit(app.exec_())
