import glob
import os
import moviepy.video.io.ImageSequenceClip

image_folder = '/Users/tanveerhannan/Downloads/grattvis_vis'
images = []
for i in range(1,5):
    print(i)
    for img in sorted(glob.glob(f"{image_folder}/vis{i}/*.jpg")):
        images.append(os.path.join(image_folder,img))


video_name = '/Users/tanveerhannan/Downloads/grattvis_vis/global.avi'
import os
import cv2

dir_path = os.getcwd()
shape = 640, 480
fps = 5

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
video = cv2.VideoWriter(video_name, fourcc, fps, shape)

for image in images:
    image_path = os.path.join(dir_path, image)
    image = cv2.imread(image_path)
    resized=cv2.resize(image,shape)
    video.write(resized)

video.release()