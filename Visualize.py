import cv2
import numpy as np
import os, sys
import glob
import colorsys
import traceback
import get_valid_first_index


class Visualizer(object):
    def __init__(self,
                 seqName=None,
                 mode=None,
                 FilePath=None,
                 output_dir=None,
                 image_dir=None,
                 metaInfoDir=None,
                 loadFile=True
                 ):

        assert mode in [None, "raw", "gt"], "Not valid mode. Value has to be None, 'raw', or 'gt'"

        self.seqName = seqName
        self.mode = mode
        self.image_dir = image_dir
        self.output_dir = output_dir
        self.FilePath = FilePath
        self.metaInfoDir = metaInfoDir
        self.loadFile = loadFile

    # adapted from https://github.com/matterport/Mask_RCNN/blob/master/mrcnn/visualize.py
    @property
    def generate_colors(self):
        """
		Generate random colors.
		To get visually distinct colors, generate them in HSV space then
		convert to RGB.
		"""
        N = 30
        brightness = 0.7
        hsv = [(i / N, 1, brightness) for i in range(N)]
        colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
        perm = [15, 13, 25, 12, 19, 8, 22, 24, 29, 17, 28, 20, 2, 27, 11, 26, 21, 4, 3, 18, 9, 5, 14, 1, 16, 0, 23, 7,
                6, 10]
        colors = [colors[idx] for idx in perm]
        return colors

    def generateVideo(self,
                      outputName=None,
                      extensions=[],
                      displayTime=False,
                      displayName=False,
                      showOccluder=False,
                      fps=25):

        self.showOccluder = showOccluder

        if outputName == None:
            outputName = self.seqName

        if not self.mode == "raw" and self.loadFile:
            #load File
            self.resFile = self.load(self.FilePath)

        # get images Folder
        # check if image folder exists
        if not os.path.isdir(self.image_dir):
            print("imgFolder does not exist")
            sys.exit()

        folders = os.listdir(self.image_dir)
        folders.sort()
        folders = [folder for folder in folders if not folder.startswith('.')]
        imgFile = folders[0]
        img = os.path.join(self.image_dir, imgFile)
        print("image file", img)
        im = cv2.imread(img, 1)
        height, width, c = im.shape

        self.imScale = 1
        if width > 800:
            self.imScale = .5
            width = int(width * self.imScale)
            height = int(height * self.imScale)

        # video extension
        extension = ".mp4"
        if self.mode:
            self.outputNameNoExt = os.path.join(self.output_dir, "%s-%s" % (outputName, self.mode))
        else:
            self.outputNameNoExt = os.path.join(self.output_dir, outputName)
        self.outputName = "%s%s" % (self.outputNameNoExt, extension)

        self.out = cv2.VideoWriter(self.outputName, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

        print("Output name: %s" % self.outputName)
        self.colors = self.generate_colors
        t = 0

        for img in sorted(glob.glob(os.path.join(self.image_dir, "*.jpg"))):
            t += 1

            im = cv2.imread(img, 1)

            if not self.mode == "raw":
                try:
                    im = self.drawResults(im, t)
                except Exception as e:
                    print(str(traceback.format_exc()))
            im = cv2.resize(im, (0, 0), fx=self.imScale, fy=self.imScale)

            if displayTime:
                cv2.putText(im, "%d" % t, (25, 50), cv2.FONT_HERSHEY_PLAIN, self.imScale * 6, [0, 0, 0], thickness=3)
            if displayName:
                text = "%s: %s" % (self.seqName, displayName)
                cv2.putText(im, text, (25, height - 25), cv2.FONT_HERSHEY_DUPLEX, self.imScale * 2, [255, 255, 255],
                            thickness=2)

            if t == 1:
                cv2.imwrite("{}.jpg".format(self.outputNameNoExt), im)
                im_mini = cv2.resize(im, (0, 0), fx=0.25, fy=0.25)
                cv2.imwrite("{}-mini.jpg".format(self.outputNameNoExt), im_mini)
            self.out.write(im)
        self.out.release()

        result = get_valid_first_index.main(
            '/Users/shuaicongwu/Documents/study/Master/MA/MOTChallengeEvalKit/ovis/ovis')
        for item in result:
            if item['video'] == self.seqName:
                first_occurrences = item['first_occurrences']
                # key = object_id
                for key, value in first_occurrences.items():
                    filename = "img_{:07d}.jpg".format(value['frame_id'])
                    img = cv2.imread(os.path.join(self.image_dir, filename), 1)

                    if not self.mode == "raw":
                        try:
                            img = self.drawSingleObject(img, key, value['frame_id'])
                        except Exception as e:
                            print(str(traceback.format_exc()))
                    img = cv2.resize(img, (0, 0), fx=self.imScale, fy=self.imScale)

                    if displayTime:
                        cv2.putText(img, "%d" % value['frame_id'], (25, 50), cv2.FONT_HERSHEY_PLAIN, self.imScale * 6, [0, 0, 0],
                                    thickness=3)
                    if displayName:
                        text = "%s: %s" % (self.seqName, displayName)
                        cv2.putText(img, text, (25, height - 25), cv2.FONT_HERSHEY_DUPLEX, self.imScale * 2,
                                    [255, 255, 255], thickness=2)

                    score_formatted = "{:.3f}".format(value['score'])

                    if self.mode:
                        self.outputSingleObjectNoExt = os.path.join(self.output_dir,
                                                                    "%s-%s-%s-%s" % (score_formatted, outputName,
                                                                                     value['frame_id'], key))
                    else:
                        self.outputSingleObjectNoExt = os.path.join(self.output_dir, outputName)

                    cv2.imwrite("{}.jpg".format(self.outputSingleObjectNoExt), img)
                    im_mini = cv2.resize(im, (0, 0), fx=0.25, fy=0.25)
                # cv2.imwrite("{}-mini.jpg".format(self.outputNameNoExt), im_mini)

        print("Finished: %s" % self.outputName)
        if not len(extensions) == 0:
            print("Convert Video to : ", extensions)
            self.convertVideo(extensions)

    def drawResults(self, image=None):
        NotImplemented

    def load(self):
        NotImplemented

    def drawSingleObject(self, image=None, key=None, value=None):
        NotImplemented

    def convertVideo(self, extensions):

        for ext in extensions:
            print(self.outputName)
            outputNameNewExt = "%s%s" % (self.outputNameNoExt, ext)
            print("Convert Video to: %s" % outputNameNewExt)
            command = "ffmpeg -loglevel warning -y -i %s -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libvorbis -cpu-used 8  %s" % (
                self.outputName, outputNameNewExt)
            os.system(command)
