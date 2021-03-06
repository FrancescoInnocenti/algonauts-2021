"""
This script evaluates an encoding model built from the features of a pretrained
PredNet on a held-out, validation set of fMRI responses in 9 visual regions
across all 10 subjects.
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from load_prednet import load_prednet
from extract_features import extract_activations, apply_pca
from algonauts.utils import perform_encoding


model_dir = '/Algonauts_2021_Models/prednet/model_data_keras2/'
video_dir = '/Algonauts_2021_Models/AlgonautsVideos268_All_30fpsmax'
fmri_dir = '/Algonauts_2021_Models/participants_data_v2021/mini_track'
results_dir = "/Algonauts_2021_Models/prednet/fmri_predictions"

prednet = load_prednet(model_dir)
video_list = glob.glob(video_dir + '/*.mp4')
video_list.sort()
n_train_videos = 1000
train_activations = extract_activations(prednet, video_list[:n_train_videos])
train_features = apply_pca(train_activations)

subs = ["sub01", "sub02", "sub03", "sub04", "sub05", "sub06", "sub07", "sub08", "sub09", "sub10"]
ROIs = ["V1", "V2", "V3", "V4", "LOC", "EBA", "FFA", "STS", "PPA"]
voxelwise_corrs = np.zeros((len(subs), len(ROIs)))
for i, sub in enumerate(subs):
    for j, ROI in enumerate(ROIs):
        voxelwise_corrs[i, j] = perform_encoding(train_features,
                                                 fmri_dir,
                                                 sub=sub,
                                                 ROI=ROI)

np.save(results_dir, voxelwise_corrs)

# mean and std correlation across subjects
subjs_mean = np.mean(voxelwise_corrs, axis=0)
subjs_std = np.std(voxelwise_corrs, axis=0)

# plot results
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(ROIs, subjs_mean, color='blue', alpha=0.5)
ax.errorbar(x=ROIs, y=subjs_mean, yerr=subjs_std, linestyle='', elinewidth=1, capsize=6, color='k')
ax.set_title('Layer 4', fontsize=30, fontweight='bold', pad=35)
ax.set_xlabel("Region of interest", fontsize=25, labelpad=30)
ax.set_ylabel("Correlation", fontsize=25, labelpad=30)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
