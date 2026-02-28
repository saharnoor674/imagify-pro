"""
Video Generation Router - UPDATED VERSION
Uses wan-video/wan-2.2-i2v-fast (faster ~39 seconds)
"""

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
import replicate
import os
import tempfile
import requests
import time

router = APIRouter()

# Set your Replicate API token
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")

if REPLICATE_API_TOKEN:
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN


@router.post("/api/animate/video")
async def generate_video(file: UploadFile = File(...)):
    """
    Generate video with blinking, smile and head movement from a face image.
    Uses wan-video/wan-2.2-i2v-fast model (~39 seconds)
    """

    if not REPLICATE_API_TOKEN:
        raise HTTPException(
            status_code=500,
            detail="REPLICATE_API_TOKEN not set. Please set your API token in environment variables."
        )

    temp_input_path = None
    temp_output_path = None

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_input:
            content = await file.read()
            temp_input.write(content)
            temp_input_path = temp_input.name

        print(f"Processing image: {temp_input_path}")
        print("Starting video generation with Wan 2.2 Fast...")

        # Open the file for Replicate
        with open(temp_input_path, "rb") as image_file:
            print("Calling Replicate API...")

            output = replicate.run(
                "wan-video/wan-2.2-i2v-fast",
                input={
                    "image": image_file,
                    "prompt": "person with natural smile, eyes blinking gently, slight head movement, looking at camera, realistic, smooth motion",
                    "negative_prompt": "distorted face, blurry, artifacts, unnatural movement",
                    "resolution": "480p",
                    "num_frames": 81,
                }
            )

        print(f"Video generation completed!")
        print(f"Output: {output}")

        # ── Extract video URL (handles all output types) ──────────────────────
        video_url = None

        if isinstance(output, str) and output.startswith('http'):
            # Direct string URL
            video_url = output
        elif isinstance(output, list) and len(output) > 0:
            # List of URLs or file objects
            video_url = str(output[0])
        elif hasattr(output, 'url'):
            # Object with url attribute
            video_url = output.url
        elif hasattr(output, '__iter__'):
            # Iterable - try to get first item
            for item in output:
                video_url = str(item)
                if video_url.startswith('http'):
                    break

        # Last resort - convert to string
        if not video_url:
            video_url = str(output)

        if not video_url or not video_url.startswith('http'):
            raise HTTPException(
                status_code=500,
                detail=f"Could not extract video URL. Output: {output}"
            )

        print(f"Downloading video from: {video_url}")

        # Download the generated video
        video_response = requests.get(video_url, timeout=180)
        video_response.raise_for_status()

        print(f"Video downloaded! Size: {len(video_response.content)} bytes")

        # Save video to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_output:
            temp_output.write(video_response.content)
            temp_output_path = temp_output.name

        print(f"Video saved to: {temp_output_path}")

        # Clean up input file
        if temp_input_path and os.path.exists(temp_input_path):
            try:
                time.sleep(0.1)
                os.unlink(temp_input_path)
            except PermissionError:
                print(f"Warning: Could not delete input file: {temp_input_path}")

        # Return the video file
        def cleanup_file(path):
            try:
                if os.path.exists(path):
                    time.sleep(0.5)
                    os.unlink(path)
            except Exception as e:
                print(f"Cleanup error: {e}")

        return FileResponse(
            temp_output_path,
            media_type="video/mp4",
            filename="animated_video.mp4",
            background=BackgroundTask(cleanup_file, temp_output_path)
        )

    except replicate.exceptions.ReplicateError as e:
        error_msg = str(e)
        print(f"Replicate API error: {error_msg}")
        cleanup_temp_files(temp_input_path, temp_output_path)

        if "401" in error_msg or "authentication" in error_msg.lower():
            detail = "Invalid API token. Please check your REPLICATE_API_TOKEN."
        elif "402" in error_msg or "payment" in error_msg.lower():
            detail = "Insufficient credits. Please add credits to your Replicate account."
        elif "404" in error_msg:
            detail = "Model not found. Check your internet connection."
        elif "422" in error_msg:
            detail = f"Input validation failed: {error_msg}"
        else:
            detail = f"Replicate API error: {error_msg}"

        raise HTTPException(status_code=500, detail=detail)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading video: {e}")
        cleanup_temp_files(temp_input_path, temp_output_path)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to download video: {str(e)}"
        )

    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        cleanup_temp_files(temp_input_path, temp_output_path)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate video: {str(e)}"
        )


def cleanup_temp_files(input_path, output_path):
    """Helper function to cleanup temporary files (Windows-safe)"""
    for path in [input_path, output_path]:
        if path and os.path.exists(path):
            try:
                time.sleep(0.1)
                os.unlink(path)
            except Exception as e:
                print(f"Cleanup error for {path}: {e}")


@router.get("/api/animate/test")
async def test_replicate_connection():
    """Test if Replicate API token works"""
    try:
        if not REPLICATE_API_TOKEN:
            return {
                "status": "error",
                "message": "REPLICATE_API_TOKEN not set",
                "solution": "Set the environment variable with your Replicate API token"
            }

        model = replicate.models.get("wan-video/wan-2.2-i2v-fast")

        return {
            "status": "success",
            "message": "Replicate API token is valid and model exists!",
            "model": "wan-video/wan-2.2-i2v-fast",
            "estimated_time": "~39 seconds"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}",
            "suggestion": "Verify your REPLICATE_API_TOKEN and internet connection"
        }


@router.get("/api/animate/info")
async def get_model_info():
    """Get information about the video generation model"""
    return {
        "model": "wan-video/wan-2.2-i2v-fast",
        "description": "Fast image-to-video generation with natural face animation",
        "features": [
            "Natural eye blinking",
            "Smile generation",
            "Subtle head movement",
            "Smooth realistic motion"
        ],
        "estimated_time": "~39 seconds",
        "output": "480p MP4 video (~5 seconds)",
        "cost": "~$0.03-0.05 per video"
    }