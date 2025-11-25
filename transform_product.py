import sys
from PIL import Image, ImageOps, ImageDraw
import numpy as np

WIDTH, HEIGHT = 320, 202

CENTER_COLOR = np.array([218, 210, 197])
EDGE_COLOR   = np.array([140, 133, 117])

if len(sys.argv) < 3:
    print("Usage: python3 transform_product.py input_path output_path")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]

product = Image.open(input_path).convert("RGBA")

bg = Image.new("RGB", (WIDTH, HEIGHT))
grad = Image.new("RGB", (WIDTH, HEIGHT))
cx, cy = WIDTH // 2, HEIGHT // 2
max_dist = np.sqrt(cx*cx + cy*cy)

for y in range(HEIGHT):
    for x in range(WIDTH):
        dist = np.sqrt((x - cx)**2 + (y - cy)**2)
        ratio = dist / max_dist
        color = CENTER_COLOR * (1 - ratio) + EDGE_COLOR * ratio
        grad.putpixel((x, y), tuple(color.astype(int)))

bg = grad

product = ImageOps.contain(product, (260, 180))

x = (WIDTH - product.width) // 2
y = (HEIGHT - product.height) // 2
bg.paste(product, (x, y), product)

bg.save(output_path, "JPEG", quality=95)

print("Saved:", output_path)
