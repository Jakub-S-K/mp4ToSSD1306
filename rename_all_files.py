import os


filename = "slideshow_kumo"
cnt = 0

os.chdir("vid")
for root, dirs, files in os.walk(".", topdown=True):
    for file in files:
        os.rename(file, filename+str(cnt) + ".png")
        cnt += 1