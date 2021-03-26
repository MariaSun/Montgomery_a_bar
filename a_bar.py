import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from LightPipes import *
import cmath 
import math
from math import sqrt
from SLM_mask import SLM_mask
from SLM_mask import get_middle
from SLM_mask import bypixel_mask
from SLM_mask import expand_mask
from SLM_mask import pad_with
import cv2

#import masks
gauss_parameter = 5#has to be an odd number

mask1=np.loadtxt("mask1_0111010_2.txt", delimiter=',')#mask1_0111010_2.txt  #mask1_0100010
mask1=expand_mask(mask1,6)#replaces each pixel with an NXN superpixel
mask1 = np.pad(mask1, 20, pad_with, padder=0.)
mask1 = np.pad(mask1, (1, 0), 'constant', constant_values=(0., 0.))
mask1 = cv2.GaussianBlur(mask1,(gauss_parameter,gauss_parameter),0)
mask2=np.loadtxt("mask2_0111010_2.txt", delimiter=',')
mask2=expand_mask(mask2,6)#replaces each pixel with an NXN superpixel
mask2 = np.pad(mask2, 20, pad_with, padder=0.)
mask2 = np.pad(mask2, (1, 0), 'constant', constant_values=(0., 0.))
mask2 = cv2.GaussianBlur(mask2,(gauss_parameter,gauss_parameter),0)

#assign size
if len(mask1)!=len(mask1[0]) or len(mask2)!=len(mask2[0]):
	print("Error, masks are not rectangular! Supply rectangular masks.")

if len(mask1)!=len(mask1[0]) and len(mask2)!=len(mask2[0]) and len(mask1) != len(mask2):
	print("Error, dimensions of mask1 != mask2. Suppy equal dimentions.")

GridDimension = len(mask1)
GridSize = 5*mm
R = GridSize/GridDimension

lambda_ = 650*nm #lambda_ is used because lambda is a Python build-in function.

#define the field
Field = Begin(GridSize, lambda_, GridDimension)

#Phase-only SLM
Field1 = bypixel_mask(Field, mask1)
Field2 = bypixel_mask(Field, mask2)

I1=Intensity(0,Field1)
I2=Intensity(0,Field2)

#Adding two fields
Field2.field = - Field2.field
Field3 = BeamMix(Field1, Field2)

#Ideal thing lens
focal_distance = 20*cm#300*cm for 1X1 size mapping
Field3 = Lens(focal_distance,0,0,Field3)

Field3 = Forward(Field3, focal_distance, 0.5*mm, 300)

I3=Intensity(0, Field3)

#plotting
f, axarr = plt.subplots(1,3)
axarr[0].imshow(I1)
axarr[1].imshow(I2)
axarr[2].imshow(I3)
plt.show()