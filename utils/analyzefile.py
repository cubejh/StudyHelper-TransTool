import io
import tempfile
from pathlib import Path
import shutil
from google import genai
from PIL import Image

def analyze_images(API_KEY, image_list, PROMPT, MODEL, fileName):
    from google import genai
    import os

    client = genai.Client(api_key=API_KEY)
    uploaded_files = []

    temp_dir = tempfile.mkdtemp() 
    #print("uploading_picture...")
    for idx, img in enumerate(image_list):
        temp_path = Path(temp_dir) / f"image_{idx+1}.png"
        img.save(temp_path, format="PNG")  
        uploaded_file = client.files.upload(file=str(temp_path))
        uploaded_files.append(uploaded_file)

    #print("Analyzing...")
    response = client.models.generate_content(
        model=MODEL,
        contents=uploaded_files + [PROMPT]
    )
    shutil.rmtree(temp_dir)
    return response.text

def paths_to_images(image_paths):
    """
    :param image_paths: List[str]
    :return: List[PIL.Image]
    """
    images = []
    for path in image_paths:
        try:
            img = Image.open(path).convert("RGB")
            images.append(img)
        except Exception as e:
            print(f"Error opening {path}: {e}")
    return images

def analyzefile(API_KEY, file_path, PROMPT,MODEL) :
    """

    """
    client = genai.Client(api_key=API_KEY)
    print("uploading file...")
    uploaded_file = client.files.upload(file = file_path)

    print("analyzing...")
    response = client.models.generate_content(
        model = MODEL,
        contents=[
            uploaded_file,
            PROMPT
        ]
    )
    return response.text