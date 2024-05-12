import os
import shutil

def remove_imgs_not_accepted_by_colmap(base_dir):
    # base_dir = '/home/ida/jupyter_notebooks/project_in_advanced_robotics/multiview_extraction_of_3d_models/data/test_gen_dataset_2/' #{{ABSOLUTE PATH TO PARENT DIRECTORY}}
    # all_img = [filename for filename in os.listdir(os.path.join(base_dir, 'images'))]
    # print(f'#{len(all_img)} images in initial dataset')
    all_img = os.listdir(os.path.join(base_dir, 'images')) #[filename for filename in os.listdir(os.path.join(base_dir, 'images'))]
    all_mask = os.listdir(os.path.join(base_dir, 'masks')) #[filename for filename in os.listdir(os.path.join(base_dir, 'masks'))]
    print(f'#{len(all_img)} images in initial dataset')

    # print(all_img[1])
    # print(all_mask[1])

    usable_files_list = []
    defect_directory = os.path.join(base_dir, 'unused_images').replace('\\', '/')
    defect_image_directory = os.path.join(defect_directory, 'images').replace('\\', '/')
    defect_mask_directory = os.path.join(defect_directory, 'mask').replace('\\', '/')
    dirs = [defect_directory, defect_image_directory, defect_mask_directory]
    for d in dirs:
        if not os.path.isdir(d):
            os.makedirs(d)
    with open(os.path.join(base_dir, 'view_imgs.txt')) as fp:
        for line in fp:
            usable_files_list.append(line.strip())
    temp_all_img = []
    temp_all_mask = []
    for idx, i in enumerate(all_img):
        # print(f'moving {os.path.join(base_dir, 'images/') + i} to {os.path.join(base_dir, 'unused_images/') + i}')
        if os.path.split(i)[1] not in usable_files_list:
            try:
                shutil.move(os.path.join(base_dir, 'images/') + i, defect_image_directory)
            except shutil.Error:
                os.unlink(os.path.join(base_dir, 'images/' + i))
        else:
            temp_all_img.append(i)
    for idx, i in enumerate(all_mask):
        if os.path.split(i)[1] not in usable_files_list:
            try:
                shutil.move(os.path.join(base_dir, 'masks/') + i, defect_mask_directory)
            except shutil.Error:
                os.unlink(os.path.join(base_dir, 'masks/') + i)
        else:
            temp_all_mask.append(i)
    all_img = temp_all_img
    all_mask = temp_all_mask

    return

if __name__ == '__main__':
    remove_imgs_not_accepted_by_colmap('/home/ida/jupyter_notebooks/project_in_advanced_robotics/multiview_extraction_of_3d_models/data/benchy/')