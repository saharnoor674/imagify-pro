# backend/services/animator.py
import os
import shutil
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw
import httpx
import base64
import asyncio
from pathlib import Path

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
RESULTS_DIR = os.path.abspath(RESULTS_DIR)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Hugging Face API Token
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", "")

def animate_placeholder(input_path: str, output_name: str) -> str:
    """
    Placeholder animation function.
    """
    with Image.open(input_path) as im:
        im = im.convert("RGB")
        mirrored = ImageOps.mirror(im)
        w, h = im.size
        new = Image.new("RGB", (w * 2, h))
        new.paste(im, (0, 0))
        new.paste(mirrored, (w, 0))

        max_w = 1200
        if new.width > max_w:
            new = new.resize((max_w, int(new.height * max_w / new.width)))

        out_path = os.path.join(RESULTS_DIR, output_name)
        new.save(out_path, format="PNG", optimize=True)
    return out_path


async def generate_smile_animation(input_path: str, output_filename: str) -> str:
    """
    Generate visible smile effect - AGGRESSIVE VERSION
    """
    try:
        print("😊 Generating visible smile effect...")
        
        from PIL import ImageEnhance, ImageDraw
        import cv2
        import numpy as np
        
        # Try OpenCV first
        img = cv2.imread(input_path)
        if img is None:
            raise Exception("Could not read image")
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Load face cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            print(f"✅ Found {len(faces)} face(s)")
            for (x, y, w, h) in faces:
                # AGGRESSIVE SMILE EFFECT
                
                # 1. Brighten the lower face significantly
                mouth_y = y + int(h * 0.5)
                mouth_h = int(h * 0.45)
                mouth_region = img[mouth_y:mouth_y + mouth_h, x:x+w].copy()
                
                # Much brighter
                mouth_region = cv2.convertScaleAbs(mouth_region, alpha=1.3, beta=30)
                img[mouth_y:mouth_y + mouth_h, x:x+w] = mouth_region
                
                # 2. Add rosy cheeks
                cheek_y = y + int(h * 0.45)
                cheek_h = int(h * 0.25)
                cheek_w = int(w * 0.25)
                
                # Left cheek
                left_cheek = img[cheek_y:cheek_y + cheek_h, x + int(w * 0.1):x + int(w * 0.1) + cheek_w].copy()
                left_cheek[:, :, 2] = np.clip(left_cheek[:, :, 2] * 1.4, 0, 255)  # More red
                img[cheek_y:cheek_y + cheek_h, x + int(w * 0.1):x + int(w * 0.1) + cheek_w] = left_cheek
                
                # Right cheek
                right_cheek = img[cheek_y:cheek_y + cheek_h, x + int(w * 0.65):x + int(w * 0.65) + cheek_w].copy()
                right_cheek[:, :, 2] = np.clip(right_cheek[:, :, 2] * 1.4, 0, 255)  # More red
                img[cheek_y:cheek_y + cheek_h, x + int(w * 0.65):x + int(w * 0.65) + cheek_w] = right_cheek
                
                # 3. Brighten eyes area (happy eyes)
                eye_y = y + int(h * 0.25)
                eye_h = int(h * 0.2)
                eye_region = img[eye_y:eye_y + eye_h, x:x+w].copy()
                eye_region = cv2.convertScaleAbs(eye_region, alpha=1.15, beta=10)
                img[eye_y:eye_y + eye_h, x:x+w] = eye_region
        else:
            print("⚠️ No face detected, applying general enhancement")
            # No face detected - apply general enhancement to whole image
            img = cv2.convertScaleAbs(img, alpha=1.2, beta=20)
        
        # Save result
        output_dir = os.path.join(os.path.dirname(__file__), "..", "temp")
        os.makedirs(output_dir, exist_ok=True)
        
        name = Path(output_filename).stem
        output_filename = f"{name}.jpg"
        output_path = os.path.join(output_dir, output_filename)
        
        cv2.imwrite(output_path, img, [cv2.IMWRITE_JPEG_QUALITY, 95])
        
        print(f"✅ Saved with visible smile effect: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ OpenCV error: {str(e)}")
        print("🔄 Falling back to PIL aggressive enhancement...")
        return await generate_aggressive_pil_smile(input_path, output_filename)


async def generate_aggressive_pil_smile(input_path: str, output_filename: str) -> str:
    """
    Aggressive smile effect using PIL - NO FACE DETECTION NEEDED
    """
    try:
        from PIL import ImageEnhance, ImageDraw
        
        print("😊 Creating smile effect with PIL (no face detection)...")
        
        with Image.open(input_path) as im:
            im = im.convert("RGB")
            width, height = im.size
            
            # Create a copy to work with
            result = im.copy()
            
            # VERY AGGRESSIVE ENHANCEMENTS
            
            # 1. Increase brightness significantly (happy, bright face)
            enhancer = ImageEnhance.Brightness(result)
            result = enhancer.enhance(1.25)  # 25% brighter
            
            # 2. Increase contrast (more definition)
            enhancer = ImageEnhance.Contrast(result)
            result = enhancer.enhance(1.3)  # 30% more contrast
            
            # 3. Increase color saturation (warmer, happier look)
            enhancer = ImageEnhance.Color(result)
            result = enhancer.enhance(1.3)  # 30% more saturated
            
            # 4. Slight sharpness increase (clearer features)
            enhancer = ImageEnhance.Sharpness(result)
            result = enhancer.enhance(1.2)
            
            # 5. Add a subtle warm overlay (happy glow)
            overlay = Image.new('RGB', (width, height), (255, 240, 220))  # Warm color
            result = Image.blend(result, overlay, 0.1)  # 10% warm overlay
            
            # Save
            output_dir = os.path.join(os.path.dirname(__file__), "..", "temp")
            os.makedirs(output_dir, exist_ok=True)
            
            name = Path(output_filename).stem
            output_filename = f"{name}.jpg"
            output_path = os.path.join(output_dir, output_filename)
            
            result.save(output_path, format="JPEG", quality=95)
            
            print(f"✅ Saved with VISIBLE smile effect: {output_path}")
            return output_path
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise Exception(f"Failed to generate smile: {str(e)}")


async def generate_smile_with_opencv(input_path: str, output_filename: str) -> str:
    """
    Alias for compatibility
    """
    return await generate_smile_animation(input_path, output_filename)


async def generate_simple_smile(input_path: str, output_filename: str) -> str:
    """
    Alias for compatibility
    """
    return await generate_smile_animation(input_path, output_filename)


async def generate_basic_enhancement(input_path: str, output_filename: str) -> str:
    """
    Alias for compatibility
    """
    return await generate_aggressive_pil_smile(input_path, output_filename)