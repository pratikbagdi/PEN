from PIL import ImageEnhance, ImageFilter, ImageOps

def preprocess_image(image):
    image = image.convert('L')  # Convert to grayscale
    image = ImageOps.invert(image)  # Invert image to improve contrast
    image = image.filter(ImageFilter.MedianFilter())  # Apply median filter
    image = ImageOps.autocontrast(image)  # Apply autocontrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Increase contrast
    return image
