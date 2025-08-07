import os
def bright(percent):
    result = os.system(f'brightnessctl set {percent}%')