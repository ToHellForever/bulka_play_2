"""Utility for automatic image compression on save."""
import io
import os
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile

# Maximum dimension (width or height) in pixels
MAX_SIZE = 1200
# JPEG quality (1-100)
JPEG_QUALITY = 85


def is_new_upload(image_field):
    """Check if the image field has a newly uploaded file (not an existing one)."""
    if not image_field:
        return False
    try:
        return isinstance(image_field.file, UploadedFile)
    except (ValueError, AttributeError, FileNotFoundError):
        return False


def compress_image(image_field):
    """
    Compress and resize an image field in-place.
    - Resizes so the longest side is MAX_SIZE px
    - Converts to JPEG (quality 85) for photos
    - Keeps PNG with transparency as PNG (optimized)
    - Skips GIFs (to preserve animation)

    Returns the updated image_field.
    """
    if not image_field:
        return image_field

    # Only compress newly uploaded files, not existing ones
    if not is_new_upload(image_field):
        return image_field

    try:
        # Open the uploaded image
        img = Image.open(image_field)
        img.load()  # ensure file is read
    except Exception:
        # If we can't open it, leave the original
        return image_field

    # Skip animated GIFs
    if getattr(img, "is_animated", False):
        return image_field

    # Convert RGBA/LA to RGB for JPEG, keep transparency for PNG
    has_transparency = img.mode in ("RGBA", "LA", "P") and (
        "transparency" in img.info or img.mode in ("RGBA", "LA")
    )

    # Crop to square (centered), then resize to MAX_SIZE x MAX_SIZE
    width, height = img.size
    if width != height:
        side = min(width, height)
        left = (width - side) // 2
        top = (height - side) // 2
        right = left + side
        bottom = top + side
        img = img.crop((left, top, right, bottom))

    if img.size[0] != MAX_SIZE:
        img = img.resize((MAX_SIZE, MAX_SIZE), Image.LANCZOS)

    # Prepare output
    output = io.BytesIO()

    if has_transparency:
        # Keep PNG for transparent images
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        img.save(output, format="PNG", optimize=True)
        ext = ".png"
    else:
        # Convert to JPEG for photos
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(output, format="JPEG", quality=JPEG_QUALITY, optimize=True)
        ext = ".jpg"

    output.seek(0)

    # Build new filename — keep the upload_to prefix, just change extension
    original_name = image_field.name
    # Get just the filename without path
    filename = os.path.basename(original_name)
    base_name = filename.rsplit(".", 1)[0] if "." in filename else filename
    # Get the directory part (upload_to prefix)
    dir_part = os.path.dirname(original_name)
    new_name = os.path.join(dir_part, base_name + ext) if dir_part else base_name + ext

    # Save to the field
    image_field.save(new_name, ContentFile(output.getvalue()), save=False)

    return image_field
