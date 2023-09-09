from src.cv import PlateDetector

pd = PlateDetector()
image_path = "test_images/N1.jpeg"

for i in range(1, 248):
    image_path = f"test_images/N{i}.jpeg"
    try:
        pd.detect_and_show(image_path)
    except:
        print(f"Could not read image {image_path}")
        continue