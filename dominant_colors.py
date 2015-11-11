from PIL import Image
import urllib, StringIO
import colorsys
import color_clusters
import json
import os

def rgb2hex(rgb):
    r,g,b = rgb
    r = int(r*255)
    g = int(g*255)
    b = int(b*255)
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def dominant_colors(path, num_colors=3):
    cache_path = path + '.colors'
    if os.path.exists(cache_path):
        return json.load(open(cache_path))
    
    file = StringIO.StringIO(open(path).read())
    image = Image.open(file)
    """resize = 150
    image = image.resize((resize, resize))
    result = image.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=num_colors)
    result.putalpha(0)
    colors = result.getcolors(resize*resize)
    return [color[:3] for (count, color) in colors]"""
    out = color_clusters.colorz(image, n=num_colors)
    open(cache_path, 'w').write(json.dumps(out))
    return out

def ensure_color_difference(hsv1, hsv2):
    if hsv1[2] > hsv2[2]:
        hsv2, hsv1 = (hsv1, hsv2)
    # hsv1 is now the darker of the two
    if hsv2[2] - hsv1[2] < 0.3:
        value_shift = 0.2
        if hsv1[2] > value_shift:
            hsv1 = (hsv1[0], hsv1[1], hsv1[2]-value_shift)
        else:
            hsv2 = (hsv2[0], hsv2[1], hsv2[2]+value_shift)
    return hsv1, hsv2


def ui_colors(path):
    colors = [(255, 255, 255), (242, 87, 113)]
    try:
        colors = dominant_colors(path, num_colors=3)
    except Exception as e:
        print e
    # print "COLORS", colors
    hsv_colors = [colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0) for (r,g,b) in colors]
    hsv_colors = sorted(hsv_colors, key=lambda (h,s,v): v)

    text, background = ensure_color_difference(hsv_colors[-1], hsv_colors[0])

    d = {"background": background, "text": text}
    # print d
    for key, (h,s,v) in d.items():
        # print colorsys.hsv_to_rgb(h,s,v)
        d[key] = rgb2hex(colorsys.hsv_to_rgb(h,s,v))
    return d
