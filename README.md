# Set up a virtualenv to avoid system packages messing with this
```
virtualenv piar
source piar/bin/activate
pip install -r requirements.txt
```

## create a jupyter kernel for this project
```ipython kernel install --user --name=piar```

Remember to add the kernel path to jupyter notebook configurations or extensions
- Add fully qualified path e.g.: `/home/ida/.local/share/jupyter/kernels/piar/kernel.json`


# Install pypylon
Install pypylon as described on https://github.com/basler/pypylon
1. Download `pylon` from the Basler website: https://www.baslerweb.com/en/software/pylon/
1. Install pylon as described in section `Installation using tar.gz files` in the `INSTALL` file located in `./pylon-*_setup.tar.gz`
1. Check pypylon installation: run the following in terminal to ensure `pypylon` has been correctly installed
    ```
    source piar/bin/activate
    pip install -r requirements.txt
    ```

## Setup camera
add udev rule
`sudo cp 69-basler-cameras.rules /etc/udev/rules.d/`
reload udev rules
`sudo udevadm control --reload-rules`
reconnect camera

### Setup camera with `./setup-usb.sh`
Set up the correct udev rules, execute: `./setup-usb.sh` from within the directory `./pylon_setup/share/pylon/`

<!-- If the camera is not found during enumeration, follow instructions in `./pylon_setup/share/pylon/README`  -->

## Check pypylon installation:
Check `pypylon` installation:
1. source the virtual environment: `source piar/bin/activate`
1. ensure `pypylon` has been correctly installed:
    ```
    source piar/bin/activate
    pip install -r requirements.txt
    ```
1. connect camera to pc with usb cable
1. Verify camera connection: run `python3 camera_basler_ace/pypylon_lib_test.py` from project root dir


# Control camera position with an Arudino UNO
1. install `Platform IO` extension for visual studio code and use it to open the arduino project located in `arduino_ws/arduino_accelstepper_pyserial_read_write/`
1. connect arduino to pc with usb cable
1. build and upload the arduino program to the Arduino UNO
1. verify control of stepper motor with arduino via serial communication by running the following commands from root of this directory: run
    ```
    source piar/bin/activate
    python3 arduino_serial/arduino_serial_read_write.py
    ```

# Acquire image dataset
1. connect camera to pc with usb cable
1. connect stepper motor to power source
1. connect arduino to pc with usb cable
1. generate dataset: run (project root dir):
    ```
    source piar/bin/activate
    ./gen_img_data.py
    ```
