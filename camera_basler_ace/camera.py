from pypylon import pylon
import cv2
from pathlib import Path

class Camera:
    def __init__(self):
        self.tlf = pylon.TlFactory.GetInstance()
        self.camera = pylon.InstantCamera(self.tlf.CreateFirstDevice())
        self.camera.Open()
    
    def grab_imgs(self, nr_imgs=20, imgs_path = './imgs/', imgs_filename_prefix = 'img_', imgs_filename_postfix = '.png'):
        # path to image folder
        self.imgs_path = imgs_path
        self.imgs_filename_prefix = imgs_filename_prefix
        self.imgs_filename_postfix = imgs_filename_postfix

        Path(imgs_path).mkdir(exist_ok=True)

        # Grab nr_imgs:
        self.number_of_imgs_to_grab = nr_imgs
        self.camera.StartGrabbingMax(self.number_of_imgs_to_grab)

        # # Grabing Continusely (video) with minimal delay
        # self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        # converting to opencv bgr format
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        # Delay before grabbing next image:
        delay_ms = 100
        
        imgNumber = 0
        n_digits = len(str(self.number_of_imgs_to_grab))
        while self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
                # Access the image data.
                image = self.converter.Convert(grabResult)
                img = image.GetArray()
                # cv2.namedWindow('title', cv2.WINDOW_NORMAL)
                img_filename = imgs_path + imgs_filename_prefix + str(imgNumber).zfill(n_digits) + imgs_filename_postfix
                cv2.imwrite(img_filename, img)
                # print("SizeX: ", grabResult.Width)
                # print("SizeY: ", grabResult.Height)
                # img = grabResult.Array
                # print("Gray value of first pixel: ", img[0, 0])
                # cv2.namedWindow(imgs_prefix + str(imgNumber), cv2.WINDOW_NORMAL)
                # cv2.imshow(imgs_prefix + str(imgNumber), img)
                key = cv2.waitKey(delay_ms)
                # if key == 27:   # 27 is "Esc" key
                #     print(f'Escape key pressed...\nExiting program after saving image #{imgNumber}')
                #     break
                
                imgNumber += 1
                if imgNumber >= self.number_of_imgs_to_grab:
                    break
            grabResult.Release()

        # Release the resource:
        self.camera.StopGrabbing()
        self.camera.Close()
        return
    
    def init_camera_grab(self, n_imgs=10, imgs_path = './imgs/', imgs_filename_prefix = 'img_', imgs_filename_postfix = '.png'):
        # Set path to image folder, and filename of grabbed imgs:
        self.imgs_path = imgs_path
        self.imgs_filename_prefix = imgs_filename_prefix
        self.imgs_filename_postfix = imgs_filename_postfix

        # Create subfolder for images if it does not already exist:
        Path(imgs_path).mkdir(exist_ok=True)

        # # Init grab of max nr_imgs images:
        self.number_of_imgs_to_grab = n_imgs
        # self.camera.StartGrabbingMax(self.number_of_imgs_to_grab)

        # Init grab of latest image:
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        # converting to opencv bgr format
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        # Counter for enumerating the image files in the dataset:
        self.img_number = 0

        # Minimum number of digits needed to enumerate last image in the generated dataset (needed to zero pad smaller numbers in img filename):
        self.n_digits_in_img_filename = len(str(self.number_of_imgs_to_grab))
        return
        
    def grab_next_img(self):
        if self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                # Access the image data.
                image = self.converter.Convert(grabResult)
                img = image.GetArray()
                # cv2.namedWindow('title', cv2.WINDOW_NORMAL)
                img_filename = self.imgs_path + self.imgs_filename_prefix + str(self.img_number).zfill(self.n_digits_in_img_filename) + self.imgs_filename_postfix
                cv2.imwrite(img_filename, img)
                self.img_number += 1

                grabResult.Release()
                if self.img_number >= self.number_of_imgs_to_grab:
                    # Release the resource:
                    self.camera.StopGrabbing()
                    self.camera.Close()
                return (img_filename, img)

            grabResult.Release()
        return None

    
if __name__ == '__main__':
    cam = Camera()
    
    # Delay before grabbing next image:
    delay_ms = 100

    # cam.grab_imgs(n_imgs=10, imgs_path='./test_grabbing_imgs/')

    grab_n_imgs = 5
    cam.init_camera_grab(n_imgs=grab_n_imgs, imgs_path='./test_grabbing_imgs/')

    for i in range(grab_n_imgs):
        grabbed_img = cam.grab_next_img()
        if grabbed_img is not None:
            cv2.namedWindow(grabbed_img[0], cv2.WINDOW_NORMAL)
            cv2.imshow(grabbed_img[0], grabbed_img[1])
            # key = cv2.waitKey(0)      # wait for key before grabbing next image
            key = cv2.waitKey(delay_ms) # wait delay_ms miliseconds before grabbing next image