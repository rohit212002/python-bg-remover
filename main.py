import os
import uuid
import subprocess
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

app = FastAPI()

BASE = "/tmp"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    input_path = f"{BASE}/{file_id}_input.png"
    output_path = f"{BASE}/{file_id}_nobg.png"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    # IMPORTANT → use the same python interpreter as Render’s venv
    python_exec = os.path.join(os.getcwd(), ".venv/bin/python")

    cmd = [python_exec, "remove_bg.py", input_path, output_path]
    subprocess.run(cmd, check=True)

    return FileResponse(output_path, media_type="image/png")


@app.post("/transform")
async def transform(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    input_path = f"{BASE}/{file_id}_nobg.png"
    output_path = f"{BASE}/{file_id}_final.jpg"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    python_exec = os.path.join(os.getcwd(), ".venv/bin/python")

    cmd = [python_exec, "transform_product.py", input_path, output_path]
    subprocess.run(cmd, check=True)

    return FileResponse(output_path, media_type="image/jpeg")
