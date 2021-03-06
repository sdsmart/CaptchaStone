# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-14 16:10
from __future__ import unicode_literals
import os
import shutil

import django
from django.db import migrations
from PIL import Image

MAX_DIMENSION = 140

def resize_and_color_image(image_path):
    im = Image.open(image_path)
    if not im.mode == 'RGB':
        im = im.convert(mode = 'RGB')
    background_color = im.quantize(1).convert('RGB').getpixel((0, 0))
    background = Image.new('RGB', (MAX_DIMENSION, MAX_DIMENSION), background_color)
    scalar = MAX_DIMENSION / max(im.size)
    im = im.resize((int(scalar * im.width), int(scalar * im.height)))
    background.paste(im, (MAX_DIMENSION // 2 - (im.width // 2), MAX_DIMENSION // 2 \
                                                                - (im.height // 2)))
    return background 

def copy_image_file_and_save_to_db(image_model, tag, image_name, image_location):
    tag_folder = os.path.join(django.conf.settings.MEDIA_ROOT, 'images', tag)
    if tag not in os.listdir(os.path.join(django.conf.settings.MEDIA_ROOT, \
      'images').replace('\\', '/')):
        os.mkdir(tag_folder)
    new_location = os.path.join(tag_folder, image_name).replace('\\', '/')
    image = resize_and_color_image(image_location)
    image.save(new_location)
    #shutil.copy(image_location, new_location)
    image = image_model(tag = tag, image_file = \
                        os.path.join('images', tag, image_name).replace('\\', '/'))
    image.save()
    
def add_images_to_database(apps, schema_editor):
    if os.path.basename(os.path.normpath(django.conf.settings.MEDIA_ROOT)) \
      not in os.listdir(django.conf.settings.BASE_DIR):
        os.mkdir(django.conf.settings.MEDIA_ROOT)        
    if 'images' not in os.listdir(django.conf.settings.MEDIA_ROOT):
        os.mkdir(os.path.join(django.conf.settings.MEDIA_ROOT, 'images'))
    Image = apps.get_model('captcha', 'Image')
    query_set_cache = {}
    for directory_path, directory_names, files in os.walk(os.path.join( \
      django.conf.settings.DATA_MIGRATION_DIR, 'Image').replace('\\', '/')):
        if files:
            tag = os.path.basename(os.path.normpath(directory_path))
            for file in files:
                if not tag in query_set_cache:
                    query_set_cache[tag] = Image.objects.filter(tag = tag)
                if not query_set_cache[tag]:
                    copy_image_file_and_save_to_db(Image, tag, file, \
                      os.path.join(directory_path, file).replace('\\', '/'))
                else:
                    exists_in_database = False
                    for image in query_set_cache[tag]:
                        name = os.path.basename(os.path.normpath( \
                          image.image_file.path))
                        if name == file:
                            exists_in_database = True
                            break                       
                    if not exists_in_database:
                        copy_image_file_and_save_to_db(Image, tag, file, \
                          os.path.join(directory_path, file).replace('\\', '/'))

class Migration(migrations.Migration):

    dependencies = [
        ('captcha', '0002_auto_20160229_1710'),
    ]

    operations = [
        migrations.RunPython(add_images_to_database),
    ]
