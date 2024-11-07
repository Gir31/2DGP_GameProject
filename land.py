from pico2d import load_image

class Land:
    image = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        # 플랫폼의 박스 크기
        self.top, self.bottom, self.left, self.right = self.y + 17, self.y - 17, self.x - 77, self.x + 77
        if self.image == None:
            self.image = load_image('Platform.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)