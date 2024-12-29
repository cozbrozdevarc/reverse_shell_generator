import time
import sys

def loading_animation(message, duration=2):
    line_chars = ['-', '/', '|', '\\']
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for char in line_chars:
            sys.stdout.write(f'\r{message} {char}')
            sys.stdout.flush()
            time.sleep(0.1)
    print()
