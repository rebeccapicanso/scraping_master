import os.path
from bs4 import BeautifulSoup as bs
import requests
import os, time
from datetime import datetime, timedelta
import cv2
import numpy as np
from PIL import Image
from random import randrange
from collections import defaultdict

jpg_images = []

def setup():
    os.environ['TZ'] = 'US/Aleutian'
    time.tzset()
    
    # Get yesterday's date with proper month and day
    yesterday = datetime.now() - timedelta(days=1)
    month = yesterday.strftime("%m")
    day = yesterday.strftime("%d")
    year = yesterday.strftime("%Y")
    
    hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
             '17', '18', '19', '20', '21', '22', '23']
    count = 0
    
    for x in hours:
        try:
            # Updated URL format to include proper year, month, and day
            dynamic_url_Z64A = f'https://www.ndbc.noaa.gov/images/buoycam/Z64A_{year}_{month}_{day}_{x}10.jpg'
            jpg_name_Z64A = f'Z64A_{year}_{month}_{day}_{x}11.jpg'
            
            if not os.path.exists(jpg_name_Z64A):
                img_data_Z64A = requests.get(dynamic_url_Z64A)
                
                if img_data_Z64A.status_code == 200:  # Check if download was successful
                    with open(jpg_name_Z64A, 'wb') as handler:
                        handler.write(img_data_Z64A.content)
                    count += 1
                    jpg_images.append(jpg_name_Z64A)
                    print(f"Downloaded: {jpg_name_Z64A}")
                    time.sleep(1)  # Add delay between downloads to be polite
                else:
                    print(f"Failed to download {dynamic_url_Z64A}: Status code {img_data_Z64A.status_code}")
                    
        except Exception as e:
            print(f"Error downloading image for hour {x}: {e}")
            
    print(f"Downloaded {count} new images for {year}-{month}-{day}")

# working on this, maybe not needed?
def sort_images_by_color(jpg_name):
    try:
        img = Image.open(jpg_name)
        x, y = img.size
        matrix = 250
        sample = 10
        sample_list = []
        
        for i in range(sample):
            x1 = randrange(0, x - matrix)
            y1 = randrange(0, y - matrix)
            cropped = img.crop((x1, y1, x1 + matrix, y1 + matrix))
            sample_list.append((cropped, get_dominant_color(cropped)))
            
        sample_list.sort(key=lambda x: sum(x[1]))
        
        output_dir = 'sorted_images'
        os.makedirs(output_dir, exist_ok=True)
        
        for i, (cropped_img, color) in enumerate(sample_list):
            output_path = os.path.join(output_dir, f'sorted_still_{i}_color_{color}.jpg')
            cropped_img.save(output_path)
            
        print(f"Sorted {sample} images by color from {jpg_name}")
        
    except Exception as e:
        print(f"Error processing {jpg_name}: {e}")

# working on this, maybe not needed?
def get_dominant_color(image):
    width, height = image.size
    pixels = image.getcolors(width * height)
    color_counts = defaultdict(int)
    
    for count, color in pixels:
        if isinstance(color, tuple):
            color = color[:3]
        color_counts[color] += count
        
    dominant_color = max(color_counts, key=color_counts.get)
    return dominant_color

if __name__ == "__main__":
    setup()

    for image in jpg_images:
        sort_images_by_color(image)

