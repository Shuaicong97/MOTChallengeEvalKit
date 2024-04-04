import os
import data_processing as dp


def check_file_exist(folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    return os.path.exists(file_path)


def find_corresponding_image(img_folder, first_col_value, res_file, current_line_index):
    img_file = f'img_{first_col_value:07d}.jpg'
    while not check_file_exist(img_folder, img_file):
        current_line_index += 1
        if current_line_index >= len(res_file):
            return None, None
        first_col_value = int(res_file[current_line_index][0])
        img_file = f'img_{first_col_value:07d}.jpg'
    return first_col_value, current_line_index


def main(root):
    folders = os.listdir(root)
    folders.sort()
    result = []
    for folder in folders:
        if not folder.startswith('.'):
            file_path = f"{root}/{folder}/gt/{folder}.txt"
            res_file = dp.load(file_path)
            first_occurrences = {}
            current_line_index = 0

            while current_line_index < len(res_file):
                line = res_file[current_line_index]
                first_col_value = int(line[0])
                second_col_value = int(line[1])
                score = line[6]

                if second_col_value not in first_occurrences:
                    img_folder = os.path.join(root_folder, folder, 'img1')
                    first_col_value, current_line_index = find_corresponding_image(img_folder, first_col_value,
                                                                                   res_file, current_line_index)
                    if first_col_value is None:
                        break
                    first_occurrences[second_col_value] = {"frame_id": first_col_value, "score": score}

                current_line_index += 1

            result.append({"video": folder, "first_occurrences": first_occurrences})
    # <class 'list'>
    return result


if __name__ == "__main__":
    root_folder = 'ovis/ovis'
    main(root_folder)
