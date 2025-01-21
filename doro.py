import pygame
import sys,random
import button

pygame.init()

# 定義常量
FPS = 60
clock = pygame.time.Clock()

# 視窗設定
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK=(255,192,203)
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 200
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Doro')

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
#button image
kill_img=pygame.image.load("./img/button/kill.png").convert_alpha()
alive_img=pygame.image.load("./img/button/alive.png").convert_alpha()

# 玩家類
class Player:
    def __init__(self, x, y, walk_list, death_list,sleep_list,dark_list):
        self.x = x
        self.y = y
        self.walk_list = walk_list
        self.death_list = death_list
        self.sleep_list=sleep_list
        self.dark_list=dark_list
        self.alive = True
        self.index = 0
        self.sleep_counter=0
        self.death_counter=0
        self.dark_counter=0
        self.update_time = pygame.time.get_ticks()
        self.animation_list = self.walk_list
        self.img = self.animation_list[self.index]
        self.rect = self.img.get_rect(center=(self.x, self.y))
        
    def update_animation(self):
        # 設定動畫冷卻時間
        ANIMATION_COOLDOWN = 100

        # 切換動畫列表
       
        if self.alive:
            if self.sleep_counter > 0:  # 如果睡眠計數器大於 0，保持睡眠動畫
                self.sleep_counter -= 1
                self.animation_list = self.sleep_list
            elif self.dark_counter>0:
                self.dark_counter-=1
                self.animation_list=self.dark_list
            else:
                if  random.randint(1,200)==2:
                    self.animation_list = self.sleep_list
                    self.sleep_counter=80
                elif random.randint(1,100)==1:
                    self.animation_list=self.dark_list
                    self.dark_counter=200
                else:
                    self.animation_list = self.walk_list
        else:
            self.animation_list = self.death_list
            

        # 更新動畫幀
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index += 1

            # 循環播放動畫
            if self.index >= len(self.animation_list):
                self.index = 0

            self.img = self.animation_list[self.index]
        
    def draw(self, surface):
        surface.blit(self.img, self.rect.topleft)
    

# 創建玩家
player = Player(100, 100, walk_list, death_list,sleep_list,dark_list)

# 繪製背景
def draw_bg():
    SCREEN.fill(PINK)
alive_button=button.Button(30,160,alive_img,1)
kill_button=button.Button(100,160,kill_img,1)
# 遊戲主循環
while True:
    clock.tick(FPS)

    # 更新背景
    draw_bg()

    # 更新玩家動畫
    player.update_animation()
    player.draw(SCREEN)
    # 按鈕邏輯
    if kill_button.draw(SCREEN):
        player.alive = False
    if alive_button.draw(SCREEN):
        player.alive = True
    # 處理事件
    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左鍵
                player.animation_list = dark_list
                player.index = 0  # 從頭播放動畫
                player.img = player.animation_list[player.index]  # 立即刷新幀
                player.dark_counter=100
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 3:
        #         player.alive=True

    # 更新螢幕
    pygame.display.update()
