import cv2
import numpy as np

def crop_center(image, crop_size):
    """
    Crop the center of the image.
    
    Parameters:
    - image: The input image.
    - crop_size: Tuple of (width, height) to crop.
    
    Returns:
    - Cropped image.
    """
    height, width = image.shape[:2]
    crop_width, crop_height = crop_size

    start_x = width // 2 - crop_width // 2
    start_y = (height // 2 - crop_height // 2) + 150

    return image[start_y:start_y + crop_height, start_x:start_x + crop_width]

def process_image(image):
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color ranges for brown, black, and white
    lower_brown = np.array([10, 100, 20])
    upper_brown = np.array([25, 255, 200])
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])


    # Create masks for brown, black, and white
    mask_brown = cv2.inRange(hsv_image, lower_brown, upper_brown)
    mask_black = cv2.inRange(hsv_image, lower_black, upper_black)

    # Clean up the masks with morphological operations
    kernel = np.ones((7, 7), np.uint8)
    mask_black = cv2.morphologyEx(mask_black, cv2.MORPH_CLOSE, kernel)
    mask_black = cv2.morphologyEx(mask_black, cv2.MORPH_OPEN, kernel)

    # Combine the masks to create a single mask for both brown and black
    combined_mask = cv2.bitwise_or(mask_brown, mask_black)

    # Invert the mask to keep everything that is not brown or black
    inverted_mask = cv2.bitwise_not(combined_mask)
    kernel = np.ones((3, 3), np.uint8)
    inverted_mask = cv2.morphologyEx(inverted_mask, cv2.MORPH_CLOSE, kernel)
    inverted_mask = cv2.morphologyEx(inverted_mask, cv2.MORPH_OPEN, kernel)


 
    # Save the alpha mask as a separate black and white image
    alpha_mask = inverted_mask

    return alpha_mask
def create_alpha_mask_for_sequence(base_path, start_num, end_num, crop_size=(500, 500)):
    for i in range(start_num, end_num + 1):
        image_path = f"{base_path}{i:03d}.png"  # Construct the path for each image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load image: {image_path}")
            continue
        
        # Crop the image
        cropped_image = crop_center(image, crop_size)
        
        # Process the image to create alpha mask
        alpha_mask = process_image(cropped_image)
        
        # Save the alpha mask and the final output image
        alpha_mask_path = f"{base_path}{i:03d}_alpha_mask.png"
        cv2.imwrite(alpha_mask_path, alpha_mask)
        
        print(f"Processed and saved {alpha_mask_path}")

# Example usage
base_path = "/home/milosz/Desktop/project AR/multiview_extraction_of_3d_models/data/test_gen_dataset_2/images/img_"  # Base path without number or file extension
start_num = 21  # Starting number of your images
end_num = 25  # Ending number of your images

create_alpha_mask_for_sequence(base_path, start_num, end_num, crop_size=(500, 500))
