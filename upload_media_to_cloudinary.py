import os
from pathlib import Path

import django
import cloudinary
import cloudinary.uploader

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "DemoProject.settings"
)

django.setup()

from django.conf import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_STORAGE["CLOUD_NAME"],
    api_key=settings.CLOUDINARY_STORAGE["API_KEY"],
    api_secret=settings.CLOUDINARY_STORAGE["API_SECRET"],
)

MEDIA_ROOT = Path(settings.MEDIA_ROOT)


def upload_folder(folder_name):

    folder_path = MEDIA_ROOT / folder_name

    if not folder_path.exists():
        print(f"\nFolder not found: {folder_path}")
        return

    print("\n" + "=" * 60)
    print(f"UPLOADING: {folder_name}")
    print("=" * 60)

    files = [
        file
        for file in folder_path.rglob("*")
        if file.is_file()
    ]

    if not files:
        print("No files found.")
        return

    for file_path in files:

        relative_path = file_path.relative_to(MEDIA_ROOT)

        relative_path = str(relative_path).replace("\\", "/")

        cloudinary_path = "media/" + relative_path

        public_id = os.path.splitext(cloudinary_path)[0]

        print()
        print("Local file:")
        print(file_path)

        print("Cloudinary public ID:")
        print(public_id)

        try:

            result = cloudinary.uploader.upload(
                str(file_path),
                public_id=public_id,
                resource_type="image",
                overwrite=True,
                invalidate=True,
            )

            print("UPLOAD SUCCESS")
            print("Cloudinary URL:")
            print(result.get("secure_url"))

        except Exception as e:

            print("UPLOAD FAILED")
            print("Error:")
            print(e)


print()
print("=" * 60)
print("CLOUDINARY MEDIA UPLOAD")
print("=" * 60)

print(
    "Cloudinary:",
    settings.CLOUDINARY_STORAGE["CLOUD_NAME"]
)

upload_folder("player_profiles")
upload_folder("clan_logos")

print()
print("=" * 60)
print("UPLOAD COMPLETED")
print("=" * 60)