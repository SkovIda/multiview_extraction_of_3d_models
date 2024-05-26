# import json
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from mpl_toolkits import mplot3d
import numpy as np


def visualise_camera_poses(poses, fig_title='Camera Frames'):
    ########################################
    # Visualize camera poses
    fig2 = plt.figure(figsize=(10, 8))
    # fig2 = plt.figure()
    ax2 = fig2.add_subplot(111, projection='3d')

    axis_scale = 0.9
    
    # for pose in camera_poses:
    for pose_i in range(poses.shape[-1]):
        pose = np.concatenate((poses[:,0:4,pose_i], np.array([[0,0,0,1]])), axis=0)
        # pose = poses[:,:,pose_i]#np.concatenate((poses[:,:,pose_i], np.array([[0,0,0,1]])), axis=0)
        start = pose[:3, 3]
        # Create unit vectors for camera orientation (assuming the rotation matrix is properly aligned)
        end_x = start + pose[:3, 0] * axis_scale #1  # X-axis direction (scaled for visualization)
        end_y = start + pose[:3, 1] * axis_scale #1  # Y-axis direction (scaled for visualization)
        end_z = start + pose[:3, 2] * axis_scale #1  # Z-axis direction (scaled for visualization)
        
        # Draw the arrows
        ax2.quiver(*start, *(end_x - start), color='r', length=np.linalg.norm(end_x - start), arrow_length_ratio=0.3)
        ax2.quiver(*start, *(end_y - start), color='g', length=np.linalg.norm(end_y - start), arrow_length_ratio=0.3)
        ax2.quiver(*start, *(end_z - start), color='b', length=np.linalg.norm(end_z - start), arrow_length_ratio=0.3)

    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')

    ax2.axis('equal')
    
    left_xz = -5.0
    right_xz = 5.0
    left_y = -4.0
    right_y = 4.0
    ax2.set_xlim(left_xz, right_xz)
    ax2.set_ylim(left_y, right_y)
    ax2.set_zlim(left_xz, right_xz)

    # ax2.view_init(elev=-160, azim=45, roll=0, vertical_axis='y')
    ax2.view_init(elev=-160, azim=00, roll=0, vertical_axis='y')
    # ax2.set_title(fig_title)
    ax2.legend()

    # plt.show()
    return

def visualize_estimated_trajectory(camera_poses):
    fig1 = plt.figure(figsize=(10, 8))
    ax1 = fig1.add_subplot(111, projection='3d')

    # Extract camera positions
    camera_positions = [pose[:3, 3] for pose in camera_poses]

    # Plot camera positions
    ax1.scatter(*zip(*camera_positions), c='r', marker='o', label='Camera Poses')

    # Connect camera positions with lines
    lines = []
    for i in range(len(camera_positions) - 1):
        lines.append([camera_positions[i], camera_positions[i + 1]])

    # Create a line collection
    lc = Line3DCollection(lines, colors='b', linewidths=1, label='Camera Trajectory')
    ax1.add_collection3d(lc)

    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('Camera Poses and trajectory')
    ax1.legend()

    plt.show()

