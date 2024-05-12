import cv2
import numpy as np

def crop_center(image, crop_size, down):
    """
    Crop the center of the image.
    
    Parameters:
    - image: The input image.
    - crop_size: Tuple of (width, height) to crop.
    - down: Pixels to shift down the starting y-coordinate
    
    Returns:
    - Cropped image.
    """
    height, width = image.shape[:2]
    crop_width, crop_height = crop_size

    start_x = width // 2 - crop_width // 2 + 10
    start_y = (height // 2 - crop_height // 2) + down

    return image[start_y:start_y + crop_height, start_x:start_x + crop_width], start_x, start_y

def process_image(image):
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color ranges for brown, black, and white
    lower_brown = np.array([10, 100, 20])
    upper_brown = np.array([25, 255, 200])
    # lower_black = np.array([0, 0, 0])
    # upper_black = np.array([180, 255, 50])


    # Create masks for brown, black, and white
    mask_brown = cv2.inRange(hsv_image, lower_brown, upper_brown)
    # mask_black = cv2.inRange(hsv_image, lower_black, upper_black)
       # Clean up the masks with morphological operations
    kernel = np.ones((7, 7), np.uint8)
    # mask_brown = cv2.morphologyEx(mask_brown, cv2.MORPH_CLOSE, kernel)
    mask_brown = cv2.morphologyEx(mask_brown, cv2.MORPH_OPEN, kernel)
    mask_brown = cv2.morphologyEx(mask_brown, cv2.MORPH_CLOSE, kernel)
    # # Clean up the masks with morphological operations
    # kernel = np.ones((7, 7), np.uint8)
    # mask_black = cv2.morphologyEx(mask_black, cv2.MORPH_CLOSE, kernel)
    # mask_black = cv2.morphologyEx(mask_black, cv2.MORPH_OPEN, kernel)

    # Combine the masks to create a single mask for both brown and black
    # combined_mask = cv2.bitwise_or(mask_brown, mask_black)

    # Invert the mask to keep everything that is not brown or black
    # inverted_mask = cv2.bitwise_not(combined_mask)
    inverted_mask = cv2.bitwise_not(mask_brown)
    # kernel = np.ones((3, 3), np.uint8)
    # inverted_mask = cv2.morphologyEx(inverted_mask, cv2.MORPH_CLOSE, kernel)
    # inverted_mask = cv2.morphologyEx(inverted_mask, cv2.MORPH_OPEN, kernel)


 
    # Save the alpha mask as a separate black and white image
    alpha_mask = inverted_mask

    return alpha_mask
def create_alpha_mask_for_sequence(base_path, start_num, end_num, crop_size=(500, 500), crop_size_alt=(600, 600), threshold=79):
    for i in range(start_num, end_num + 1):
        image_path = f"{base_path}{i:03d}.png"  # Construct the path for each image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load image: {image_path}")
            continue
       
        alt=150
        # Select crop size based on the image number
        current_crop_size = crop_size if i <= threshold else crop_size_alt
        down =90 if i <= threshold else alt
        # Crop the image
        # Crop the image
        cropped_image, start_x, start_y = crop_center(image, current_crop_size, down)
        
        # Process the image to create alpha mask
        alpha_mask_cropped = process_image(cropped_image)
        
        # Create a blank mask with the same size as the original image
        alpha_mask = np.zeros_like(image[:, :, 0])
        
        # Place the cropped alpha mask in the correct position within the blank mask
        alpha_mask[start_y:start_y + current_crop_size[1], start_x:start_x + current_crop_size[0]] = alpha_mask_cropped
        
        # Save the alpha mask
        alpha_mask_path = f"{base_path_out}{i:03d}_alpha_mask.JPG"
        cv2.imwrite(alpha_mask_path, alpha_mask, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        
        print(f"Processed and saved {alpha_mask_path}")
        
# Example usage
base_path = "/home/milosz/Desktop/project_AR/multiview_extraction_of_3d_models/data/benchy_2/images/img_"  # Base path without number or file extension
base_path_out = "/home/milosz/Desktop/project_AR/multiview_extraction_of_3d_models/data/benchy_2/alpha/img_"
start_num = 0  # Starting number of your images
end_num = 139  # Ending number of your images

create_alpha_mask_for_sequence(base_path, start_num, end_num, crop_size=(400, 500), crop_size_alt=(400, 300))
