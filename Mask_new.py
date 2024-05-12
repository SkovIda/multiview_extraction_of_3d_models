import cv2
import numpy as np

def crop_center(image, crop_size,down):
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

    start_x = width // 2 - crop_width // 2 + 10
    start_y = (height // 2 - crop_height // 2) + down

    return image[start_y:start_y + crop_height, start_x:start_x + crop_width], start_x, start_y

def initial_mask_with_color_thresholding(image, crop_size,down):
    cropped_image, start_x, start_y = crop_center(image, crop_size,down)
    
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)

    # Define color ranges for brown
    lower_brown = np.array([10, 100, 10])
    upper_brown = np.array([25, 255, 200])

    # Create mask for brown
    mask_brown = cv2.inRange(hsv_image, lower_brown, upper_brown)
    # kernel = np.ones((7, 7), np.uint8)
    # mask_brown = cv2.morphologyEx(mask_brown, cv2.MORPH_CLOSE, kernel)
    # mask_brown = cv2.morphologyEx(mask_brown, cv2.MORPH_OPEN, kernel)
    # Invert the mask to keep everything that is not brown
    inverted_mask = cv2.bitwise_not(mask_brown)

    # Create a blank mask with the same size as the original image
    initial_mask = np.zeros_like(image[:, :, 0])
    
    # Place the inverted mask in the correct position within the blank mask
    initial_mask[start_y:start_y + crop_size[1], start_x:start_x + crop_size[0]] = inverted_mask

    return initial_mask, start_x, start_y, crop_size

def create_alpha_mask_with_combined_method(base_path, start_num, end_num,  crop_size=(400, 500), crop_size_alt=(400, 300), threshold=79):
    # Read the image
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
        # Create an initial mask using color thresholding
        initial_mask, start_x, start_y, crop_size = initial_mask_with_color_thresholding(image, current_crop_size, down)

        # Initialize the GrabCut mask
        mask = np.zeros(image.shape[:2], np.uint8)
        
        # Set the probable foreground and background regions
        mask[initial_mask == 0] = cv2.GC_PR_BGD
        mask[initial_mask == 255] = cv2.GC_PR_FGD
        mask[:start_y, :] = cv2.GC_BGD
        mask[start_y + crop_size[1]:, :] = cv2.GC_BGD
        mask[:, :start_x] = cv2.GC_BGD
        mask[:, start_x + crop_size[0]:] = cv2.GC_BGD
        # Define the background and foreground models
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        rect = (start_x, start_y, crop_size[0], crop_size[1])
        # Apply GrabCut algorithm
        cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_MASK)

        # Create a mask where 0 and 2 are background, 1 and 3 are foreground
        grabcut_mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
# Remove small connected components from the mask
        # grabcut_mask = remove_small_components(grabcut_mask, 50)
        # Create the final alpha mask
        alpha_mask = grabcut_mask*255
        
        # kernel = np.ones((9, 9), np.uint8)
        # alpha_mask = cv2.morphologyEx(alpha_mask, cv2.MORPH_CLOSE, kernel)
        # alpha_mask = cv2.morphologyEx(alpha_mask, cv2.MORPH_OPEN, kernel)

        alpha_mask_path = f"{base_path_out}{i:03d}_alpha_mask.JPG"
        cv2.imwrite(alpha_mask_path, alpha_mask, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        
        print(f"Processed and saved {alpha_mask_path}")
        

   
# Example usage
base_path = "C:\\Users\\HP\\Desktop\\SDU\\SEM2\\Project in Advanced Robotics\\data\\benchy_2\\images\\img_"  # Base path without number or file extension
base_path_out = "C:\\Users\\HP\\Desktop\\SDU\\SEM2\\Project in Advanced Robotics\\data\\benchy_2\\alpha\\img_"
start_num = 0  # Starting number of your images
end_num = 139  # Ending number of your images

create_alpha_mask_with_combined_method(base_path, start_num, end_num,  crop_size=(350, 450), crop_size_alt=(350, 290))
