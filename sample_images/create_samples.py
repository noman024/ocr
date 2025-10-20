#!/usr/bin/env python3
"""
Script to create sample images for testing the OCR API
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_text_image(text, filename, size=(800, 600), bg_color='white', text_color='black'):
    """Create an image with text"""
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    # Calculate text position (center)
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        text_width = len(text) * 10
        text_height = 20
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    draw.text((x, y), text, fill=text_color, font=font)
    img.save(filename)
    print(f"Created: {filename}")


def main():
    """Create sample images"""
    os.makedirs("sample_images", exist_ok=True)
    
    # Create various test images
    create_text_image(
        "Hello World!\nThis is a test image for OCR.",
        "sample_images/text_sample.jpg"
    )
    
    create_text_image(
        "Sample Document\n\nLine 1: This is line one\nLine 2: This is line two\nLine 3: Final line",
        "sample_images/document_sample.jpg",
        size=(1000, 800)
    )
    
    create_text_image(
        "LOW CONTRAST TEXT",
        "sample_images/low_contrast.jpg",
        bg_color='lightgray',
        text_color='gray'
    )
    
    create_text_image(
        "1234567890\nABCDEFGHIJ\n!@#$%^&*()",
        "sample_images/mixed_content.jpg"
    )
    
    # Create a simple colored image without text
    img = Image.new('RGB', (400, 300), 'lightblue')
    img.save("sample_images/no_text.jpg")
    print("Created: sample_images/no_text.jpg")
    
    print("\nSample images created successfully!")
    print("You can use these to test the OCR API.")


if __name__ == "__main__":
    main()
