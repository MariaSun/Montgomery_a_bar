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

#import masks
mask1=np.loadtxt("mask1_0111010_2.txt", delimiter=',')
mask2=np.loadtxt("mask2_0111010_2.txt", delimiter=',')

#assign size
if len(mask1)!=len(mask1[0]) or len(mask2)!=len(mask2[0]):
	print("Error, masks are not rectangular! Supply rectangular masks.")

if len(mask1)!=len(mask1[0]) and len(mask2)!=len(mask2[0]) and len(mask1) != len(mask2):
	print("Error, dimensions of mask1 != mask2. Suppy equal dimentions.")

GridDimension = len(mask1)
GridSize = 50*um
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
Field3 = Lens(6*cm,0,0,Field3)
Field3 = Forward(Field3, 4.5*cm, 10*mm, 20)

I3=Intensity(0, Field3)

#plotting
f, axarr = plt.subplots(1,3)
axarr[0].imshow(I1)
axarr[1].imshow(I2)
axarr[2].imshow(I3)
plt.show()