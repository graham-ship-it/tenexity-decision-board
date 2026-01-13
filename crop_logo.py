
from PIL import Image
import os

def crop_image(input_path, output_path):
    try:
        img = Image.open(input_path)
        img = img.convert("RGBA")
        
        # Get bounding box of non-zero alpha (or non-white) pixels
        # First, let's assume transparent background. If not, we might need to handle white.
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
        # getbbox is usually sufficient for transparent images
        bbox = img.getbbox()
        
        # If it's a white background that is opaque, getbbox() might return the whole image.
        # Let's try to detect if it's white background
        if bbox ==  (0, 0, img.width, img.height):
             # Create a mask of non-white pixels
             # (Assume white is > 240, 240, 240)
             datas = img.getdata()
             new_data = []
             for item in datas:
                 if item[0] > 240 and item[1] > 240 and item[2] > 240:
                     new_data.append((255, 255, 255, 0)) # Make white transparent
                 else:
                     new_data.append(item)
             
             img.putdata(new_data)
             bbox = img.getbbox()

        if bbox:
            print(f"Cropping to {bbox}")
            cropped_img = img.crop(bbox)
            cropped_img.save(output_path)
            print(f"Saved cropped image to {output_path}")
        else:
            print("Could not find bounding box, saving original")
            img.save(output_path)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    crop_image("logo-original.png", "logo.png")
