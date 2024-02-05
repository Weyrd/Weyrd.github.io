import os
from PIL import Image
from PIL.ExifTags import TAGS
from progress.bar import Bar
import time

# Directory paths
source_dir = "./images"
target_dir = "./images/fulls/"
thumbnail_dir = "./images/thumbs/"

# Create target directories if they don't exist
os.makedirs(target_dir, exist_ok=True)
os.makedirs(thumbnail_dir, exist_ok=True)

# Get the list of image files in the source directory
image_files = [file for file in os.listdir(source_dir) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

# Create a progress bar with the total number of image files
progress_bar = Bar('Processing images', max=len(image_files))

for file in image_files:
    # Get the full path of the source image
    source_path = os.path.join(source_dir, file)
    
    # Open the source image
    image = Image.open(source_path)
    
    # Copy the image to the target directory
    target_path = os.path.join(target_dir, file)
    image.save(target_path, exif=image.info.get("exif", b""))
    
    # Calculate the thumbnail size while maintaining the aspect ratio
    max_size = 450
    width, height = image.size
    if width > height:
        thumbnail_width = max_size
        thumbnail_height = int(max_size * (height / width))
    else:
        thumbnail_height = max_size
        thumbnail_width = int(max_size * (width / height))
        
    # Create the thumbnail with the calculated size
    thumbnail_size = (thumbnail_width, thumbnail_height)
    thumbnail = image.resize(thumbnail_size, Image.LANCZOS)
    
    # Decrease the quality of the thumbnail
    thumbnail_quality = 60
    thumbnail_path = os.path.join(thumbnail_dir, file)
    thumbnail.save(thumbnail_path, optimize=True, quality=thumbnail_quality, exif=image.info.get("exif", b""))

    # Then delete the original image
    os.remove(source_path)
    
    # Update the progress bar
    progress_bar.next()

progress_bar.finish()
print("Image processing complete!")
