from django.test import TestCase
from captcha.models import Image, set_tag_folder

class ImageTestCase(TestCase):

    def setUp(self):
        Image.objects.create(tag='peas', image_file = None)
        Image.objects.create(tag='trees', image_file = None)
        Image.objects.create(tag='keys', image_file = None)

    def test_set_tag_folder(self):
        self.assertEqual(set_tag_folder(Image.objects.get(tag='peas'), ''), 'images/peas/')
        self.assertEqual(set_tag_folder(Image.objects.get(tag='trees'), ''), 'images/trees/')
        self.assertEqual(set_tag_folder(Image.objects.get(tag='keys'), ''), 'images/keys/')
