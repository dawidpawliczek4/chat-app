from PIL import Image
from django.core.exceptions import ValidationError
import os


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 100 or img.height > 100:
                raise ValidationError("Image size must be maxx 100x100 pixels")


def validate_image_file_extension(image):
    ext = os.path.splitext(image.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', ".gif"]
    if ext.lower() not in valid_extensions:
        raise ValidationError("Unsupported file extension. Supported extensions are: jpg, jpeg, png, gif")