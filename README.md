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

# Install colmap from source
Install as descrribed here https://colmap.github.io/install.html#linux or follow steps below for building colmap from source on Ubuntu 22.04.

**Note changes when building COLMAP from source on ubuntu 22.04:**
1. Install requirements:
    ```
    sudo apt-get install git cmake build-essential libboost-program-options-dev libboost-filesystem-dev libboost-graph-dev libboost-system-dev libeigen3-dev libflann-dev libfreeimage-dev libmetis-dev libgoogle-glog-dev libgtest-dev libsqlite3-dev libglew-dev qtbase5-dev libqt5opengl5-dev libcgal-dev libceres-dev
    ```
    - To compile with CUDA support, also install Ubuntu’s default CUDA package:
        `sudo apt-get install -y nvidia-cuda-toolkit nvidia-cuda-toolkit-gcc`
    - Install GCC 10 (must compile against GCC 10 on ubuntu 22.04): `sudo apt-get install gcc-10 g++-10`
1. clone colmap repo and make build folder:
    ```
    git clone https://github.com/colmap/colmap.git
    cd colmap
    mkdir build
    cd build
    ```
1. check GPU compute capability is using the command `nvidia-smi --query-gpu=compute_cap --format=csv`
    - Example output:
        ```
        compute_cap
        6.1
        ```
1. then use it in cmake:
    ```
    export CC=/usr/bin/gcc-10
    export CXX=/usr/bin/g++-10
    export CUDAHOSTCXX=/usr/bin/g++-10
    cmake .. -DCMAKE_CUDA_ARCHITECTURES=61
    MAKEFLAGS='-j8 ' cmake --build .
    ```
1. Install colmap: `sudo make install`

# Generate LLFF dataset
1. run in termnal from project root: `python3 colmap2poses.py "data/coil-100/" --colmap_path "/usr/local/bin/colmap"`
    - **NOTE:** run `which colmap` in terminal to get colmap path.

1. **NOTE:** run `gen_nerd_dataset.py` with the absolute path to the root dir of the dataset to remove the images and corresponding masks from the `images/` and `masks/` dirs in the dataset dir.


# Run nvdiffrec on Linux Server through docker
**NOTE:** not tested on server, but running nvdiffrec through docker works
1. get nvdiffrec code from github: `git clone https://github.com/NVlabs/nvdiffrec.git`
1. use secure copy script to get docker image on the server: `scp ./NVDIFFRECRUNDOCKER/start.sh serverhostname:path/to/dataset/destination`
1. clone the dataset from github with HTTPS

Run training example:
1. init docker container with path to nvdiffrec and path to dataset (same dir if using the nvdiffrec datasets): `./start.sh /home/ida/Downloads/git_sources/nvdiffrec  /home/ida/Downloads/git_sources/nvdiffrec`
1. train with bob: `python train.py --config configs/bob.json`

Run training with custom data:
1. use secure copy `scp ./NVDIFFRECRUNDOCKER/start.sh serverhostname:path/to/dataset/destination` to copy required files from local to server:
    1. copy the dataset folder (imgs dir, masks dir, and poses_bounds.npy) into `data/nerd/`
    1. copy the scale_images2.py into `data/nerd/` and run it from nvdiffrec root dir (`nvdiffrec/data/nerd/`). NOTE: make sure the name of the  dataset (i.e., the dir name) matches the name in scale_images2.py
    1. copy the nerd_benchy.json into the `nvdiffrec/configs/` dir
1. **NOTE:** run train.py from root dir with `TMux` or `screen` (if installed on server)

# NOTES:
- make a dataset that can be used with the nvdiffrec code based on this issue https://github.com/NVlabs/nvdiffrec/issues/58
- Improve image matching with colmap:
    `"Colmap takes what images it can map together, try exhaustive mapping or reduce image resolution to avoid some motion blur.
    
    Under absolutely perfect conditions, colmap shouldn't reject any images, but if you're feeding a large unfiltered dataset it's better to spend the extra time in exhaustive mapping to check each image against each other. Changing res or manually using only images with as little movement of the subject/background should help. I also should note interpolation on video to increase the number of images in a dataset doesn't improve the quality of the model even when the interpolated images are added to the set, tried that for NeRFs awhile ago."`