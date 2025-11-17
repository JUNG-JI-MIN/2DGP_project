class Camera:
    def __init__(self, map_width, map_height, screen_width=800, screen_height=600):
        self.x = 0  # 카메라 왼쪽 위치
        self.y = 0  # 카메라 아래 위치
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height

    def update(self, target_x, target_y):
        # 플레이어를 화면 중심에 위치시키기
        self.x = target_x - self.screen_width // 2
        self.y = target_y - self.screen_height // 2

        # 카메라가 맵 경계를 벗어나지 않도록 제한
        self.x = max(0, min(self.x, self.map_width - self.screen_width))
        self.y = max(0, min(self.y, self.map_height - self.screen_height))

    def update_map_size(self, new_map_w, new_map_h):
        """맵 크기 변경"""
        self.map_width = new_map_w
        self.map_height = new_map_h
        self.x = 0  # 카메라 위치 초기화
        self.y = 0

    def apply(self, x, y):
        # 월드 좌표를 화면 좌표로 변환
        return x - self.x, y - self.y