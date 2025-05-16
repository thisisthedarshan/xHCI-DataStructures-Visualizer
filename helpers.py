# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

# This file contains helper functions

from PIL import Image, ImageFont, ImageDraw

def convert32BitToLEBytesArray(dataIn32BitForm:list[int]) -> list[int]:
  '''This function Converts 32-bit int array to an array of bytes'''
  result:list[int] = []
  for bit32Value in dataIn32BitForm:
    resultingBytes = bit32Value.to_bytes(4,'little')
    result += list(resultingBytes)
  return result


def bytes2binList(dataBytesList:list[int]) -> list[int]:
    '''This function takes in a list of bytes (Little Endian format) and creates 32-bit binary list and returns it'''
    rows:list[int] = []
    for i in range(0,len(dataBytesList),4):
        row = int.from_bytes(dataBytesList[i:i+4], "little")
        rows.append(row)
    
    # We have the values. Split them in binary list items
    rawBinData:list[list[int]] = []
    for i in range(0, len(rows),1):
        rawBinary = bin(rows[i])[2:].zfill(32)
        rawBinaryList = [int(bit) for bit in rawBinary]
        rawBinData.append(rawBinaryList)

    return rawBinData

def addWatermark(image_path):
    """
    Adds a watermark to a PNG image by extending it from the bottom and adding text.
    
    Args:
        image_path (str): Path to the PNG image file.
    """
    # Open the original image
    img = Image.open(image_path)
    original_height = img.height
    original_width = img.width
    mode = img.mode
    
    # Set padding and font size
    padding = 20  # pixels
    dynamic_size = original_height/69
    font_size = max(dynamic_size, 18)
    
    try:
        font = ImageFont.truetype("Anta-Regular.ttf", font_size)
    except IOError:
        print("Font not found, using default font")
        font = ImageFont.load_default()
    
    # Define texts
    left_text = "Made with xHCI-DataStructures-Visualizer"
    right_text = "github.com/thisisthedarshan/xHCI-DataStructures-Visualizer"
    center_text = "With Love from :D"
    
    # Create a temporary draw object to measure text
    temp_img = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(temp_img)
    
    # Get text sizes
    left_bbox = draw.textbbox((0, 0), left_text, font=font)
    center_bbox = draw.textbbox((0, 0), center_text, font=font)
    right_bbox = draw.textbbox((0, 0), right_text, font=font)
    
    left_width = left_bbox[2] - left_bbox[0]
    left_height = left_bbox[3] - left_bbox[1]
    center_width = center_bbox[2] - center_bbox[0]
    center_height = center_bbox[3] - center_bbox[1]
    right_width = right_bbox[2] - right_bbox[0]
    right_height = right_bbox[3] - right_bbox[1]
    
    max_text_height = max(left_height, center_height, right_height)
    
    # Set extension height based on text size
    extension_height = max_text_height + 2 * padding
    
    # Create new image with extended height
    new_height = original_height + extension_height
    if mode == 'RGBA':
        new_img = Image.new('RGBA', (img.width, new_height), (255, 255, 255, 255))
    else:
        new_img = Image.new('RGB', (img.width, new_height), (255, 255, 255))
    new_img.paste(img, (0, 0))
    
    # Create draw object for new image
    draw = ImageDraw.Draw(new_img)
    
    # Set text color based on image mode
    if mode == 'RGBA':
        text_color = (0, 0, 0, 128)  # Semi-transparent black
    else:
        text_color = (0, 0, 0)  # Solid black
    
    # Calculate y position for all texts
    y_position = original_height + padding
    
    # Draw left text
    left_x = padding
    draw.text((left_x, y_position), left_text, font=font, fill=text_color)
    
    # Draw center text
    center_x = (img.width - center_width) / 2
    draw.text((center_x, y_position), center_text, font=font, fill=text_color)
    
    # Draw right text
    right_x = img.width - right_width - padding
    draw.text((right_x, y_position), right_text, font=font, fill=text_color)
    
    # Save over original file
    new_img.save(image_path)
    
