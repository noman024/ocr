#!/usr/bin/env python3
"""
Create sample test images for OCR testing.
Run this script to generate test images with known text content.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_text_image(text, filename, size=(800, 200), bg_color='white', text_color='black'):
    """Create an image with text for OCR testing."""
    # Create image
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position (center)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Save image
    img.save(filename, 'JPEG', quality=95)
    print(f"Created: {filename}")

def create_no_text_image(filename, size=(400, 300)):
    """Create an image without text."""
    # Create a simple gradient image
    img = Image.new('RGB', size, 'lightblue')
    draw = ImageDraw.Draw(img)
    
    # Draw some shapes (no text)
    draw.rectangle([50, 50, 350, 250], outline='blue', width=3)
    draw.ellipse([100, 100, 300, 200], outline='red', width=2)
    
    img.save(filename, 'JPEG', quality=95)
    print(f"Created: {filename}")

def main():
    """Create all sample test images."""
    print("Creating sample test images...")
    
    # Create images with text
    create_text_image(
        "Hello World! This is a test image for OCR.",
        "text_sample.jpg",
        size=(800, 200)
    )
    
    create_text_image(
        "Document Processing\nMultiple Lines\nOCR Testing",
        "document_sample.jpg", 
        size=(600, 300)
    )
    
    create_text_image(
        "Low Contrast Text",
        "low_contrast.jpg",
        size=(600, 150),
        bg_color='lightgray',
        text_color='gray'
    )
    
    create_text_image(
        "Mixed Content\nText and Graphics",
        "mixed_content.jpg",
        size=(700, 250)
    )
    
    # Create image without text
    create_no_text_image("no_text.jpg")
    
    print("\n✅ All sample images created successfully!")
    print("You can now test the OCR API with these images.")

if __name__ == "__main__":
    main()
