import pafy
import vlc
import os

url ="https://www.youtube.com/watch?v=YXOsToLfGkw&ab_channel=HEARTBROKENCLUB%E5%82%B7%E5%BF%83%E3%81%AE%E4%BA%8B%E5%8B%99%E6%89%80"

video = pafy.new(url)

best = video.getbest()

player = vlc.MediaPlayer(best.url)
player.play()

while player.is_playing():
    break