from pico2d import load_image


class Character:
    # 일단은 캐릭터 스프라이트 얻기 전까지는 수업때 쓰던걸로 구현
    def __init__(self):
        # 일단 필요한 것을 생각해보자
        # 캐릭터의 좌표값, 방향 (x, y) / (Left, Right)
        self.x, self.y = 400, 90
        self.dir = 1 # | 0 : LEFT | 1 : RIGHT |
        self.speed = 0 # | 정지, 걸을 때, 달릴 때 |
        # 캐릭터 프래임
        self.frame = 0
        # 캐릭터 이미지
        self.image = load_image('animation_sheet.png')
        # 캐릭터 상태 (정지, 걷기, 달리기, 점프, 피격?, 공격?)
        self.state = 3 # | 0 : stop | 1 : walk | 2 : run | 3 : jumping | 4 : ?? | 5 : ?? |
                       # 지금은 스프라이트에 맞춰 사용 | 1 : walk | 3 : stop |
        pass

    def update(self):
        # 캐릭터의 프래임이 바뀌며 애니메이션이 바뀔거야
        self.frame = (self.frame + 1) % 8
        pass

    def handle_event(self, event):
        # 캐릭터 상태 다루는 함수 / 아직 안배웠지만 해보자고
        pass

    def draw(self):
        # 캐릭터가 그려져야겠지
        if self.dir == 0:
            self.image.clip_composite_draw(self.frame * 100, self.state * 100, 100, 100, 0, 'h', self.x, self.y, 100, 100)
        else:
            self.image.clip_draw(self.frame * 100, self.state * 100, 100, 100, self.x, self.y)
        pass
