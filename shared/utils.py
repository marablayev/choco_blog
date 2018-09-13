import uuid

from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import slugify

@deconstructible
class get_file_path(object):
    def __init__(self, prep):
        self.prep = prep
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join(self.prep, filename)

def cyrr2latin(text):
    symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
               u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
    tr = {ord(a):ord(b) for a, b in zip(*symbols)}
    return text.translate(tr)

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        title = cyrr2latin(instance.title)
        slug = slugify(title)

    ModelName = instance.__class__
    qs_exists = ModelName.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{}-{}".format(slug, uuid.uuid4().hex[:5])
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
