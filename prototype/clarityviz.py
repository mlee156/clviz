#!/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import print_function

__author__ = 'seelviz'

#import matplotlib as mpl
#mpl.use('Agg')

from skimage import data, img_as_float
from skimage import exposure

import plotly
from plotly.graph_objs import *

import cv2

import math, os, gc, random
import numpy as np
import nibabel as nib
import os.path

## Tony's get_brain_figure stuff
#from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
#from plotly import tools
#plotly.offline.init_notebook_mode()
#
import networkx as nx
import pandas as pd
import re

from ndreg import *
import ndio.remote.neurodata as neurodata
from numpy import genfromtxt

import time

def get_image(token, resolution=5):
    return imgDownload(token, resolution=resolution)

def register(token, orientation, resolution=5):
    """ Saves fully registered brain as token + '_reg.nii'."""
    refToken = "ara_ccf2"
    refImg = imgDownload(refToken)

    refAnnoImg = imgDownload(refToken, channel="annotation")

    inImg = imgDownload(token, resolution=resolution)

    # resampling CLARITY image
    inImg = imgResample(inImg, spacing=refImg.GetSpacing())

    # reorienting CLARITY image
    inImg = imgReorient(inImg, orientation, "RSA")

    # Thresholding
    (values, bins) = np.histogram(sitk.GetArrayFromImage(inImg), bins=100, range=(0, 500))

    counts = np.bincount(values)
    maximum = np.argmax(bins)
    # print(maximum)
    # print(counts)

    lowerThreshold = maximum
    upperThreshold = sitk.GetArrayFromImage(inImg).max() + 1

    # print(lowerThreshold)
    # print(upperThreshold)

    inImg = sitk.Threshold(inImg, lowerThreshold, upperThreshold, lowerThreshold) - lowerThreshold

    # Generating CLARITY mask
    (values, bins) = np.histogram(sitk.GetArrayFromImage(inImg), bins=1000)
    cumValues = np.cumsum(values).astype(float)
    cumValues = (cumValues - cumValues.min()) / cumValues.ptp()

    maxIndex = np.argmax(cumValues > 0.95) - 1
    threshold = bins[maxIndex]

    inMask = sitk.BinaryThreshold(inImg, 0, threshold, 1, 0)

    # Affine Transformation
    spacing = [0.25, 0.25, 0.25]
    refImg_ds = imgResample(refImg, spacing=spacing)

    inImg_ds = imgResample(inImg, spacing=spacing)

    inMask_ds = imgResample(inMask, spacing=spacing, useNearest=True)

    affine = imgAffineComposite(inImg_ds, refImg_ds, inMask=inMask_ds, iterations=100, useMI=True, verbose=True)

    inImg_affine = imgApplyAffine(inImg, affine, size=refImg.GetSize())

    inMask_affine = imgApplyAffine(inMask, affine, size=refImg.GetSize(), useNearest=True)

    # LDDMM Registration
    inImg_ds = imgResample(inImg_affine, spacing=spacing)
    inMask_ds = imgResample(inMask_affine, spacing=spacing, useNearest=True)
    (field, invField) = imgMetamorphosisComposite(inImg_ds, refImg_ds, inMask=inMask_ds, alphaList=[0.05, 0.02, 0.01],
                                                  useMI=True, iterations=100, verbose=True)
    inImg_lddmm = imgApplyField(inImg_affine, field, size=refImg.GetSize())
    inMask_lddmm = imgApplyField(inMask_affine, field, size=refImg.GetSize(), useNearest=True)

    # Saving registered image
    location = "img/" + token + "_regis.nii"
    imgWrite(inImg_lddmm, str(location))

    # Saving annotations
    location = "img/" + token + "_anno.nii"
    imgWrite(refAnnoImg, str(location))

    return inImg_lddmm, refAnnoImg

def apply_clahe(input_path):
    """
    input_path is the path to the registered .nii file of the brain.
    Returns the clahe image array.
    """
    im = nib.load(input_path)
    im = im.get_data()

    x_value = im.shape[0]
    y_value = im.shape[1]
    z_value = im.shape[2]

    im_flat = im.reshape(-1)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    cl1 = clahe.apply(im_flat)

    im_clahe = cl1.reshape(x_value, y_value, z_value)

    return im_clahe

def down_sample(inImg):
    """ inImg: The downloaded image object from ndreg."""
    (values, bins) = np.histogram(sitk.GetArrayFromImage(inImg), bins=100, range=(0, 500))
    counts = np.bincount(values)
    maximum = np.argmax(counts)

    lowerThreshold = maximum
    upperThreshold = sitk.GetArrayFromImage(inImg).max() + 1

    inImg = sitk.Threshold(inImg, lowerThreshold, upperThreshold, lowerThreshold) - lowerThreshold
    print
    "applied filtering"
    rawImg = sitk.GetArrayFromImage(inImg)
    xdimensions = len(rawImg[:, 0, 0])
    ydimensions = len(rawImg[0, :, 0])
    zdimensions = len(rawImg[0, 0, :])
    xyz = []
    for i in range(40000):
        value = 0
        while (value == 0):
            xval = random.sample(xrange(0, xdimensions), 1)[0]
            yval = random.sample(xrange(0, ydimensions), 1)[0]
            zval = random.sample(xrange(0, zdimensions), 1)[0]
            value = rawImg[xval, yval, zval]
            if [xval, yval, zval] not in xyz and value > 300:
                xyz.append([xval, yval, zval])
            else:
                value = 0
    return xyz

def save_points(points, path=None):
    """Saves points array into a .csv file."""
    np.savetxt(path, points, fmt='%d', delimiter=',')

def im_to_scatterplot(im):
    tupleResolution = inImg.GetSpacing();

def array_to_scatterplot(points, resolution, output_path):
    # Set tupleResolution to resolution input parameter
    tupleResolution = resolution;

    # EG: for Aut1367, the spacing is (0.01872, 0.01872, 0.005).
    xResolution = tupleResolution[0]
    yResolution = tupleResolution[1]
    zResolution = tupleResolution[2]
    # Now, to get the mm image size, we can multiply all x, y, z
    # to get the proper mm size when plotting.

    trace1 = Scatter3d(
        x=[x * xResolution for x in points['a']],
        y=[x * yResolution for x in points['b']],
        z=[x * zResolution for x in points['c']],
        mode='markers',
        marker=dict(
            size=1.2,
            color='cyan',  # set color to an array/list of desired values
            colorscale='Viridis',  # choose a colorscale
            opacity=0.15
        )
    )

    data = [trace1]
    layout = Layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        ),
        paper_bgcolor='rgb(0,0,0)',
        plot_bgcolor='rgb(0,0,0)'
    )

    fig = Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=output_path)


def apply_clahe(im_path):
    im = nib.load(im_path)
    im = im.get_data()

    num_slices = im.shape[2]

    for slice in

    slice = aut_im[:, :, 400]

    # create a CLAHE object (Arguments are optional).
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(10,10))
    aut_slice_clahe = clahe.apply(aut_slice)

def nii_to_array(brain_path, anno_path):
    anno_img = nb.load(anno_path)  # <- annotation .nii image
    brain_img = nb.load(brain_path)  # <- annotation .nii image

    anno_img





