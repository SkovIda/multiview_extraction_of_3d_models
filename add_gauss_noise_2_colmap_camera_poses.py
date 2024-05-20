import os
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection

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
    ax2.set_title(fig_title)
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
    dataset_basedir = '/home/ida/jupyter_notebooks/project_in_advanced_robotics/multiview_extraction_of_3d_models/data/thermostat_p2_high_light_perfect/'
    load_filename = 'poses_bounds.npy'
    # colmap_poses_bounds = np.load(dataset_basedir + load_filename)
    # print(colmap_poses_bounds.shape)

    ##### SOURCE: LLFF/llff/pose_utils.py:
    poses_arr = np.load(os.path.join(dataset_basedir, load_filename))
    poses = poses_arr[:, :-2].reshape([-1, 3, 5]).transpose([1,2,0])
    bds = poses_arr[:, -2:].transpose([1,0])
    ##### END CITE
    print(f'Loaded file: {dataset_basedir + load_filename}')

    ################################################
    # Visualize camera poses and estimated trajectory:
    camera_poses = []
    for pose_i in range(poses.shape[-1]):
        transform = np.concatenate((poses[:,0:4,pose_i], np.array([[0,0,0,1]])), axis=0)
        camera_poses.append(poses[:,0:4,pose_i])

    # Show original camera poses:
    visualise_camera_poses(poses, fig_title='no noise')

    ##### TODO: Add gaussian noise to the affine transformaiton matrix:
    affine_cam_transforms = poses[:,0:4,:]
    print(f'affine_cam_transforms.shape:\t{affine_cam_transforms.shape}')

    # Generate
    mu = 0.0
    sigma = 0.05
    # gauss_noise = np.random.default_rng().normal(mu, sigma, size=(3,1, poses.shape[-1]))
    gauss_noise = np.random.default_rng().normal(mu, sigma, size=(3, poses.shape[-1]))
    # print(f'gauss_noise.shape:\t{gauss_noise.shape}')

    affine_cam_transforms_noisy = np.zeros((3,4,poses.shape[-1]))
    # print(affine_cam_transforms_noisy[:,3,:].shape)
    affine_cam_transforms_noisy[:,-1,:] = gauss_noise
    
    # visualise_camera_poses(affine_cam_transforms, fig_title='no noise')
    # visualise_camera_poses(affine_cam_transforms_noisy, fig_title=f'noise: mu={mu}, sigma={sigma}')
    # plt.show()

    poses_bounds_noise = poses

    poses_bounds_noise[:, 0:4, :] += affine_cam_transforms_noisy

    poses_bounds_noise_arr = poses_arr
    poses_bounds_noise_arr[:,0:15] = poses_bounds_noise.transpose([2,0,1]).reshape([poses_arr.shape[0], 15])

    save_filename = load_filename + '_gauss_noise_mu0_sigma05'

    np.save(dataset_basedir + save_filename, poses_bounds_noise_arr)

    print(f'Saved noisy camera poses to file: {dataset_basedir + save_filename}')
    
    ##### Verify noise was generated correctly:
    # Extract camera pose from noisy poses_bounds.npy:
    # dataset_basedir = '/home/ida/jupyter_notebooks/project_in_advanced_robotics/multiview_extraction_of_3d_models/data/thermostat_p2_high_light_perfect/'

    ##### SOURCE: LLFF/llff/pose_utils.py:
    poses_arr = np.load(os.path.join(dataset_basedir, save_filename + '.npy'))
    poses = poses_arr[:, :-2].reshape([-1, 3, 5]).transpose([1,2,0])
    bds = poses_arr[:, -2:].transpose([1,0])
    ##### END CITE
    print(f'Loaded file: {dataset_basedir + save_filename}')

    # Show camera poses with added gauss noise before and after save::
    visualise_camera_poses(poses_bounds_noise, fig_title=f'noise: mu={mu}, sigma={sigma}')
    visualise_camera_poses(poses, fig_title=f'reload noise: mu={mu}, sigma={sigma}')
    plt.show()