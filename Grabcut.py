import cv2
import numpy as np

def create_alpha_mask_with_grabcut(image_path, crop_size=(400, 400)):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load image.")
        return

    # Get the dimensions of the image
    height, width = image.shape[:2]
    
    # Calculate the crop boundaries
    crop_width, crop_height = crop_size
    start_x = width // 2 - crop_width // 2+20
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

    # Create the result image with alpha channel
    result = cv2.bitwise_and(image, image, mask=grabcut_mask)
    final_output = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    final_output[:, :, 3] = alpha_mask

    # Show the results for debugging
    cv2.imshow("GrabCut Mask", grabcut_mask * 255)
    cv2.imshow("Result", result)
    cv2.imshow("Alpha Mask", alpha_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the alpha mask as a separate black and white image
    cv2.imwrite('alpha_mask.png', alpha_mask)
    print("Alpha mask saved as 'alpha_mask.png'.")

    # Save the final image
    cv2.imwrite('final_output_with_alpha.png', final_output)
    print("Final image saved as 'final_output_with_alpha.png'.")

# Example usage
image_path = '/home/milosz/Desktop/project AR/multiview_extraction_of_3d_models/data/test_gen_dataset_2/images/img_061.png'
create_alpha_mask_with_grabcut(image_path, crop_size=(300, 300))
