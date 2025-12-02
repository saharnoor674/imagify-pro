from PIL import Image
import io

def enhance_image(image_bytes):
    # Load image from bytes
    img = Image.open(io.BytesIO(image_bytes))

    # Simple enhancement (placeholder)
    img = img.convert("RGB")
    img = img.resize((img.width * 2, img.height * 2))  # double size for demo

    # Convert back to bytes
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return buffer.getvalue()

