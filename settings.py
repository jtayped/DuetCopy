import ctypes

user32 = ctypes.windll.user32
HEIGHT = user32.GetSystemMetrics(1)
WIDTH = HEIGHT/2

FPS = 60