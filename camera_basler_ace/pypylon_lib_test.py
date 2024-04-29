import os
from pathlib import Path

from pypylon import pylon
import cv2

tlf = pylon.TlFactory.GetInstance()
camera = pylon.InstantCamera(tlf.CreateFirstDevice())
camera.Open()

# # demonstrate some feature access
# new_width = camera.Width.Value - camera.Width.Inc
# if new_width >= camera.Width.Min:
#     camera.Width.Value = new_width

numberOfImagesToGrab = 50
camera.StartGrabbingMax(numberOfImagesToGrab)

# Delay before grabbing next image:
delay_ms = 100

# Grabing Continusely (video) with minimal delay
# camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

imgs_path = './camera_basler_ace/test/'
imgs_prefix = imgs_path + 'camera_grab_img_'
imgs_postfix = '.png'

Path(imgs_path).mkdir(exist_ok=True)

imgNumber = 0
n_digits = len(str(numberOfImagesToGrab))
while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data.
        image = converter.Convert(grabResult)
        img = image.GetArray()
        # cv2.namedWindow('title', cv2.WINDOW_NORMAL)
        img_filename = imgs_prefix + str(imgNumber).zfill(n_digits) + imgs_postfix
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
        if imgNumber >= numberOfImagesToGrab:
            break
    grabResult.Release()

# Release the resource:
camera.StopGrabbing()
camera.Close()