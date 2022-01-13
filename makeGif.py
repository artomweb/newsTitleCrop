import os
from PIL import Image

imageDir = "output/"
SF = 2

images = []

for r, dirs, files in os.walk(imageDir):
    for i, filename in enumerate(files):
        img = Image.open(imageDir + filename)
        (width, height) = img.size
        r = i // SF
        if i == 50:
            print(r)
        img = img.crop((r, r, width - r, height - r))
        img = img.resize((width, height), Image.LANCZOS)
        images.append(img)


images[0].save('output-man.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=120, loop=0)
