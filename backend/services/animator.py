# backend/services/animator.py
import os
import shutil
from PIL import Image, ImageOps
import cv2
import numpy as np
from pathlib import Path
import urllib.request

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
RESULTS_DIR = os.path.abspath(RESULTS_DIR)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Model directory
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

def animate_placeholder(input_path: str, output_name: str) -> str:
    """Placeholder animation function."""
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


def download_model_if_needed():
    """Download pre-trained smile GAN model"""
    model_path = os.path.join(MODEL_DIR, "smile_gan.pth")
    
    if os.path.exists(model_path):
        print("✅ Model already downloaded")
        return model_path
    
    print("📥 Downloading smile GAN model (~150MB)...")
    print("    This is a one-time download...")
    
    # Model URL - using a lightweight pre-trained model
    # Note: This is a placeholder URL - we need a real pre-trained model
    model_url = "https://example.com/smile_gan_model.pth"
    
    try:
        urllib.request.urlretrieve(model_url, model_path)
        print(f"✅ Model downloaded to: {model_path}")
        return model_path
    except Exception as e:
        print(f"❌ Failed to download model: {e}")
        raise Exception("Model download failed. Using fallback method.")


async def generate_smile_animation(input_path: str, output_filename: str) -> str:
    """
    Generate smile using GAN-based approach
    """
    try:
        print("🤖 GAN-based smile generation...")
        
        # Try PyTorch GAN method
        try:
            import torch
            print("✅ PyTorch available")
            result_path = await generate_smile_with_pytorch_gan(input_path, output_filename)
            return result_path
        except ImportError:
            print("⚠️ PyTorch not installed")
            print("   Install with: pip install torch torchvision")
        except Exception as e:
            print(f"⚠️ GAN method failed: {e}")
        
        # Fallback to advanced MediaPipe
        print("🔄 Using advanced MediaPipe fallback...")
        return await generate_smile_mediapipe_advanced(input_path, output_filename)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return await save_original(input_path, output_filename)


async def generate_smile_with_pytorch_gan(input_path: str, output_filename: str) -> str:
    """
    Use PyTorch-based GAN for realistic smile
    """
    import torch
    import torchvision.transforms as transforms
    
    print("🔧 Loading GAN model...")
    
    # For now, we'll use a simpler approach since we don't have a pre-trained model yet
    # This demonstrates the GAN approach structure
    
    # Read image
    img = Image.open(input_path).convert('RGB')
    img_cv = cv2.imread(input_path)
    
    # TODO: Load pre-trained GAN model
    # model = torch.load(model_path)
    # model.eval()
    
    # For now, use the best available method
    print("⚠️ Pre-trained GAN model not available yet")
    print("📋 Using hybrid approach: MediaPipe + enhanced warping")
    
    # Use enhanced version
    result = await generate_smile_mediapipe_advanced(input_path, output_filename)
    return result


