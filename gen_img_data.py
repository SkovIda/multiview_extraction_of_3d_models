#!/usr/bin/env python3
import time
import cv2

from camera_basler_ace import camera
from arduino_serial.arduino_serial_read_write import SerialArduinoReadWrite

def capture_images(image_dataset_name, n_images_per_full_rotation=20):
    serial_arduino = SerialArduinoReadWrite()
    print('wait for ARDUINO UNO to finish resetting after opening the serial port...')
    time.sleep(2)   # NOTE: SERIAL COMMUNICATION WITH ARDUINO UNO WILL FAIL IF THIS IS REMOVED!!!

    cam = camera.Camera()
    # grab_n_imgs = n_images_per_full_rotation
    answer = input("Enter the number of images in the complete dataset and press Enter: ")
    if str(answer).isdigit():
        grab_n_imgs = int(answer)
    else:
        print("Input is not a number!!! Exiting ...")
    
    n_full_rotations = grab_n_imgs // n_images_per_full_rotation

    # cam.init_camera_grab(n_imgs=grab_n_imgs, imgs_path='./data/' + image_dataset_name + '/images/')
    cam.init_camera_grab(n_imgs=n_full_rotations*n_images_per_full_rotation, imgs_path='./data/' + image_dataset_name + '/images/')

    subsections = n_images_per_full_rotation
    angle_rot_step = int(360 / subsections)

    # cv2.namedWindow(image_dataset_name, cv2.WINDOW_NORMAL)
    delay_ms = 100

    # done_captuing_imgs = False
    answer = None

    

    for cam_angle in range(n_full_rotations):
        for i in range(subsections):
            int_to_send = i * angle_rot_step
            serial_arduino.send_message(int_to_send)

            motor_is_executing_command = True
            while motor_is_executing_command:
                read = serial_arduino.get_message()
                if read is not None:
                    print('received msg:',end=' ')
                    print('{!r}'.format(read))
                    motor_is_executing_command = False
                time.sleep(0.01)
            
            grabbed_img = cam.grab_next_img()
            
            if grabbed_img is not None:
                # # cv2.namedWindow(grabbed_img[0], cv2.WINDOW_NORMAL)
                # cv2.imshow(image_dataset_name, grabbed_img[1])
                # # key = cv2.waitKey(0)      # wait for key before grabbing next image
                # key = cv2.waitKey(delay_ms) # wait delay_ms miliseconds before grabbing next image
                # if key == 27:   # 27 is "Esc" key
                #     print(f'Escape key pressed...\nExiting program after saving image to {grabbed_img[0]}')
                #     break
                time.sleep(0.1)
        answer = input("Move camera to new position and press enter to continue: ")
    time.sleep(2)


if __name__=='__main__':
    capture_images(image_dataset_name='test_gen_dataset_2', n_images_per_full_rotation=20)