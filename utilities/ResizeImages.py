import PIL.Image
if not hasattr(PIL.Image, 'Resampling'):  # Pillow<9.0
    PIL.Image.Resampling = PIL.Image
import os

def resize_images(folder_path, output_folder, processed_list_path, max_count=50, size=(1024, 768)):
    """
    Resize images in the specified folder to a given size and save them to the output folder.

    Args:
        folder_path (str): The path to the folder containing the original images.
        output_folder (str): The path to the folder where the resized images will be saved.
        processed_list_path (str): The path to the file keeping track of already processed images.
        max_count (int, optional): Maximum number of images to process in one run. Default value is 50.
        size (tuple, optional): The target size of the resized images. Default value is (1024, 768).

    Returns:
        int: The number of images processed in this run.

    Raises:
        OSError: If unable to create the output folder.
    """
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
            img = PIL.Image.open(img_path)
            img_resized = img.resize(size, PIL.Image.Resampling.LANCZOS)

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
# output paths will follow this format:
folder_path = '/work/hsiycsci4970/pstruthers/images_handheld'
output_folder = '/work/hsiycsci4970/pstruthers/handheld_output'
processed_list_path = '/work/hsiycsci4970/pstruthers/handheld.txt'  # Set this to keep track of what images we've already processed!
max_count = 100  # Number of images to process in one run

processed = resize_images(folder_path, output_folder, processed_list_path, max_count)
