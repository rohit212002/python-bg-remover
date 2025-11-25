from fastapi import FastAPI, UploadFile, File
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    input_bytes = await file.read()
    input_img = Image.open(io.BytesIO(input_bytes)).convert("RGBA")
    output = remove(input_img)

    buf = io.BytesIO()
    output.save(buf, format="PNG")
    buf.seek(0)

    return {
        "success": True,
        "image_bytes": buf.getvalue().hex()
    }
