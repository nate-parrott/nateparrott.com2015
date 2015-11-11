from PIL import Image
import os

def is_transparent(path):
    im = Image.open(path)
    im = im.convert('RGBA')
    r, g, b, a = im.getpixel((0, 0))
    return a < 255

def name_parts(path):
    _, name = os.path.split(path)
    name, _ = os.path.splitext(name)
    return name.split('-')

def is_icon(path):
    # print path, name_parts(path), 'icon' in name_parts(path)
    return 'icon' in name_parts(path)

if __name__ == '__main__':
    import sys
    print is_transparent(sys.argv[1])
