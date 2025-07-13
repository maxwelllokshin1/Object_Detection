import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Show up to 10 predicted images
image_paths = glob.glob('runs/detect/predict/*.jpg')[:10]

for image_path in image_paths:
    img = mpimg.imread(image_path)
    plt.figure(figsize=(8, 6))
    plt.imshow(img)
    plt.title(image_path)
    plt.axis('off')
    plt.show()
