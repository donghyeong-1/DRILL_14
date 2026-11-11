import random
from pico2d import get_canvas_width, load_image
import game_framework

# 2D 공간 물리 스케일 정의 (10 pixel = 30 cm, 1m = 약 33.33 pixel)
PIXEL_PER_METER = (10.0 / 0.3)

# 새의 비행 속력 계산 (시속 30 km/h -> 분속 -> 초속 -> 초당 픽셀 이동 속도)
FLY_SPEED_KMPH = 30.0
FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

# 날개짓 애니메이션 프레임 증가 속도 계산 (LEC16_시간.pdf 27~28p 논리)
WINGBEAT_DISTANCE_M = 1.5  # 1회 날개짓 동안 전진하는 거리 (1.5m)
FRAMES_PER_WINGBEAT = 14   # 1회 날개짓 당 애니메이션 프레임 수 (14장)

# 1초당 몇 개의 프레임을 증가시켜야 하는가? (초당 약 77.78 FPS)
FLY_FRAMES_PER_SECOND = FLY_SPEED_MPS / WINGBEAT_DISTANCE_M * FRAMES_PER_WINGBEAT

# bird_animation.png (918x506, 5열x3행) 프레임 규격 및 화면 출력 크기
FRAME_WIDTH = 183
FRAME_HEIGHT = 168
BIRD_DRAW_WIDTH = 100
BIRD_DRAW_HEIGHT = 100


class Bird:
    image = None

    def __init__(self):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x = random.randint(100, 1500)
        self.y = random.randint(300, 550)
        self.frame = float(random.randint(0, FRAMES_PER_WINGBEAT - 1))
        self.dir = random.choice([-1, 1])

    def update(self):
        self.frame = (self.frame + FLY_FRAMES_PER_SECOND * game_framework.frame_time) % FRAMES_PER_WINGBEAT
        self.x += self.dir * FLY_SPEED_PPS * game_framework.frame_time

        half_w = BIRD_DRAW_WIDTH // 2
        if self.x >= get_canvas_width() - half_w:
            self.x = get_canvas_width() - half_w
            self.dir = -1
        elif self.x <= half_w:
            self.x = half_w
            self.dir = 1

    def draw(self):
        frame_index = int(self.frame)
        col = frame_index % 5
        row = 2 - (frame_index // 5)
        left = col * FRAME_WIDTH
        bottom = row * FRAME_HEIGHT
        flip = '' if self.dir == 1 else 'h'
        Bird.image.clip_composite_draw(
            left, bottom, FRAME_WIDTH, FRAME_HEIGHT,
            0, flip, self.x, self.y, BIRD_DRAW_WIDTH, BIRD_DRAW_HEIGHT
        )
