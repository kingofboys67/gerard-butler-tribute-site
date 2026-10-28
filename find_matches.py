import os
import glob
from PIL import Image
import numpy as np  # pyright: ignore[reportMissingImports]

user_imgs = [
    "/Users/mac/.gemini/antigravity/brain/5742ab31-1d2a-4ddb-a378-b97d2a059511/media__1778015319287.png",
    "/Users/mac/.gemini/antigravity/brain/5742ab31-1d2a-4ddb-a378-b97d2a059511/media__1778015319280.png",
    "/Users/mac/.gemini/antigravity/brain/5742ab31-1d2a-4ddb-a378-b97d2a059511/media__1778015319244.png",
    "/Users/mac/.gemini/antigravity/brain/5742ab31-1d2a-4ddb-a378-b97d2a059511/media__1778015319231.png",
    "/Users/mac/.gemini/antigravity/brain/5742ab31-1d2a-4ddb-a378-b97d2a059511/media__1778015319213.png"
]

def get_feat(path):
    try:
        img = Image.open(path).convert('RGB')
        # crop middle 80% to avoid screenshot borders
        w, h = img.size
        img = img.crop((int(w*0.1), int(h*0.1), int(w*0.9), int(h*0.9)))
        img = img.resize((32, 32))
        return np.array(img).astype(float)
    except:
        return None

feats = []
files = []
for i in range(1, 121):
    f = f"img/img{i:03d}.jpg"
    if os.path.exists(f):
        feat = get_feat(f)
        if feat is not None:
            feats.append(feat)
            files.append(f)

for ui in user_imgs:
    ufeat = get_feat(ui)
    if ufeat is None: continue
    
    best_match = None
    best_dist = float('inf')
    
    for feat, f in zip(feats, files):
        dist = np.mean(np.abs(ufeat - feat))
        if dist < best_dist:
            best_dist = dist
            best_match = f
            
    print(f"Match for {os.path.basename(ui)} -> {best_match} (dist: {best_dist:.2f})")
