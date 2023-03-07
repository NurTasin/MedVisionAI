from PIL import Image, ImageEnhance

# Open the grayscale image
img = Image.open("G:\Codes\MedVisionAI\db\9-518.jpg")

# Increase the brightness
enhancer = ImageEnhance.Brightness(img)
bright_img = enhancer.enhance(1.5) # increase brightness by a factor of 1.5

# Increase the contrast
enhancer = ImageEnhance.Contrast(bright_img)
final_img = enhancer.enhance(1.5) # increase contrast by a factor of 1.5

# Save the final image
final_img.save("more_white_image(1).jpg")

