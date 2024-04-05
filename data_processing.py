import os
import shutil
import numpy as np


def move_imgs_to_img1():
    base_dir = 'ovis/ovis/'

    # get all sub folders in valid
    subfolders = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]
    print(f'{type(subfolders)}: {subfolders}')

    folder_name_list = []

    for folder_name in subfolders:
        folder_name_list.append(folder_name)

        img_folder_path = os.path.join(base_dir, folder_name, 'img1')
        os.makedirs(img_folder_path, exist_ok=True)

        jpg_files = [file for file in os.listdir(os.path.join(base_dir, folder_name)) if file.endswith('.jpg')]

        for jpg_file in jpg_files:
            old_file_path = os.path.join(base_dir, folder_name, jpg_file)
            new_file_path = os.path.join(img_folder_path, jpg_file)
            shutil.move(old_file_path, new_file_path)

    print('processing completes!')


def move_gts_to_gt():
    valid_dir = 'ovis/ovis/'
    gt_dir = 'ovis/dvis_ovis_video_gt/'

    # create gt folder for every sub folder in valid
    for folder_name in os.listdir(valid_dir):
        if not folder_name.startswith('.'):
            folder_path = os.path.join(valid_dir, folder_name)
            gt_folder_path = os.path.join(folder_path, 'gt')
            os.makedirs(gt_folder_path, exist_ok=True)

    for txt_file in os.listdir(gt_dir):
        # get filename of txt file
        txt_filename = os.path.splitext(txt_file)[0]

        for folder_name in os.listdir(valid_dir):
            if not folder_name.startswith('.'):
                if txt_filename == folder_name:
                    src_file_path = os.path.join(gt_dir, txt_file)
                    dest_folder_path = os.path.join(valid_dir, folder_name, 'gt')
                    shutil.move(src_file_path, dest_folder_path)

    print('processing completes!')


def handle_frame_names_from_1():
    base_dir = 'ovis/ovis/'

    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        img1_folder_path = os.path.join(folder_path, 'img1')

        if os.path.isdir(img1_folder_path) and folder_name == 'cfff47c3':
            jpg_files = sorted([file for file in os.listdir(img1_folder_path) if file.endswith('.jpg')])
            print(jpg_files)
            first_img_index = int(jpg_files[0].split('_')[-1].split('.')[0])

            if first_img_index != 1:
                # rename filename from img_0000001.jpg
                for i, jpg_file in enumerate(jpg_files):
                    new_index = i + 1
                    new_file_name = f'img_{str(new_index).zfill(7)}.jpg'
                    old_file_path = os.path.join(img1_folder_path, jpg_file)
                    new_file_path = os.path.join(img1_folder_path, new_file_name)
                    os.rename(old_file_path, new_file_path)
                    print(f'{i}: {old_file_path}, {new_file_path}')

    print('processing completes!')


def load(FilePath):
    data = np.genfromtxt(FilePath, delimiter=',')
    if data.ndim == 1:  # Because in MOT we have different delimites in result files?!?!?!?!?!?
        data = np.genfromtxt(FilePath, delimiter=' ')
    if data.ndim == 1:  # Because
        print("Ooops, cant parse %s, skipping this one ... " % FilePath)

        return None
    # clean nan from results
    # data = data[~np.isnan(data)]
    nan_index = np.sum(np.isnan(data), axis=1)
    data = data[nan_index == 0]
    return data


def get_first_occurrences():
    path = '/Users/shuaicongwu/Documents/study/Master/MA/MOTChallengeEvalKit/ovis/ovis'
    folders = os.listdir(path)
    folders.sort()
    result = []
    for folder in folders:
        if not folder.startswith('.'):
            file_path = f"{path}/{folder}/gt/{folder}.txt"
            res_file = load(file_path)
            # 初始化一个空字典来存储第二列第一次出现时对应的第一列的数值
            first_occurrences = {}

            # 迭代self.resFile数组
            for line in res_file:
                # 提取第一列和第二列的值
                first_col_value = int(line[0])
                second_col_value = int(line[1])
                score = line[6]

                # 如果第二列的值还没有在字典中出现过，将第一列的值记录到字典中
                if second_col_value not in first_occurrences:
                    first_occurrences[second_col_value] = {"frame_id": first_col_value, "score": score}

            result.append({"video": folder, "first_occurrences": first_occurrences})
            # 打印结果
            # print('当前video是', folder)
            # for key, value in first_occurrences.items():
            #     print("第二列第一次出现", key, "时，第一列是", value)

    return result


def print_jpg():
    base_dir = 'ovis/ovis'
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)

        # 检查路径是否为文件夹
        if os.path.isdir(folder_path):
            print(f"文件夹: {folder_path}")

            # 遍历文件夹中的文件
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)

                # 检查文件是否为 JPG 文件
                if file.lower().endswith('.jpg'):
                    print(f"  JPG 文件: {file_path}")
                    # os.remove(file_path)


# print_jpg()