async def generate_smile_mediapipe_advanced(input_path: str, output_filename: str) -> str:
    """
    BEST AVAILABLE: Enhanced MediaPipe with better warping algorithm
    """
    try:
        import mediapipe as mp
        
        print("✨ Advanced smile generation (best available)...")
        
        img = cv2.imread(input_path)
        if img is None:
            raise Exception("Could not read image")
        
        h, w, _ = img.shape
        
        # MediaPipe detection
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(img_rgb)
        
        if not results.multi_face_landmarks:
            print("⚠️ No face detected")
            return await save_original(input_path, output_filename)
        
        # Get landmarks
        face_landmarks = results.multi_face_landmarks[0]
        landmarks = []
        for landmark in face_landmarks.landmark:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            landmarks.append((x, y))
        
        print(f"✅ Detected {len(landmarks)} landmarks")
        
        # Apply BEST smile transformation we have
        result = create_best_smile(img, landmarks)
        
        # Save
        output_dir = os.path.join(os.path.dirname(__file__), "..", "temp")
        os.makedirs(output_dir, exist_ok=True)
        
        name = Path(output_filename).stem
        output_filename = f"{name}.jpg"
        output_path = os.path.join(output_dir, output_filename)
        
        cv2.imwrite(output_path, result, [cv2.IMWRITE_JPEG_QUALITY, 95])
        
        print(f"✅ Best smile created: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return await save_original(input_path, output_filename)


def create_best_smile(img, landmarks):
    """
    Best smile we can create without trained GAN
    Uses optimized warping with natural smile curve
    """
    h, w = img.shape[:2]
    
    # Mouth corners
    LEFT = 61
    RIGHT = 291
    UPPER_CENTER = 13
    LOWER_CENTER = 14
    
    left = np.array(landmarks[LEFT])
    right = np.array(landmarks[RIGHT])
    upper = np.array(landmarks[UPPER_CENTER])
    lower = np.array(landmarks[LOWER_CENTER])
    
    mouth_width = np.linalg.norm(right - left)
    
    # Strong, visible smile
    lift = int(mouth_width * 0.35)  # 35% - very visible
    
    print(f"📏 Creating smile: {lift}px lift")
    
    # Displacement field
    x_grid, y_grid = np.meshgrid(np.arange(w), np.arange(h))
    disp_x = np.zeros((h, w), dtype=np.float32)
    disp_y = np.zeros((h, w), dtype=np.float32)
    
    # Small, precise radius
    corner_radius = 18
    lip_radius = 15
    
    # Left corner UP + OUT
    dist_l = np.sqrt((x_grid - left[0])**2 + (y_grid - left[1])**2)
    weight_l = np.exp(-(dist_l**2) / (2 * corner_radius**2))
    disp_y -= lift * weight_l
    disp_x -= 3 * weight_l
    
    # Right corner UP + OUT
    dist_r = np.sqrt((x_grid - right[0])**2 + (y_grid - right[1])**2)
    weight_r = np.exp(-(dist_r**2) / (2 * corner_radius**2))
    disp_y -= lift * weight_r
    disp_x += 3 * weight_r
    
    # Upper lip - gentle curve
    UPPER_LIP = [185, 40, 37, 0, 267, 270, 409]
    for idx in UPPER_LIP:
        if idx < len(landmarks):
            pt = np.array(landmarks[idx])
            dist = np.sqrt((x_grid - pt[0])**2 + (y_grid - pt[1])**2)
            weight = np.exp(-(dist**2) / (2 * lip_radius**2))
            # Curve: more lift near corners, less in center
            dist_to_center = min(np.linalg.norm(pt - left), np.linalg.norm(pt - right))
            curve_factor = 1.0 - (dist_to_center / mouth_width) * 0.5
            disp_y -= (lift * 0.4 * curve_factor) * weight
    
    # Apply
    map_x = (x_grid + disp_x).astype(np.float32)
    map_y = (y_grid + disp_y).astype(np.float32)
    
    map_x = np.clip(map_x, 0, w - 1)
    map_y = np.clip(map_y, 0, h - 1)
    
    result = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    
    return result


async def save_original(input_path: str, output_filename: str) -> str:
    """Save original"""
    img = cv2.imread(input_path)
    output_dir = os.path.join(os.path.dirname(__file__), "..", "temp")
    os.makedirs(output_dir, exist_ok=True)
    
    name = Path(output_filename).stem
    output_filename = f"{name}.jpg"
    output_path = os.path.join(output_dir, output_filename)
    
    cv2.imwrite(output_path, img, [cv2.IMWRITE_JPEG_QUALITY, 95])
    return output_path


async def generate_smile_with_opencv(input_path: str, output_filename: str) -> str:
    return await generate_smile_animation(input_path, output_filename)

async def generate_simple_smile(input_path: str, output_filename: str) -> str:
    return await generate_smile_animation(input_path, output_filename)