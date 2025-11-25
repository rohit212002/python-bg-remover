import io
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image, ImageOps
import numpy as np

app = FastAPI()

# Dimensions
WIDTH, HEIGHT = 320, 202

# Colors (from your script)
CENTER_COLOR = np.array([218, 210, 197])   # light beige
EDGE_COLOR   = np.array([140, 133, 117])   # darker beige


def create_gradient_background(width=WIDTH, height=HEIGHT):
    bg = Image.new("RGB", (width, height))
    cx, cy = width // 2, height // 2
    max_dist = np.sqrt(cx*cx + cy*cy)

    for y in range(height):
        for x in range(width):
            dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            ratio = dist / max_dist
            color = CENTER_COLOR * (1 - ratio) + EDGE_COLOR * ratio
            bg.putpixel((x, y), tuple(color.astype(int)))

    return bg


def transform_image(input_image: Image.Image) -> Image.Image:
    # Ensure RGBA for rembg
    input_image = input_image.convert("RGBA")

    # Remove background
    product = remove(input_image)
    product = Image.open(io.BytesIO(product)).convert("RGBA") if isinstance(product, (bytes, bytearray)) else product

    # Create background
    bg = create_gradient_background(WIDTH, HEIGHT)

    # Resize product (contain)
    product = ImageOps.contain(product, (260, 180))

    # Center product
    x = (WIDTH - product.width) // 2
    y = (HEIGHT - product.height) // 2
    bg.paste(product, (x, y), product)

    return bg


@app.post("/transform")
async def transform(file: UploadFile = File(...)):
    # Read uploaded file
    contents = await file.read()
    input_image = Image.open(io.BytesIO(contents))

    # Transform
    output_image = transform_image(input_image)

    # Save to in-memory buffer
    buf = io.BytesIO()
    output_image.save(buf, format="JPEG", quality=95)
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="image/jpeg",
        headers={
            "Content-Disposition": 'inline; filename="output.jpg"'
        },
    )


@app.get("/")
def root():
    return {"status": "ok", "message": "Product transform API is running"}
