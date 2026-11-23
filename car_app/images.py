"""Versionet WebP të fotove të makinave (480 / 960 / 1600 px).

Kur ruhet një makinë, krijohen kopje të vogla WebP pranë fotos origjinale
(p.sh. cars/bmw.jpg -> cars/bmw-480.webp, cars/bmw-960.webp, cars/bmw-1600.webp).
Faqet përdorin `srcset`, kështu që telefoni shkarkon vetëm madhësinë që i duhet.
"""
from io import BytesIO
from pathlib import PurePosixPath

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image, ImageOps

SIZES = (480, 960, 1600)
QUALITY = 75


def variant_name(name, width):
    return f"{PurePosixPath(name).with_suffix('')}-{width}.webp"


def make_variants(name, storage=default_storage):
    """Krijon versionet që mungojnë. Kthen sa versione u krijuan."""
    missing = [w for w in SIZES if not storage.exists(variant_name(name, w))]
    if not missing:
        return 0
    with storage.open(name, "rb") as f:
        image = ImageOps.exif_transpose(Image.open(f))  # foto nga telefoni: rrotullimi i saktë
        image = image.convert("RGB")
    for width in missing:
        copy = image.copy()
        if copy.width > width:
            copy = copy.resize((width, round(copy.height * width / copy.width)), Image.LANCZOS)
        buffer = BytesIO()
        copy.save(buffer, "WEBP", quality=QUALITY, method=6)
        storage.save(variant_name(name, width), ContentFile(buffer.getvalue()))
    return len(missing)


def variant_urls(name, storage=default_storage):
    """{gjerësia: url} vetëm për versionet që ekzistojnë."""
    return {
        w: storage.url(variant_name(name, w))
        for w in SIZES
        if storage.exists(variant_name(name, w))
    }
