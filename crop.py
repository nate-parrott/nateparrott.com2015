from PIL import Image
from generate import AssetFilter
from StringIO import StringIO

def crop_square(img, size):
    w, h = img.size
    if w > h:
        crop = (w - h) / 2, 0, w - (w - h)/2, h
    else:
        crop = 0, (h - w) / 2, w, h - (h - w)/2
    img = img.crop(crop)
    img = img.resize((size, size))
    return img

class ImageAssetFilter(AssetFilter):
    def id(self): return 'img'
    def ext(self): return '.jpg'
    def filter(self, data):
        img = Image.open(StringIO(data))
        img = self.filter_image(img)
        io = StringIO()
        img.save(io, format='JPEG')
        data = io.getvalue()
        io.close()
        return data
        
    def filter_image(self, img):
        return img

class SquareCropAssetFilter(ImageAssetFilter):
    def __init__(self, size):
        self.size = size
    def id(self):
        return 'square-crop-{0}'.format(self.size)
    def filter_image(self, img):
        return crop_square(img, self.size)
