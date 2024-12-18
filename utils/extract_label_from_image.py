
import cv2
import os
from PIL import Image
import numpy as np

def get_image_label(save_path):
    # Check if the file exists
    if not os.path.exists(save_path):
        raise FileNotFoundError(f"File does not exist: {save_path}")

    # Attempt to load the image
    try:
        # Try using OpenCV first
        image = cv2.imread(save_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            # If OpenCV fails, try Pillow
            with Image.open(save_path) as img:
                image = np.array(img.convert("L"))  # Convert to grayscale
    except Exception as e:
        raise FileNotFoundError(f"Image could not be loaded: {save_path}. Error: {e}")

    # Template matching
    template_paths = [
        ("False", r"sfc_templates\false.PNG"),
        ("Misleading", r"sfc_templates\misleading.PNG"),
        ("True", r"sfc_templates\true.PNG")
    ]
        
    scores = []

    for label, template_path in template_paths:
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            raise FileNotFoundError(f"Template could not be loaded: {template_path}")

        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        scores.append(max_val)

    idx = np.argmax(scores)
    return template_paths[idx][0]



'''
import cv2
import numpy as np
from scrappers.sochfactcheck.news_extractor import extract_details
from scrappers.sochfactcheck.crawl_all_news import scrape_all_pages



#image_folder = "sochfactcheck"
#image_path = os.path.join(image_folder, title_to_file_name("Woman doctored into selfie of Maulana Fazlur Rehman and son"))


# TODO: create a function get_image_label 
# which receives an image as an argument and returns its label or None if no lable is found


def get_image_label(save_path):
    #image_path = "sochfactcheck"
    image = cv2.imread(save_path)
    #image = cv2.imread(save_path, cv2.IMREAD_GRAYSCALE)
    template_paths = [
        ("False", r"sfc_templates\false.PNG"),
        ("Misleading", r"sfc_templates\misleading.PNG"),
        ("True", r"sfc_templates\true.PNG")
    ]
   
    scores = []

    for idx, template_path in enumerate(template_paths):
        template = cv2.imread(template_path[1])

        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        scores.append(max_val)
    
    idx = np.argmax(scores)
    return (template_paths[idx][0])
    #print(template_paths[idx][0])
'''  