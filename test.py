#coding=utf-8
import time
import pygame
file = 'plane.mp3'
pygame.mixer.init()
print("播放音乐1")
pygame.mixer.music.load(file)

pygame.mixer.music.play(loops=20)
time.sleep(10)
pygame.mixer.music.stop()
