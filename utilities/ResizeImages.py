from PIL import Image
import os

def resize_images(folder_path, output_folder, processed_list_path, max_count=50, size=(1024, 768)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the list of already processed images
    if os.path.exists(processed_list_path):
        with open(processed_list_path, 'r') as file:
            processed = {line.strip() for line in file}
    else:
        processed = set()

    processed_count = 0

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')) and filename not in processed:
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path)
            img_resized = img.resize(size, Image.Resampling.LANCZOS)

            output_path = os.path.join(output_folder, filename)
            img_resized.save(output_path)
            print(f"Resized and saved: {output_path}")

            processed.add(filename)
            with open(processed_list_path, 'a') as file:
                file.write(filename + '\n')

            processed_count += 1
            if processed_count >= max_count:
                break

    return processed_count

# Usage
folder_path = 'path/to/our/images'
output_folder = 'path/to/our/resized/images'
processed_list_path = 'path/to/processed_list.txt'  # Set this to keep track of what images we've already processed!
max_count = 50  # Number of images to process in one run

processed = resize_images(folder_path, output_folder, processed_list_path, max_count)