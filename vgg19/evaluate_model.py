"""
This script evaluates an encoding model built from the features of a pretrained
VGG19 layer on a held-out, validation set of fMRI responses in 9 visual regions
across all 10 subjects.
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from load_vgg19 import load_vgg19
from extract_features import extract_activations, apply_pca
from algonauts.utils import perform_encoding


vgg19_url = 'https://download.pytorch.org/models/vgg19-dcbb9e9d.pth'
video_dir = '/Algonauts_2021_Models/AlgonautsVideos268_All_30fpsmax'
activations_dir = "/Algonauts_2021_Models/vgg19/activations"
pca_dir = '/Algonauts_2021_Models/vgg19/pca_activations'
fmri_dir = '/Algonauts_2021_Models/participants_data_v2021/mini_track'
results_dir = '/Algonauts_2021_Models/vgg19/fmri_predictions'

vgg19 = load_vgg19(vgg19_url)
video_list = glob.glob(video_dir + '/*.mp4')
video_list.sort()
n_train_videos = 1000
layer = 'layer_16'
extract_activations(vgg19, video_list[:n_train_videos], activations_dir, layer)
apply_pca(activations_dir, pca_dir, layer)

subs = ["sub01", "sub02", "sub03", "sub04", "sub05", "sub06", "sub07","sub08", "sub09", "sub10"]
ROIs = ["V1", "V2", "V3", "V4", "LOC", "EBA", "FFA", "STS", "PPA"]
voxelwise_corrs = np.zeros((len(subs), len(ROIs)))
for i, sub in enumerate(subs):
    for j, ROI in enumerate(ROIs):
        voxelwise_corrs[i, j] = perform_encoding(pca_dir,
                                                 fmri_dir,
                                                 sub=sub,
                                                 ROI=ROI)

np.save(results_dir, voxelwise_corrs)

# mean and std correlation across subjects
subjs_mean = np.mean(voxelwise_corrs, axis=0)
subjs_std = np.std(voxelwise_corrs, axis=0)

# plot results
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(ROIs, subjs_mean, color='red', alpha=0.5)
ax.errorbar(x=ROIs, y=subjs_mean, yerr=subjs_std, linestyle='', elinewidth=1, capsize=6, color='k')
ax.set_title('Layer 16', fontsize=30, fontweight='bold', pad=35)
ax.set_xlabel("Region of interest", fontsize=25, labelpad=30)
ax.set_ylabel("Correlation", fontsize=25, labelpad=30)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
