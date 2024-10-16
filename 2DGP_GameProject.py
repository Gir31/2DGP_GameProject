from pico2d import *

class character:

    def __init__(self):
        # 일단 필요한 것을 생각해보자
        # 캐릭터의 좌표값, 방향 (x, y) / (Left, Right)
        # 캐릭터 프래임
        # 캐릭터 이미지
        # 캐릭터 상태 (정지, 걷기, 달리기, 점프, 피격?, 공격?)
        self.x, self.y, self.dir, self.frame, self.state, self.img = 0, 0, 0, 0, 0, 0
        pass

    def update(self):
        # 캐릭터의 프래임이 바뀌며 애니메이션이 바뀔거야
        pass

    def handle_event(self, event):
        # 캐릭터 상태 다루는 함수 / 아직 안배웠지만 해보자고
        pass

    def draw(self):
        # 캐릭터가 그려져야겠지
        self.image.clip_draw()
        pass