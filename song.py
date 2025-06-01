import time
from threading import Thread, Lock
import sys

lock = Lock()

def teks_animasi(teks, delay=0.1):
    with lock:
        for char in teks:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

def lirik_lagu(lyric, delay, speed):
    time.sleep(delay)
    teks_animasi(lyric, speed)

def musik():
    lyrics =[
        ("we all need someone to stay", 0.1),
        ("hear you falling and lonely", 0.1),
        ("cry out", 0.1),
        ("will you fix me up?", 0.1),
        ("will you show me hope?", 0.1),
        ("the end of the day", 0.1),
        ("you were helpless", 0.1),
        ("can you keep me close?", 0.1),
        ("can you love me most?", 0.1),
        ("-rawr-", 0.2)
    ]
    delays= [2.0, 5.20, 7.26, 9.25, 11.25, 14.01, 15.18, 17.24, 19.22, 20.00]

    threads = []
    for i in range(len(lyrics)):
        lyric, speed = lyrics[i]
        t = Thread(target=lirik_lagu, args=(lyric, delays[i], speed))
        threads.append(t)
        t.start()

    for theard in threads:
        theard.join()

if __name__ == "__main__":
    musik()