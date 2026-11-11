from pico2d import get_canvas_width, load_image
import game_framework

# 2D 공간 물리 스케일 정의 (10 pixel = 30 cm, 1m = 약 33.33 pixel)
PIXEL_PER_METER = (10.0 / 0.3)

# 새의 비행 속력 계산 (시속 30 km/h -> 분속 -> 초속 -> 초당 픽셀 이동 속도)
FLY_SPEED_KMPH = 30.0
FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)
