import cv2
import numpy as np
import os

def create_alpha_mask_with_grabcut(image_path, crop_size=(400, 400)):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return None, None

    # Get the dimensions of the image
    height, width = image.shape[:2]
    
    # Calculate the crop boundaries
    crop_width, crop_height = crop_size
    start_x = width // 2 - crop_width // 2 + 20
    start_y = (height // 2 - crop_height // 2) + 170

    # Define the rectangle using the crop boundaries
    rect = (start_x, start_y, crop_width, crop_height)

    # Initialize the mask
    mask = np.zeros(image.shape[:2], np.uint8)
    
    # Initializing mask with probable background and foreground
    mask[start_y:start_y + crop_height, start_x:start_x + crop_width] = cv2.GC_PR_FGD
    mask[:start_y, :] = cv2.GC_BGD
    mask[start_y + crop_height:, :] = cv2.GC_BGD
    mask[:, :start_x] = cv2.GC_BGD
    mask[:, start_x + crop_width:] = cv2.GC_BGD

    # Define the background and foreground models
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    # Apply GrabCut algorithm
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    cv2.grabCut(image, mask, None, bgd_model, fgd_model, 5, cv2.GC_EVAL)

    # Create a mask where 0 and 2 are background, 1 and 3 are foreground
    grabcut_mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Create the final alpha mask
    alpha_mask = grabcut_mask * 255


    return  alpha_mask

def process_image_sequence(base_path, start_num, end_num, crop_size=(400, 400)):
    for i in range(start_num, end_num + 1):
        image_path = f"{base_path}{i:03d}.png"  # Adjust the format according to your filenames
        alpha_mask = create_alpha_mask_with_grabcut(image_path, crop_size)
        if alpha_mask is not None:
            alpha_mask_path = f"{base_path}{i:03d}_alpha_mask.png"
            cv2.imwrite(alpha_mask_path, alpha_mask)
            print(f"Processed and saved: {alpha_mask_path}")

# Example usage
base_path = "/home/milosz/Desktop/project AR/multiview_extraction_of_3d_models/data/test_gen_dataset_2/images/img_"
start_num = 61  # Starting number of your images
end_num = 70    # Ending number of your images

process_image_sequence(base_path, start_num, end_num, crop_size=(300, 300))
