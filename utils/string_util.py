
import re

def title_to_file_name(title):
    
    cleaned_title = re.sub(r"[^\w\s]", "", title)

    return cleaned_title.lower().strip().replace(" ","_") + ".png"
