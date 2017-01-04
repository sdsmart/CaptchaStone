from django.db import models

def set_tag_folder(instance, filename):
    '''
    Sets upload directory for images to MEDIA_ROOT/images/tag/
    '''
    return 'images/{tag}/{file_name}'.format(
        tag = instance.tag, file_name = filename)

class Image(models.Model):
    '''
    Image model.
    '''
    tag = models.CharField(max_length = 64) #How descriptive could a tag possibly be?
    image_file = models.ImageField(upload_to = set_tag_folder)

class Captcha(models.Model):
    token = models.CharField(max_length = 64)
    key = models.BinaryField()
    grid_images = models.BinaryField()
