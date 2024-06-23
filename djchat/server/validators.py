from PIL import Image
from django.core.exceptions import ValidationError
import os


def validate_icon_image_size(image):
    '''
    Validate image size is less than 100x100

    Args:
        `image` (File): Image file

    Raises:
        `ValidationError`: If image size is greater than 100x100
    '''
    if image:
        with Image.open(image) as img:
            if img.height > 100 or img.width > 100:
                raise ValidationError(
                    f"Image size should be less than 100x100, "
                    f"but got {img.height}x{img.width}"
                )


def validate_image_file_extension(file):
    '''
    Validate image file extension is .png or .jpg

    Args:
        `file` (File): Image file

    Raises:
        `ValidationError`: If image file extension is not .png or .jpg
    '''
    ext = os.path.splitext(file.name)[1]  # [1] returns the extension
    valid_extensions = [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension.")
