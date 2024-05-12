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

    start_x = width // 2 - crop_width // 2 +10
    start_y = (height // 2 - crop_height // 2) + 135

    return image[start_y:start_y + crop_height, start_x:start_x + crop_width]
def create_alpha_mask_with_options_input_loop(image_path, crop_size=(100, 100)):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load image.")
        return

    # Crop the image to the center
    cropped_image = crop_center(image, crop_size)
    
    # Display cropped image for debugging
    cv2.imshow("Cropped Image", cropped_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)

    # Define color ranges for brown and black
    lower_brown = np.array([10, 100, 10])
    upper_brown = np.array([25, 255, 200])
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([190, 255, 20])
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])

    # Create masks for brown and black
    mask_brown = cv2.inRange(hsv_image, lower_brown, upper_brown)

    # mask_black = cv2.inRange(hsv_image, lower_black, upper_black)

    # Clean up the brown mask with morphological operations
    # kernel = np.ones((7,7), np.uint8)
    # mask_black = cv2.morphologyEx(mask_black, cv2.MORPH_CLOSE, kernel)
    # mask_black = cv2.morphologyEx(mask_black, cv2.MORPH_OPEN, kernel)

    # Combine the masks to create a single mask for both brown and black
    # combined_mask = cv2.bitwise_or(mask_brown, mask_black)

    # Invert the mask to keep everything that is not brown or black
    inverted_mask = cv2.bitwise_not(mask_brown)
    # inverted_mask = cv2.bitwise_not(combined_mask)
    kernel = np.ones((3,3), np.uint8)
    inverted_mask= cv2.morphologyEx(inverted_mask, cv2.MORPH_CLOSE, kernel)
    inverted_mask= cv2.morphologyEx(inverted_mask, cv2.MORPH_OPEN, kernel)
    # Apply the mask to the image
    result = cv2.bitwise_and(cropped_image, cropped_image, mask=inverted_mask)

    # Show the results for debugging
    #cv2.imshow("Brown Mask", mask_brown)
    #cv2.imshow("Black Mask", mask_black)
    #cv2.imshow("Combined Mask", combined_mask)
    #cv2.imshow("Inverted Mask", inverted_mask)
    #cv2.imshow("Result", result)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    # Save the alpha mask as a separate black and white image
    alpha_mask = inverted_mask 
    #cv2.imwrite('alpha_mask.png', alpha_mask)
    print("Alpha mask saved as 'alpha_mask.png'.")

    # Convert the final chosen image to include an alpha channel
    #final_output = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    #final_output[:, :, 3] = alpha_mask

    # Save the final image
    cv2.imwrite('final_output_with_alpha.png', alpha_mask)
    print("Final image saved as 'final_output_with_alpha.png'.")

    # Display the final image
    #cv2.imshow("Final Output", final_output)
    cv2.imshow("Alpha Mask", alpha_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
# Example usage
image_path = "C:\\Users\\HP\\Desktop\\SDU\\SEM2\\Project in Advanced Robotics\\data\\benchy_2\\images\\img_139.png"
create_alpha_mask_with_options_input_loop(image_path, crop_size=(300, 290))