if __name__ == '__main__':
    ##### Extract camera pose from poses_bounds.npy:
    dataset_basedir_estimated = '/home/ida/jupyter_notebooks/project_in_advanced_robotics/multiview_extraction_of_3d_models/results/b18-goodmask-newdataset/imgscaled_410x660/'
    dataset_basedir_noisy_sigma005 = '/home/ida/jupyter_notebooks/project_in_advanced_robotics/multiview_extraction_of_3d_models/results/b18-goodmask-noisypose-newdataset/imgscaled_410x660 _fkedpose/'
    dataset_basedir_noisy_sigma01 = '/home/ida/jupyter_notebooks/project_in_advanced_robotics/multiview_extraction_of_3d_models/results/Thermo_b18_GOODMASK_410x660_0.1sigma/'

    load_filename = 'poses_bounds.npy'
    # colmap_poses_bounds = np.load(dataset_basedir + load_filename)
    # print(colmap_poses_bounds.shape)

    camera_3d_points = []
    camera_3d_points_noisy_sigma005 = []
    camera_3d_points_noisy_sigma01 = []

    ##### Visualize Camera poses estimated with COLMAP:
    ##### SOURCE: LLFF/llff/pose_utils.py:
    poses_arr = np.load(os.path.join(dataset_basedir_estimated, load_filename))
    poses = poses_arr[:, :-2].reshape([-1, 3, 5]).transpose([1,2,0])
    # bds = poses_arr[:, -2:].transpose([1,0])
    ##### END CITE
    print(f'Loaded file: {dataset_basedir_estimated + load_filename}')

    visualise_camera_poses(poses, fig_title='no noise')

    # save the camera positions estimated with COLMAP:
    for pose_i in range(poses.shape[-1]):
        transform = np.concatenate((poses[:,0:4,pose_i], np.array([[0,0,0,1]])), axis=0)
        #camera_poses.append(poses[:,0:4,pose_i])
        camera_3d_points.append(poses[:,0:4,pose_i])

    ##### Visualize Noisy Camera poses: sigme=0.05 [dm]
    ##### SOURCE: LLFF/llff/pose_utils.py:
    poses_arr = np.load(os.path.join(dataset_basedir_noisy_sigma005, load_filename))
    poses = poses_arr[:, :-2].reshape([-1, 3, 5]).transpose([1,2,0])
    # bds = poses_arr[:, -2:].transpose([1,0])
    ##### END CITE
    print(f'Loaded file: {dataset_basedir_noisy_sigma005 + load_filename}')

    # Show original camera poses:
    mu = 0.0
    sigma = 0.05
    visualise_camera_poses(poses, fig_title=f'noise: mu={mu}, sigma={sigma}')

    # plt.show()

    # # Visualize camera poses and estimated trajectory:
    # camera_poses = []
    # for pose_i in range(poses.shape[-1]):
    #     transform = np.concatenate((poses[:,0:4,pose_i], np.array([[0,0,0,1]])), axis=0)
    #     camera_poses.append(poses[:,0:4,pose_i])
    
    # save the camera positions with added noise to the position: sigma=0.05
    for pose_i in range(poses.shape[-1]):
        transform = np.concatenate((poses[:,0:4,pose_i], np.array([[0,0,0,1]])), axis=0)
        #camera_poses.append(poses[:,0:4,pose_i])
        camera_3d_points_noisy_sigma005.append(poses[:,0:4,pose_i])


    ##### Visualize Noisy Camera poses: sigme=0.1 [dm]
    ##### SOURCE: LLFF/llff/pose_utils.py:
    poses_arr = np.load(os.path.join(dataset_basedir_noisy_sigma01, load_filename))
    poses = poses_arr[:, :-2].reshape([-1, 3, 5]).transpose([1,2,0])
    # bds = poses_arr[:, -2:].transpose([1,0])
    ##### END CITE
    print(f'Loaded file: {dataset_basedir_noisy_sigma01 + load_filename}')

    # Show the noisy camera poses: sigma = 0.1
    mu = 0.0
    sigma = 0.05
    visualise_camera_poses(poses, fig_title=f'noise: mu={mu}, sigma={sigma}')
    # save the camera positions with added noise to the position: sigma=0.05
    for pose_i in range(poses.shape[-1]):
        transform = np.concatenate((poses[:,0:4,pose_i], np.array([[0,0,0,1]])), axis=0)
        #camera_poses.append(poses[:,0:4,pose_i])
        camera_3d_points_noisy_sigma01.append(poses[:,0:4,pose_i])

    
    ##### Plot the estimated camera positions together with the noisy ones:
    fig3 = plt.figure(figsize=(10, 8))
    ax3 = fig3.add_subplot(111, projection='3d')

    # Extract camera positions
    camera_positions = [pose[:3, 3] for pose in camera_3d_points]
    # Extract camera positions: sigma=0.05
    camera_positions_noisy_sigma005 = [pose[:3, 3] for pose in camera_3d_points_noisy_sigma005]

    # Extract camera positions: sigma=0.1
    camera_positions_noisy_sigma01 = [pose[:3, 3] for pose in camera_3d_points_noisy_sigma01]

    # Plot camera positions
    ax3.scatter(*zip(*camera_positions), c='b', marker='o', label='estimated camera position')
    ax3.scatter(*zip(*camera_positions_noisy_sigma005), c='r', marker='x', label='camera positions with gaussian noise: mu=0, sigma=0.05')
    ax3.scatter(*zip(*camera_positions_noisy_sigma01), c='g', marker='+', label='camera positions with gaussian noise: mu=0, sigma=0.1')

    # # Connect camera positions with lines
    # lines = []
    # for i in range(len(camera_positions) - 1):
    #     lines.append([camera_positions[i], camera_positions[i + 1]])

    # # Create a line collection
    # lc = Line3DCollection(lines, colors='b', linewidths=1, label='Camera Trajectory')
    # ax1.add_collection3d(lc)

    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')
    ax3.view_init(elev=-160, azim=00, roll=0, vertical_axis='y')
    
    ax3.axis('equal')
    left_xz = -5.0
    right_xz = 5.0
    left_y = -4.0
    right_y = 4.0
    ax3.set_xlim(left_xz, right_xz)
    ax3.set_ylim(left_y, right_y)
    ax3.set_zlim(left_xz, right_xz)

    # ax3.set_title('Camera Poses')
    ax3.legend()


    ################### Number of images test:
    dataset_basedir_img = '/home/ida/jupyter_notebooks/project_in_advanced_robotics/multiview_extraction_of_3d_models/number_imgs_test_cam_poses'
    load_filename_60 = 'poses_bounds_60_imgs.npy'
    load_filename_120 = 'poses_bounds_120_imgs.npy'
    load_filename_160 = 'poses_bounds_160_imgs.npy'

    ##### Visualize Camera poses estimated with COLMAP:

    ##### SOURCE: LLFF/llff/pose_utils.py:
    poses_arr = np.load(os.path.join(dataset_basedir_img, load_filename_60))
    poses = poses_arr[:, :-2].reshape([-1, 3, 5]).transpose([1,2,0])
    ##### END CITE
    print(f'Loaded file: {dataset_basedir_img + load_filename_60}')

    visualise_camera_poses(poses, fig_title='60 imgs')

    ##### SOURCE: LLFF/llff/pose_utils.py:
    poses_arr = np.load(os.path.join(dataset_basedir_img, load_filename_120))
    poses = poses_arr[:, :-2].reshape([-1, 3, 5]).transpose([1,2,0])
    ##### END CITE
    print(f'Loaded file: {dataset_basedir_img + load_filename_120}')

    visualise_camera_poses(poses, fig_title='120 imgs')

    ##### SOURCE: LLFF/llff/pose_utils.py:
    poses_arr = np.load(os.path.join(dataset_basedir_img, load_filename_160))
    poses = poses_arr[:, :-2].reshape([-1, 3, 5]).transpose([1,2,0])
    ##### END CITE
    print(f'Loaded file: {dataset_basedir_img + load_filename_160}')

    visualise_camera_poses(poses, fig_title='120 imgs')

    plt.show()

