from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import uuid
import subprocess
import os

app = FastAPI()

BASE = "/tmp"

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    input_path = f"{BASE}/{file_id}_input.png"
    output_path = f"{BASE}/{file_id}_nobg.png"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    cmd = ["python3", "remove_bg.py", input_path, output_path]
    subprocess.run(cmd, check=True)

    return FileResponse(output_path, media_type="image/png")


@app.post("/transform")
async def transform(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    input_path = f"{BASE}/{file_id}_nobg.png"
    output_path = f"{BASE}/{file_id}_final.jpg"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    cmd = ["python3", "transform_product.py", input_path, output_path]
    subprocess.run(cmd, check=True)

    return FileResponse(output_path, media_type="image/jpeg")
