from pathlib import Path

from PIL import Image

from writeit.enums.image_type import ImageType
from writeit.validators.is_valid_image import IsValidImage


class ImageHandler:

    @classmethod
    def convert(cls, source: Path, to: ImageType = ImageType.JPG) -> Path:
        source = cls._rename_source(source)
        destination = cls._destination_name(source, to)

        if to == ImageType.ICO:
            return cls._convert_to_ico(source, destination)

        with Image.open(source) as image:
            prepared = cls._prepare_image(image, to)
            prepared.save(destination, **cls._options(to))

        return destination

    @classmethod
    def _rename_source(cls, source: Path) -> Path:
        source = IsValidImage.validate(source)

        extension = source.suffix.lower()

        if extension == ".jpeg":
            extension = ImageType.JPG.value

        destination = source.with_suffix(extension)

        if source != destination:
            if destination.exists():
                raise FileExistsError(f"'{destination}' already exists!")

            source = source.rename(destination)

        return source

    @staticmethod
    def _destination_name(source: Path, to: ImageType) -> Path:
        return source.with_suffix(to.value)

    @staticmethod
    def _options(image_type: ImageType) -> dict:
        options = {
            ImageType.JPG: {
                "format": "JPEG",
                "quality": 85,
                "optimize": True,
            },
            ImageType.PNG: {
                "format": "PNG",
                "optimize": True,
                "compress_level": 9,
            },
            ImageType.WEBP: {
                "format": "WEBP",
                "quality": 85,
                "method": 6,
            },
            ImageType.GIF: {
                "format": "GIF",
                "optimize": True,
            },
            ImageType.ICO: {
                "format": "ICO",
            },
            ImageType.AVIF: {
                "format": "AVIF",
                "quality": 85,
            },
        }

        return options[image_type]

    @staticmethod
    def _prepare_image(
        image: Image.Image,
        image_type: ImageType,
    ) -> Image.Image:
        supports_alpha = image_type in (
            ImageType.PNG,
            ImageType.WEBP,
            ImageType.GIF,
            ImageType.ICO,
            ImageType.AVIF,
        )

        has_alpha = "A" in image.getbands() or "transparency" in image.info

        if supports_alpha:
            return image.convert("RGBA" if has_alpha else "RGB")

        if not has_alpha:
            return image.convert("RGB")

        rgba = image.convert("RGBA")
        background = Image.new("RGB", rgba.size, "white")
        background.paste(rgba, mask=rgba.getchannel("A"))

        return background

    @classmethod
    def _convert_to_ico(cls, source: Path, destination: Path) -> Path:
        with Image.open(source) as image:
            width, height = image.size
            size = min(width, height)

            left = (width - size) // 2
            top = (height - size) // 2

            image = image.crop(
                (
                    left,
                    top,
                    left + size,
                    top + size,
                )
            )

            rgba = image.convert("RGBA")
            background = Image.new("RGB", rgba.size, "white")
            background.paste(rgba, mask=rgba.getchannel("A"))

            background = background.resize(
                (32, 32),
                Image.Resampling.LANCZOS,
            )

            background.save(
                destination,
                format="ICO",
                sizes=[(32, 32)],
                bitmap_format="bmp",
            )

        return destination
