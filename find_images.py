import sys, os

try:
    from PIL import Image
    import numpy as np  # pyright: ignore[reportMissingImports]
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow', 'numpy'])
    from PIL import Image
    import numpy as np  # pyright: ignore[reportMissingImports]

def dominant_color(image_path):
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        img = img.resize((50, 50))
        data = np.array(img)
        data = data.reshape(-1, 3)
        colors, counts = np.unique(data, axis=0, return_counts=True)
        dominant = colors[counts.argmax()]
        return dominant
    except Exception as e:
        return [0,0,0]

def aspect_ratio(image_path):
    try:
        img = Image.open(image_path)
        return round(img.width / img.height, 2)
    except: return 0

print("Scanning images...")
for i in range(1, 121):
    path = f"img/img{i:03d}.jpg"
    if os.path.exists(path):
        c = dominant_color(path)
        ar = aspect_ratio(path)
        # We are looking for:
        # - Collage of 2 polaroids on green background (green dominant, square/portrait AR)
        # - Safari hat (two black men and Gerard) - outdoors
        # - Kneeling with two kids in blue shirts - blue shirts prominent, outdoors
        # - Slicing green fruit with woman in blue/yellow dress - blue/green prominent
        if ar < 0.8:  # portrait
            print(f"{path}: AR={ar}, Color={c}")
        elif ar > 1.2: # landscape
            print(f"{path}: AR={ar}, Color={c}")
        else:          # roughly square
            print(f"{path}: AR={ar}, Color={c}")
