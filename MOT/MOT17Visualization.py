from Visualize import Visualizer
import glob
import os
import cv2
import numpy as np
import math


class MOTVisualizer(Visualizer):

    def load(self, FilePath):
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

    def drawResults(self, im=None, t=0):
        self.draw_boxes = False

        maxConf = 1
        if self.mode == "det":
            maxConf = max(self.resFile[:, 6])

        # boxes in this frame
        thisF = np.flatnonzero(self.resFile[:, 0] == t)

        for bb in thisF:
            targetID = self.resFile[bb, 1]
            IDstr = "%d" % targetID
            left = ((self.resFile[bb, 2] - 1) * self.imScale).astype(int)
            top = ((self.resFile[bb, 3] - 1) * self.imScale).astype(int)
            width = ((self.resFile[bb, 4]) * self.imScale).astype(int)
            height = ((self.resFile[bb, 5]) * self.imScale).astype(int)

            left = ((self.resFile[bb, 2] - 1)).astype(int)
            top = ((self.resFile[bb, 3] - 1)).astype(int)
            width = ((self.resFile[bb, 4])).astype(int)
            height = ((self.resFile[bb, 5])).astype(int)

            # normalize confidence to [0,5]
            rawConf = self.resFile[bb, 6]
            conf = (rawConf) / maxConf
            conf = int(conf * 5)

            pt1 = (left, top)
            pt2 = (left + width, top + height)

            color = self.colors[int(targetID % len(self.colors))]
            color = tuple([int(c * 255) for c in color])

            if self.mode == "gt":
                label = self.resFile[bb, 7]
            else:
                label = 1

            # occluder
            if ((self.mode == "gt") & (self.showOccluder) & (int(label) in [9, 10, 11, 13])):

                overlay = im.copy()
                alpha = 0.7
                color = (0.7 * 255, 0.7 * 255, 0.7 * 255)
                cv2.rectangle(overlay, pt1, pt2, color, -1)
                im = cv2.addWeighted(overlay, alpha, im, 1 - alpha, 0)

            else:
                cv2.rectangle(im, pt1, pt2, color, 2)
                if not self.mode == "det":
                    cv2.putText(im, IDstr, pt1, cv2.FONT_HERSHEY_SIMPLEX, 2, color=color, thickness=3)

        return im

    def drawSingleObject(self, im=None, key=None, value=None):
        self.draw_boxes = False
        maxConf = 1
        if self.mode == "det":
            maxConf = max(self.resFile[:, 6])

        # boxes in this frame
        thisF = np.flatnonzero((self.resFile[:, 0] == value) & (self.resFile[:, 1] == key))

        # only one element
        for bb in thisF:
            targetID = self.resFile[bb, 1]
            IDstr = "%d" % targetID
            left = ((self.resFile[bb, 2] - 1) * self.imScale).astype(int)
            top = ((self.resFile[bb, 3] - 1) * self.imScale).astype(int)
            width = ((self.resFile[bb, 4]) * self.imScale).astype(int)
            height = ((self.resFile[bb, 5]) * self.imScale).astype(int)

            left = ((self.resFile[bb, 2] - 1)).astype(int)
            top = ((self.resFile[bb, 3] - 1)).astype(int)
            width = ((self.resFile[bb, 4])).astype(int)
            height = ((self.resFile[bb, 5])).astype(int)

            # normalize confidence to [0,5]
            rawConf = self.resFile[bb, 6]
            conf = (rawConf) / maxConf
            conf = int(conf * 5)

            pt1 = (left, top)
            pt2 = (left + width, top + height)
            pt3 = (left, top + height)

            color = self.colors[int(targetID % len(self.colors))]
        color = tuple([int(c * 255) for c in color])

        if self.mode == "gt":
            label = self.resFile[bb, 7]
        else:
            label = 1

        # occluder
        if ((self.mode == "gt") & (self.showOccluder) & (int(label) in [9, 10, 11, 13])):
            overlay = im.copy()
            alpha = 0.7
            color = (0.7 * 255, 0.7 * 255, 0.7 * 255)
            cv2.rectangle(overlay, pt1, pt2, color, -1)
            im = cv2.addWeighted(overlay, alpha, im, 1 - alpha, 0)
        else:
            cv2.rectangle(im, pt1, pt2, color, 2)
            if not self.mode == "det":
                if top < 30:
                    cv2.putText(im, IDstr, pt3, cv2.FONT_HERSHEY_SIMPLEX, 2, color=color, thickness=3)
                else:
                    cv2.putText(im, IDstr, pt1, cv2.FONT_HERSHEY_SIMPLEX, 2, color=color, thickness=3)

        return im


if __name__ == "__main__":
    path = '/Users/shuaicongwu/Documents/study/Master/MA/MOTChallengeEvalKit/ovis/ovis'
    folders = next(os.walk(path))[1]
    folders.sort()
    for folder in folders:
        visualizer = MOTVisualizer(
            seqName=folder,
            FilePath=f"{path}/{folder}/gt/{folder}.txt",
            image_dir=f"{path}/{folder}/img1",
            mode="gt",
            output_dir=f"{path}/{folder}")

        visualizer.generateVideo(
            displayTime=True,
            displayName="traj",
            showOccluder=True,
            fps=25)
        resFile = visualizer.resFile
        unique_ids = np.unique(visualizer.resFile.T[1])
        visualizer.loadFile = False
    # n_box = 15
    # for i in range(math.ceil(len(unique_ids)/n_box)):
    # 	ids = unique_ids[i*n_box:i*n_box+n_box]
    # 	visualizer.resFile = resFile[[v in ids for v in resFile.T[1]]]
    # 	visualizer.seqName = f"{folder}_{ids[0]}_{ids[-1]}"
    # 	visualizer.generateVideo(
    # 		displayTime=True,
    # 		displayName="traj",
    # 		showOccluder=True,
    # 		fps=25)
    # 	print()
